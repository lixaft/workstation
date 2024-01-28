#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from typing import NamedTuple
from typing import Protocol

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSTATION_FILE = os.path.join(ROOT, "roles/workstation/vars/main.yml")


def _to_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in version.split("."))


def _cmp(a: str, b: str) -> int:
    return _to_tuple(a) > _to_tuple(b)


class Strategy(Protocol):
    def get_latest_version(self) -> str | None: ...


class Github(NamedTuple):
    repo: str
    pattern: re.Pattern[str]

    def get_latest_version(self) -> str | None:
        url = f"https://api.github.com/repos/{self.repo}/releases"
        releases = json.loads(urllib.request.urlopen(url).read())

        latest = None
        for rel in releases:
            match = self.pattern.match(rel["name"])
            if not match:
                continue
            version = match.group(1)

            if latest is None or _cmp(version, latest):
                latest = version

        return latest


class Changelog(NamedTuple):
    url: str
    pattern: re.Pattern[str]

    def get_latest_version(self) -> str | None:
        doc = urllib.request.urlopen(self.url).read().decode("utf-8")

        latest = None
        for line in doc.splitlines():
            match = self.pattern.match(line)
            if not match:
                continue
            version = match.group(1)

            if latest is None or _cmp(version, latest):
                latest = version

        return latest


class Go:
    def get_latest_version(self) -> str | None:
        url = "https://go.dev/dl/?mode=json"
        releases = json.loads(urllib.request.urlopen(url).read())

        latest = None
        for rel in releases:
            if not rel["stable"]:
                continue
            version = rel["version"].lstrip("go")

            if latest is None or _cmp(version, latest):
                latest = version

        return latest


def update(lines: list[str], key: str, strategy: Strategy) -> None:
    i = None
    for j, line in enumerate(lines):
        if line.startswith(f"{key}:"):
            i = j
            break

    version = strategy.get_latest_version()
    if version is None:
        sys.stderr.write(f"Could not find latest version for {key}\n")
        sys.stderr.flush()
        return

    s = f"{key}: {version}\n"
    if i is None:
        lines.append(s)
    else:
        lines[i] = s


def main() -> int:
    with open(WORKSTATION_FILE) as f:
        lines = f.readlines()

    re_bazecor = re.compile(r"^(?:Bazecor |v)?(\d+\.\d+\.\d+)$")
    re_mrv2 = re.compile(r"^mrv2 v(\d+\.\d+\.\d+)$")
    re_rack = re.compile(r"^### (\d+\.\d+\.\d+) \(\d+-\d+-\d+\)$")
    re_version = re.compile(r"^(\d+\.\d+\.\d+)$")
    url_rack = "https://raw.githubusercontent.com/VCVRack/Rack/v2/CHANGELOG.md"

    update(lines, "bazecor_version", Github("Dygmalab/Bazecor", re_bazecor))
    update(lines, "go_version", Go())
    update(lines, "mrv2_version", Github("ggarra13/mrv2", re_mrv2))
    update(lines, "opam_version", Github("ocaml/opam", re_version))
    update(lines, "rack_version", Changelog(url_rack, re_rack))
    update(lines, "zig_version", Github("ziglang/zig", re_version))

    with open(WORKSTATION_FILE, "w") as f:
        f.writelines(lines)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
if __name__ == "__main__":
    raise SystemExit(main())
