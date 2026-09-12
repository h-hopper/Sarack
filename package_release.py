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

COMMON_FILES = (
    Path("LICENSE-FONT"),
    Path("THIRD_PARTY_NOTICES.md"),
    Path("ACKNOWLEDGEMENTS.md"),
    Path("README.md"),
    Path("README.en.md"),
    Path("LICENSES/Sarasa-Gothic-OFL.txt"),
    Path("LICENSES/Hack-LICENSE.md"),
)

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


def add_file(zf: zipfile.ZipFile, source: Path, archive_name: str) -> None:
    info = zipfile.ZipInfo(archive_name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, source.read_bytes())


def write_archive(
    archive_path: Path,
    root_name: str,
    fonts: list[Path],
    repo_root: Path,
) -> None:
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for font in sorted(fonts, key=lambda p: p.name):
            add_file(zf, font, f"{root_name}/{font.name}")
        for relative in COMMON_FILES:
            source = repo_root / relative
            if not source.is_file():
                raise FileNotFoundError(source)
            add_file(zf, source, f"{root_name}/{relative.as_posix()}")


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

    targets = (
        ("Mono", mono),
        ("Term", term),
    )
    archives = []
    for variant, fonts in targets:
        root_name = f"Sarack-{variant}-v{args.version}"
        archive_path = output_dir / f"{root_name}.zip"
        write_archive(archive_path, root_name, fonts, repo_root)
        archives.append(archive_path)
        print(f"Created {archive_path}")

    checksums = output_dir / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in archives),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Created {checksums}")


if __name__ == "__main__":
    main()
