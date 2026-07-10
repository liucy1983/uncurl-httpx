Forked from https://github.com/spulec/uncurl

## Changes In This Fork

1. Switched generated client code from `requests` to `httpx`.
2. Updated proxy and redirect argument rendering to match `httpx` semantics.
3. Removed Python 2 compatibility code and standardized on Python 3.
4. Replaced legacy test tooling with `pytest` and simplified the test suite.
5. Removed unused legacy dependencies such as `six`, `mock`, `sure`, `nose`, and `coverage`.
6. Improved code generation safety by using Python-safe literals instead of manual string quoting.
7. Unified cookie parsing so `--cookie` and `Cookie:` headers are handled consistently.
8. Omit empty request arguments in generated output to produce cleaner `httpx` code.


# Uncurl - Converting curl requests to httpx

# In a nutshell

Uncurl is a library that allows you to convert curl requests into python code that uses [httpx](https://www.python-httpx.org/). Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for recreating browser requests in python.

When you don't pass any arguments to uncurl, it will use whatever is in your clipboard as the curl command.


## Example

```bash
$ uncurl "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: foo=bar;' -H 'Connection: keep-alive' --compressed"
httpx.get("https://pypi.python.org/pypi/uncurl-httpx", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}, cookies={
    "foo": "bar",
})
```

The underlying API:

```python
import uncurl

print(uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'"))
```

如果你想直接发起请求，也可以调用：

```python
import uncurl

response = uncurl.request(
    "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'",
    timeout=5.0,
)
print(response.status_code)
```

prints the string

```bash
'httpx.get("https://pypi.python.org/pypi/uncurl-httpx", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
})'
```

You can also retrieve the components as python objects:

```python
>>> import uncurl
>>> context = uncurl.parse_context("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'")
>>> context.url
https://pypi.python.org/pypi/uncurl-httpx
>>> context.headers
OrderedDict([('Accept-Encoding', 'gzip,deflate,sdch')])
```

Or ask `parse()` to return the same mutable object, then tweak and send it:

```python
import uncurl

parsed = uncurl.parse(
    "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'",
    as_object=True,
)
parsed.url = "https://example.com/api"
parsed.headers["X-Debug"] = "1"

response = parsed.request(timeout=5.0)
print(response.status_code)
```

On Mac OS, you can also pipe input to uncurl:

```bash
pbpaste | uncurl
```

## Install

```console
$ pip install uncurl-httpx
```
