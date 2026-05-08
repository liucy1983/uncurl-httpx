# Changelog

## Unreleased

- Added `uncurl.request(curl_command, **kwargs)` to parse a curl command and execute the request directly via `httpx.request(...)`.
- Exported `request` from the top-level `uncurl` package alongside `parse` and `parse_context`.
- Added test coverage for direct request execution, including forwarding `allow_redirects` as `follow_redirects`.
- Added `httpx>=0.28.0` to runtime dependencies.
- Documented the direct request API in the README.
