#!/usr/bin/env python3
"""Publish uncurl-httpx to PyPI using twine."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd, check=True):
    """Run a shell command."""
    print(f"+ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result


def get_token():
    """Get PyPI token from environment or .env file."""
    # Try environment variable first
    token = os.environ.get("PYPI_TOKEN")
    if token:
        return token

    # Try .env file
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("PYPI_TOKEN="):
                return line.split("=", 1)[1].strip("\"'")

    raise RuntimeError(
        "PyPI token not found. Set PYPI_TOKEN env var or create .env file with PYPI_TOKEN=..."
    )


def main():
    project_root = Path(__file__).resolve().parent.parent

    print("=" * 70)
    print("Publishing uncurl-httpx to PyPI")
    print("=" * 70)

    # Clean up old builds
    print("\n[1/4] Cleaning old builds...")
    for d in ["dist", "build"]:
        path = project_root / d
        if path.exists():
            shutil.rmtree(path)
            print(f"  Removed {d}/")

    # Run tests
    print("\n[2/4] Running tests...")
    run([sys.executable, "-m", "pytest", "-q"], cwd=project_root)

    # Build
    print("\n[3/4] Building distributions...")
    run([sys.executable, "-m", "build"], cwd=project_root)

    # Check
    print("\n[4/4] Checking distributions...")
    dist_dir = project_root / "dist"
    dist_files = sorted(dist_dir.glob("*"))
    if not dist_files:
        raise RuntimeError("No distributions found in dist/")
    run([sys.executable, "-m", "twine", "check"] + [str(f) for f in dist_files])

    # Upload
    print("\n[Upload] Uploading to PyPI...")
    token = get_token()
    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token

    result = subprocess.run(
        [sys.executable, "-m", "twine", "upload"] + [str(f) for f in dist_files],
        env=env,
        cwd=project_root,
    )

    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("✓ Successfully published to PyPI!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗ Upload failed")
        print("=" * 70)
        return result.returncode

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

