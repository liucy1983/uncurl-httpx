# -*- coding: utf-8 -*-
import argparse
import json
import re
import shlex
from collections import OrderedDict
from dataclasses import dataclass, field
from http.cookies import SimpleCookie
from typing import Any, Optional, Tuple

import httpx

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data')
parser.add_argument('-b', '--cookie', default='')
parser.add_argument('--data-binary', '--data-raw', default=None)
parser.add_argument('-X', default='')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('-k','--insecure', action='store_true')
parser.add_argument('--user', '-u', default=())
parser.add_argument('-i','--include', action='store_true')
parser.add_argument('-s','--silent', action='store_true')
parser.add_argument('-x', '--proxy', default={})
parser.add_argument('-U', '--proxy-user', default='')

BASE_INDENT = " " * 4


@dataclass
class ParsedContext:
    method: str
    url: str
    data: Optional[str] = None
    headers: OrderedDict = field(default_factory=OrderedDict)
    cookies: OrderedDict = field(default_factory=OrderedDict)
    verify: bool = False
    auth: Tuple[str, ...] = ()
    proxy: Any = field(default_factory=dict)

    def build_request_kwargs(self, **kwargs):
        request_kwargs = dict(kwargs)
        if 'allow_redirects' in request_kwargs:
            request_kwargs['follow_redirects'] = request_kwargs.pop('allow_redirects')

        if self.data:
            request_kwargs['data'] = self.data

        if self.headers:
            request_kwargs['headers'] = dict(self.headers)

        if self.cookies:
            request_kwargs['cookies'] = dict(self.cookies)

        if self.auth:
            request_kwargs['auth'] = self.auth

        if self.proxy:
            request_kwargs['proxy'] = self.proxy

        if self.verify:
            request_kwargs['verify'] = False

        return request_kwargs

    def to_code(self, **kwargs):
        request_kwargs = []

        for key, value in sorted(kwargs.items()):
            if key == 'allow_redirects':
                key = 'follow_redirects'
            request_kwargs.append(format_request_arg(key, value))

        if self.data:
            request_kwargs.append(format_request_arg('data', self.data))

        if self.headers:
            request_kwargs.append(format_dict_arg('headers', self.headers))

        if self.cookies:
            request_kwargs.append(format_dict_arg('cookies', self.cookies))

        if self.auth:
            request_kwargs.append(format_request_arg('auth', self.auth))

        if self.proxy:
            request_kwargs.append(format_request_arg('proxy', self.proxy))

        if self.verify:
            request_kwargs.append(format_request_arg('verify', False, trailing_comma=False))

        if not request_kwargs:
            return "httpx.{method}({url})".format(
                method=self.method,
                url=json.dumps(self.url),
            )

        return """httpx.{method}({url},
{request_kwargs}
)""".format(
            method=self.method,
            url=json.dumps(self.url),
            request_kwargs='\n'.join(request_kwargs),
        )

    def request(self, **kwargs):
        return httpx.request(self.method, self.url, **self.build_request_kwargs(**kwargs))


def normalize_newlines(multiline_text):
    return multiline_text.replace(" \\\n", " ")


def parse_cookies(cookie_string):
    if not cookie_string:
        return OrderedDict()

    cookie = SimpleCookie(cookie_string)
    return OrderedDict((key, morsel.value) for key, morsel in sorted(cookie.items()))


def parse_context(curl_command):
    method = "get"

    tokens = shlex.split(normalize_newlines(curl_command))
    parsed_args = parser.parse_args(tokens)

    post_data = parsed_args.data or parsed_args.data_binary
    if post_data:
        method = 'post'

    if parsed_args.X:
        method = parsed_args.X.lower()

    cookie_dict = parse_cookies(parsed_args.cookie)
    
    quoted_headers = OrderedDict()

    for curl_header in parsed_args.header:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == 'cookie':
            decoded_cookie = bytes(header_value, "ascii").decode("unicode-escape")
            cookie_dict.update(parse_cookies(decoded_cookie))
        else:
            quoted_headers[header_key] = header_value.strip()

    # add auth
    user = parsed_args.user
    if parsed_args.user:
        user = tuple(user.split(':'))

    # add proxy and its authentication if it's available.
    proxy = parsed_args.proxy
    if parsed_args.proxy and parsed_args.proxy_user:
        proxy = "http://{}@{}/".format(parsed_args.proxy_user, parsed_args.proxy)
    elif parsed_args.proxy:
        proxy = "http://{}/".format(parsed_args.proxy)

    return ParsedContext(
        method=method,
        url=parsed_args.url,
        data=post_data,
        headers=quoted_headers,
        cookies=cookie_dict,
        verify=parsed_args.insecure,
        auth=user,
        proxy=proxy,
    )


def parse(curl_command, as_object=True, **kwargs):
    parsed_context = parse_context(curl_command)

    if as_object:
        return parsed_context

    return parsed_context.to_code(**kwargs)


def request(curl_command, **kwargs):
    parsed_context = parse_context(curl_command)
    return parsed_context.request(**kwargs)


def format_request_arg(key, value, trailing_comma=True):
    suffix = ',' if trailing_comma else ''
    return "{}{}={}{}".format(BASE_INDENT, key, repr(value), suffix)


def format_dict_arg(key, value):
    return "{}{}={},".format(BASE_INDENT, key, dict_to_pretty_string(value))


def dict_to_pretty_string(the_dict, indent=4):
    if not the_dict:
        return "{}"

    return ("\n" + " " * indent).join(
        json.dumps(the_dict, sort_keys=True, indent=indent, separators=(',', ': ')).splitlines())

