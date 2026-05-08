import uncurl
from unittest.mock import sentinel


def assert_parse(command, expected, **kwargs):
    assert uncurl.parse(command, **kwargs) == expected


def test_request_executes_httpx_request(mocker=None):
    from unittest.mock import patch

    with patch("uncurl.api.httpx.request", return_value=sentinel.response) as request_mock:
        response = uncurl.request(
            "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' --data 'payload' --insecure",
            timeout=0.1,
            allow_redirects=True,
        )

    assert response is sentinel.response
    request_mock.assert_called_once_with(
        'post',
        'https://pypi.python.org/pypi/uncurl-httpx',
        timeout=0.1,
        follow_redirects=True,
        data='payload',
        headers={
            'Accept-Encoding': 'gzip,deflate,sdch',
        },
        verify=False,
    )


def test_basic_get():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx")"""
    )


def test_colon_header():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'authority:mobile.twitter.com'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "authority": "mobile.twitter.com"
    },
)"""
    )


def test_basic_headers():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
)"""
    )


def test_cookies():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_cookies_lowercase():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'cookie: foo=bar; baz=baz2'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )

def test_cookies_dollar_sign():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H $'Cookie: somereallyreallylongcookie=true'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "somereallyreallylongcookie": "true"
    },
)"""
    )

def test_post():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --data '[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data='[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_post_with_dict_data():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --data '{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data='{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_post_with_string_data():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --data 'this is just some data'""", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data='this is just some data',
)"""
    )


def test_parse_curl_with_binary_data():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --data-binary 'this is just some data'""", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data='this is just some data',
)"""
    )

def test_parse_curl_with_raw_data():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --data-raw 'this is just some data'""", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data='this is just some data',
)"""
    )


def test_post_with_single_quote_data():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' --data \"it's me\"", """httpx.post("https://pypi.python.org/pypi/uncurl-httpx",
    data="it's me",
)"""
    )

def test_parse_curl_with_another_binary_data():
    assert_parse("""curl -H 'PID: 20000079' -H 'MT: 4' -H 'DivideVersion: 1.0' -H 'SupPhone: Redmi Note 3' -H 'SupFirm: 5.0.2' -H 'IMEI: wx_app' -H 'IMSI: wx_app' -H 'SessionId: ' -H 'CUID: wx_app' -H 'ProtocolVersion: 1.0' -H 'Sign: 7876480679c3cfe9ec0f82da290f0e0e' -H 'Accept: /' -H 'BodyEncryptType: 0' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({"packageName":"com.oppo.market","type":"other","extra":{}})' -H 'Content-Type: text/plain; charset=utf-8' -H 'Host: pandahomeios.ifjing.com' --data-binary '{"CateID":"508","PageIndex":1,"PageSize":30}' --compressed 'http://pandahomeios.ifjing.com/action.ashx/otheraction/9028'""", r"""httpx.post("http://pandahomeios.ifjing.com/action.ashx/otheraction/9028",
    data='{"CateID":"508","PageIndex":1,"PageSize":30}',
    headers={
        "Accept": "/",
        "BodyEncryptType": "0",
        "CUID": "wx_app",
        "Content-Type": "text/plain; charset=utf-8",
        "DivideVersion": "1.0",
        "Host": "pandahomeios.ifjing.com",
        "IMEI": "wx_app",
        "IMSI": "wx_app",
        "MT": "4",
        "PID": "20000079",
        "ProtocolVersion": "1.0",
        "SessionId": "",
        "Sign": "7876480679c3cfe9ec0f82da290f0e0e",
        "SupFirm": "5.0.2",
        "SupPhone": "Redmi Note 3",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({\"packageName\":\"com.oppo.market\",\"type\":\"other\",\"extra\":{}})"
    },
)""")


def test_parse_curl_with_insecure_flag():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' --insecure""", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    verify=False
)"""
    )

def test_parse_curl_with_request_kargs():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    follow_redirects=True,
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
)""", timeout=0.1, allow_redirects=True)
                      
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
)""", timeout=0.1)
                      
def test_parse_curl_with_escaped_newlines():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' \
 -H 'Accept-Encoding: gzip,deflate' \
 --insecure""", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate"
    },
    verify=False
)"""
    )
    
def test_parse_curl_escaped_unicode_in_cookie():
    assert_parse("""curl 'https://pypi.python.org/pypi/uncurl-httpx' -H $'cookie: sid=00Dt00000004XYz\\u0021ARg' """, """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    cookies={
        "sid": "00Dt00000004XYz!ARg"
    },
)""")

def test_parse_curl_with_proxy_and_proxy_auth():
    assert_parse("curl 'https://pypi.python.org/pypi/uncurl-httpx' -U user: -x proxy.python.org:8080", """httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    proxy='http://user:@proxy.python.org:8080/',
)""")



if __name__ == '__main__':
    test_basic_get()
    test_colon_header()
    test_basic_headers()
    test_cookies()
    test_cookies_lowercase()
    test_post()
    test_post_with_dict_data()
    test_post_with_string_data()
    test_parse_curl_with_binary_data()
    test_parse_curl_with_raw_data()
    test_post_with_single_quote_data()
    test_parse_curl_with_another_binary_data()
    test_parse_curl_with_insecure_flag()
    test_parse_curl_with_request_kargs()
    test_parse_curl_with_proxy_and_proxy_auth()
