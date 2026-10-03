#!/usr/bin/env python3
"""Create deterministic Sarack binary release archives from built TTFs."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont

MONO_FILES = (
    "SarackMono-Regular.ttf",
    "SarackMono-Bold.ttf",
    "SarackMono-Italic.ttf",
    "SarackMono-BoldItalic.ttf",
    "SarackMonoHS-Regular.ttf",
    "SarackMonoHS-Bold.ttf",
    "SarackMonoHS-Italic.ttf",
    "SarackMonoHS-BoldItalic.ttf",
)

TERM_FILES = (
    "SarackTerm-Regular.ttf",
    "SarackTerm-Bold.ttf",
    "SarackTerm-Italic.ttf",
    "SarackTerm-BoldItalic.ttf",
    "SarackTermHS-Regular.ttf",
    "SarackTermHS-Bold.ttf",
    "SarackTermHS-Italic.ttf",
    "SarackTermHS-BoldItalic.ttf",
)

LICENSE_SOURCES = (
    Path("LICENSE-FONT"),
    Path("LICENSES/Sarasa-Gothic-OFL.txt"),
    Path("LICENSES/Hack-LICENSE.md"),
)

LICENSE_HEADINGS = (
    "Sarack Font License",
    "Sarasa Gothic / Source Han Sans notices",
    "Hack / Bitstream Vera notices",
)


def license_bundle(repo_root: Path) -> bytes:
    """Join complete license sources, normalizing line endings only."""
    sections = []
    for heading, relative in zip(LICENSE_HEADINGS, LICENSE_SOURCES, strict=True):
        text = (repo_root / relative).read_bytes().decode("utf-8")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        sections.append(f"{'=' * 50}\n{heading}\n{'=' * 50}\n\n{text}\n")
    data = "\n".join(sections).encode("utf-8")
    for notice in (
        b"SIL OPEN FONT LICENSE Version 1.1",
        b"Copyright (c) 2015-2025, Renzhi Li",
        b"Adobe Systems Incorporated",
        b"Reserved Font Name 'Source'",
        b"Copyright 2018 Source Foundry Authors",
        b"MIT License",
        b"Bitstream Vera License",
    ):
        if notice not in data:
            raise RuntimeError(f"Required license notice missing: {notice!r}")
    return data

EXPECTED_FONT_PROPERTIES = {
    "SarackMono-": ("Sarack Mono", 1000),
    "SarackMonoHS-": ("Sarack Mono HS", 1000),
    "SarackTerm-": ("Sarack Term", 500),
    "SarackTermHS-": ("Sarack Term HS", 500),
}

EXPECTED_HALF_WIDTH = 500
EXPECTED_FULL_WIDTH = 1000
UNHINTED_TABLES = ("cvt ", "fpgm", "prep")

ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--mono-dir", required=True, type=Path)
    parser.add_argument("--term-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?", args.version):
        raise ValueError("--version must be a semantic-style version token such as 0.1.0")
    return args


def get_name(font: TTFont, name_id: int) -> str | None:
    record = font["name"].getName(name_id, 3, 1, 0x0409)
    if record is not None:
        return record.toUnicode()
    for candidate in font["name"].names:
        if candidate.nameID == name_id:
            try:
                return candidate.toUnicode()
            except UnicodeDecodeError:
                pass
    return None


def expected_font_properties(filename: str) -> tuple[str, int]:
    for prefix, properties in EXPECTED_FONT_PROPERTIES.items():
        if filename.startswith(prefix):
            return properties
    raise RuntimeError(f"Unknown Sarack release filename: {filename}")


def validate_font(path: Path, version: str) -> None:
    font = TTFont(path, recalcBBoxes=False, recalcTimestamp=False)
    family, expected_em_dash_width = expected_font_properties(path.name)
    if get_name(font, 1) != family or get_name(font, 16) != family:
        raise RuntimeError(f"Family metadata mismatch: {path.name}")
    if get_name(font, 5) != f"Version {version}":
        raise RuntimeError(f"Version metadata mismatch: {path.name}")
    if get_name(font, 13) != "This Font Software is licensed under the SIL Open Font License, Version 1.1.":
        raise RuntimeError(f"License metadata mismatch: {path.name}")
    if get_name(font, 14) != "https://openfontlicense.org":
        raise RuntimeError(f"License URL metadata mismatch: {path.name}")

    cmap = font.getBestCmap()
    required_codepoints = (0x30, 0x3042, 0x3000, 0x2014)
    if cmap is None or any(codepoint not in cmap for codepoint in required_codepoints):
        missing = [
            f"U+{codepoint:04X}"
            for codepoint in required_codepoints
            if cmap is None or codepoint not in cmap
        ]
        raise RuntimeError(
            f"Required release glyphs missing from {path.name}: {', '.join(missing)}"
        )

    hmtx = font["hmtx"].metrics
    half_width = hmtx[cmap[0x30]][0]
    full_width = hmtx[cmap[0x3042]][0]
    u3000_width = hmtx[cmap[0x3000]][0]
    em_dash_width = hmtx[cmap[0x2014]][0]
    if half_width != EXPECTED_HALF_WIDTH:
        raise RuntimeError(
            f"Half width mismatch in {path.name}: {half_width} != {EXPECTED_HALF_WIDTH}"
        )
    if full_width != EXPECTED_FULL_WIDTH:
        raise RuntimeError(
            f"Full width mismatch in {path.name}: {full_width} != {EXPECTED_FULL_WIDTH}"
        )
    if u3000_width != EXPECTED_FULL_WIDTH:
        raise RuntimeError(
            f"U+3000 width mismatch in {path.name}: {u3000_width} != {EXPECTED_FULL_WIDTH}"
        )
    if em_dash_width != expected_em_dash_width:
        raise RuntimeError(
            f"U+2014 width mismatch in {path.name}: "
            f"{em_dash_width} != {expected_em_dash_width}"
        )

    present_hinting_tables = [tag for tag in UNHINTED_TABLES if tag in font]
    if present_hinting_tables:
        raise RuntimeError(
            f"Unhinted validation failed for {path.name}; unexpected tables: "
            + ", ".join(repr(tag) for tag in present_hinting_tables)
        )

    print(
        f"Validated {path.name}: half/full={half_width}/{full_width}, "
        f"U+3000={u3000_width}, U+2014={em_dash_width}, "
        "Unhinted tables absent"
    )


def require_inputs(directory: Path, filenames: tuple[str, ...], version: str) -> list[Path]:
    result = []
    for filename in filenames:
        path = directory / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        validate_font(path, version)
        result.append(path)
    return result


def add_file(zf: zipfile.ZipFile, data: bytes, archive_name: str) -> None:
    info = zipfile.ZipInfo(archive_name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def write_archive(
    archive_path: Path,
    root_name: str,
    fonts: list[Path],
    licenses: bytes,
) -> None:
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for font in sorted(fonts, key=lambda p: p.name):
            add_file(zf, font.read_bytes(), f"{root_name}/{font.name}")
        add_file(zf, licenses, f"{root_name}/LICENSES.txt")


def validate_archive(
    archive_path: Path, root_name: str, filenames: tuple[str, ...], licenses: bytes
) -> None:
    expected = [f"{root_name}/{name}" for name in sorted(filenames)]
    expected.append(f"{root_name}/LICENSES.txt")
    with zipfile.ZipFile(archive_path) as archive:
        if archive.namelist() != expected:
            raise RuntimeError(f"Unexpected release entries/order: {archive_path.name}")
        if any(entry.date_time != ZIP_TIMESTAMP for entry in archive.infolist()):
            raise RuntimeError(f"Unexpected ZIP timestamp: {archive_path.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {archive_path.name}")
        if archive.read(f"{root_name}/LICENSES.txt") != licenses:
            raise RuntimeError(f"License bundle mismatch: {archive_path.name}")
    print(f"Verified {archive_path.name}: 8 TTF + LICENSES.txt; no extra files")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    mono = require_inputs(args.mono_dir.resolve(), MONO_FILES, args.version)
    term = require_inputs(args.term_dir.resolve(), TERM_FILES, args.version)

    licenses = license_bundle(repo_root)
    targets = (
        ("Mono", mono, MONO_FILES),
        ("Term", term, TERM_FILES),
    )
    archives = []
    for variant, fonts, filenames in targets:
        root_name = f"Sarack-{variant}-v{args.version}"
        archive_path = output_dir / f"{root_name}.zip"
        write_archive(archive_path, root_name, fonts, licenses)
        validate_archive(archive_path, root_name, filenames, licenses)
        archives.append(archive_path)
        print(f"Created {archive_path}")

    with zipfile.ZipFile(archives[0]) as mono_zip, zipfile.ZipFile(archives[1]) as term_zip:
        if mono_zip.read(f"Sarack-Mono-v{args.version}/LICENSES.txt") != term_zip.read(
            f"Sarack-Term-v{args.version}/LICENSES.txt"
        ):
            raise RuntimeError("Mono/Term license bundles differ")
    print("Mono/Term LICENSES.txt: byte-identical")

    checksums = output_dir / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in archives),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Created {checksums}")


if __name__ == "__main__":
    main()
