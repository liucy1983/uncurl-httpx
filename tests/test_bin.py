from unittest.mock import patch
from uncurl.bin import main


@patch("uncurl.bin.sys")
@patch("uncurl.bin.print")
def test_main(printer, fake_sys):
    fake_sys.argv = ['uncurl', "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'"]
    main()

    printer.assert_called_once_with(
        """
httpx.get("https://pypi.python.org/pypi/uncurl-httpx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
)""")
