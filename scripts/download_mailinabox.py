#!/usr/bin/env python3
"""Download a release archive of Mail-in-a-Box.

This utility fetches the latest Mail-in-a-Box release (or a user-specified
version) and downloads the source archive to a target directory.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Tuple

API_LATEST_RELEASE = "https://api.github.com/repos/mail-in-a-box/mailinabox/releases/latest"
ARCHIVE_TEMPLATE = "https://github.com/mail-in-a-box/mailinabox/archive/refs/tags/{tag}.tar.gz"


def fetch_latest_release() -> Tuple[str, str]:
    """Return the latest release tag and archive URL.

    Raises:
        RuntimeError: If the latest release information cannot be retrieved.
    """

    try:
        with urllib.request.urlopen(API_LATEST_RELEASE) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"GitHub API request failed with status code {response.status}."
                )
            data = json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError("Unable to retrieve latest release information.") from exc

    tag_name = data.get("tag_name")
    tarball_url = data.get("tarball_url")

    if not tag_name:
        raise RuntimeError("Latest release tag is missing from the API response.")

    if not tarball_url:
        tarball_url = ARCHIVE_TEMPLATE.format(tag=tag_name)

    return tag_name, tarball_url


def download_archive(url: str, destination: Path) -> None:
    """Download the archive at ``url`` to ``destination``.

    Args:
        url: The download URL for the archive.
        destination: Path where the archive should be saved.

    Raises:
        RuntimeError: If the download fails.
    """

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Download failed with status code {response.status}."
                )
            destination.write_bytes(response.read())
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to download archive from {url}.") from exc


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Download the latest Mail-in-a-Box release archive."
    )
    parser.add_argument(
        "--version",
        help=(
            "Specific Mail-in-a-Box release tag to download (for example, v60). "
            "If omitted, the latest release is downloaded."
        ),
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Directory where the archive should be saved (defaults to the current directory).",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.version:
        tag_name = args.version
        download_url = ARCHIVE_TEMPLATE.format(tag=tag_name)
    else:
        try:
            tag_name, download_url = fetch_latest_release()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 1

    archive_name = f"mailinabox-{tag_name}.tar.gz"
    destination = output_dir / archive_name

    if destination.exists():
        print(f"Archive already exists at {destination}.", file=sys.stderr)
        return 0

    try:
        download_archive(download_url, destination)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Downloaded {tag_name} to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
