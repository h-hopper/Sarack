"""Regression checks for the binary-only package and public documentation."""
import re
import struct
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

import package_release as package

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.fonts = []
        for name in package.MONO_FILES:
            path = self.base / name
            path.write_bytes(b"test font payload")
            self.fonts.append(path)
        self.licenses = package.license_bundle(ROOT)
        self.root = "Sarack-Mono-v0.1.1"
        self.archive = self.base / (self.root + ".zip")
        package.write_archive(self.archive, self.root, self.fonts, self.licenses)

    def test_full_license_sources_preserved(self):
        for source in package.LICENSE_SOURCES:
            text = (ROOT / source).read_bytes().decode("utf-8")
            normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
            self.assertIn(normalized, self.licenses)

    def test_exact_nine_files_and_deterministic_bytes(self):
        package.validate_archive(self.archive, self.root, package.MONO_FILES, self.licenses)
        second = self.base / "second.zip"
        package.write_archive(second, self.root, list(reversed(self.fonts)), self.licenses)
        self.assertEqual(self.archive.read_bytes(), second.read_bytes())

    def test_extra_readme_rejected(self):
        with zipfile.ZipFile(self.archive, "a") as archive:
            archive.writestr(self.root + "/README.md", "not a binary asset")
        with self.assertRaises(RuntimeError):
            package.validate_archive(self.archive, self.root, package.MONO_FILES, self.licenses)

    def test_duplicate_entry_rejected(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.archive, "a") as archive:
                archive.writestr(self.root + "/LICENSES.txt", self.licenses)
        with self.assertRaises(RuntimeError):
            package.validate_archive(self.archive, self.root, package.MONO_FILES, self.licenses)

    def test_changed_license_rejected(self):
        package.write_archive(self.archive, self.root, self.fonts, b"abridged license")
        with self.assertRaises(RuntimeError):
            package.validate_archive(self.archive, self.root, package.MONO_FILES, self.licenses)

    def test_missing_font_rejected(self):
        package.write_archive(self.archive, self.root, self.fonts[:-1], self.licenses)
        with self.assertRaises(RuntimeError):
            package.validate_archive(self.archive, self.root, package.MONO_FILES, self.licenses)

    def test_missing_notice_rejected(self):
        for source in package.LICENSE_SOURCES:
            destination = self.base / source
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / source).read_bytes())
        (self.base / "LICENSE-FONT").write_text("incomplete license", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            package.license_bundle(self.base)


class DocumentationTests(unittest.TestCase):
    def test_repository_links_resolve(self):
        for path in [ROOT / "README.md", ROOT / "README.en.md", *sorted((ROOT / "docs").glob("*.md"))]:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("```") % 2, 0, str(path))
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith("https://github.com/h-hopper/Sarack/blob/main/"):
                    target = ROOT / link.split("/blob/main/", 1)[1].split("#")[0]
                elif not re.match(r"[a-z]+:", link) and not link.startswith("#"):
                    target = path.parent / link.split("#")[0]
                else:
                    continue
                self.assertTrue(target.resolve().is_relative_to(ROOT), link)
                self.assertTrue(target.is_file(), f"{path.name}: {link}")

    def test_specimen_pngs_exist(self):
        for name in ("sarack-specimen.png", "sarack-variants.png"):
            data = (ROOT / "docs/images" / name).read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            self.assertGreater(width, 0)
            self.assertGreater(height, 0)


if __name__ == "__main__":
    unittest.main()
