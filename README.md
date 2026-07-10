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

parsed = uncurl.parse(
    "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'"
)
print(parsed.headers)
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

If you want the generated `httpx` code string, ask explicitly:

```python
import uncurl

print(
    uncurl.parse(
        "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'",
        as_object=False,
    )
)
```

This prints:

```bash
httpx.get("https://pypi.python.org/pypi/uncurl-httpx", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
})
```

You can also retrieve the components as python objects:

```python
import uncurl

context = uncurl.parse_context(
    "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'"
)
print(context.url)
print(context.headers)
```

`parse()` already returns a mutable object by default, so you can tweak and send it directly:

```python
import uncurl

parsed = uncurl.parse(
    "curl 'https://pypi.python.org/pypi/uncurl-httpx' -H 'Accept-Encoding: gzip,deflate,sdch'"
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

## Release to PyPI with GitHub Actions

This repository includes `.github/workflows/publish.yml` for automated releases. However, if GitHub Actions is disabled on your account, you can publish manually.

## Manual Release to PyPI

Create a local `.env` file at the project root:

```dotenv
PYPI_TOKEN=pypi-your-token-from-pypi-org
```

Then run:

```bash
make publish
```

Or directly:

```bash
uv run python scripts/publish.py
```

The script will:
1. Run tests
2. Build distributions
3. Check with `twine`
4. Upload to PyPI

After upload completes, the new version will appear on [PyPI](https://pypi.org/project/uncurl-httpx/).

## Automated Release with GitHub Actions

This repository includes `.github/workflows/publish.yml`.
Pushing a tag like `v0.1.1` will:

1. run the test suite,
2. build the package,
3. validate the built artifacts with `twine check`,
4. publish to PyPI.

Before using it, configure a PyPI Trusted Publisher for this GitHub repository and workflow.

Create and push a release tag with:

```bash
git tag v0.1.1
git push origin v0.1.1
```

