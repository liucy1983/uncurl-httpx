# Changelog

## Unreleased

## 0.1.1 - 2026-07-10

- Added object mode for `parse(...)` via `as_object=True`, returning a mutable `ParsedContext` for post-parse edits.
- Replaced the old immutable `ParsedContext` tuple with a dataclass and added `ParsedContext.to_code(...)` to render updated request code.
- Added `ParsedContext.request(...)` as the primary object API for dispatching requests, aligned with `httpx`/`requests` naming.
- Kept `ParsedContext.send(...)` as a backward-compatible alias to `ParsedContext.request(...)`.
- Exported `ParsedContext` from the top-level `uncurl` package and added tests/docs for the object workflow.
- Updated type annotations in `uncurl/api.py` to more broadly compatible `typing` forms for IDE/parser compatibility.

## 0.1.0 - 2026-05-08
- Added `uncurl.request(curl_command, **kwargs)` to parse a curl command and execute the request directly via `httpx.request(...)`.
- Exported `request` from the top-level `uncurl` package alongside `parse` and `parse_context`.
- Added test coverage for direct request execution, including forwarding `allow_redirects` as `follow_redirects`.
- Added `httpx>=0.28.0` to runtime dependencies.
- Documented the direct request API in the README.
