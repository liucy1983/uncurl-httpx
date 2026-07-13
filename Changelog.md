# Changelog

## Unreleased

## 0.1.3 - 2026-07-13

- Added `is_json_data` field to `ParsedContext` to auto-detect JSON payloads and handle them accordingly.
- Implemented JSON auto-detection with fallback: `parse_context()` attempts to parse `--data` as JSON when `is_json_data=True`, falling back to plain text on failure.
- Added JSON validation to `ParsedContext.set_data()`: warns and skips assignment if the current payload is not a JSON object.
- Updated `ParsedContext.to_code()` to preserve original JSON string format when generating code, ensuring curl-like output with compact JSON serialization.
- Enhanced `ParsedContext.build_request_kwargs()` to handle both JSON-parsed objects (serialized via `json.dumps`) and plain text payloads.

## 0.1.2 - 2026-07-10

- Added `.github/workflows/publish.yml` to test, build, and publish tagged releases to PyPI via GitHub Actions.
- Documented the GitHub Actions release flow and PyPI Trusted Publisher setup in `README.md`.
- Made `parse(...)` return a mutable `ParsedContext` by default; pass `as_object=False` when you want generated `httpx` source code.
- Updated the CLI and tests to request string output explicitly where needed.

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
