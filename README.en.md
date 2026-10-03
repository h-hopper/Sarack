# Sarack

**Sarack (紗絡)** is a Japanese monospace font for programming and terminals, combining Sarasa Gothic and Hack. Four families with four styles each provide **16 Unhinted TTFs**, with strict half/full-width metrics of **500/1000**.

[日本語README](README.md)

[![Build](https://github.com/h-hopper/Sarack/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/h-hopper/Sarack/actions/workflows/build.yml)
[![Latest Release](https://img.shields.io/github/v/release/h-hopper/Sarack)](https://github.com/h-hopper/Sarack/releases)

## Variants

| Family | U+3000 space | Use |
| --- | --- | --- |
| Sarack Mono | Visible | Editors and programming |
| Sarack Mono HS | Hidden | Mono with invisible ideographic spaces |
| Sarack Term | Visible | Terminal spacing for non-ASCII symbols |
| Sarack Term HS | Hidden | Term with invisible ideographic spaces |

Each family includes Regular, Bold, Italic, and Bold Italic. **HS** means Hidden Space. Mono/Term differ in spacing design; Term does not include Nerd Fonts icons. In PuTTY, select `UTF-8`, rather than `UTF-8 (CJK)`, for Term families.

## Download

Get the latest version from [GitHub Releases](https://github.com/h-hopper/Sarack/releases):

- `Sarack-Mono-vX.Y.Z.zip` — 8 TTFs
- `Sarack-Term-vX.Y.Z.zip` — 8 TTFs
- `SHA256SUMS.txt` — ZIP checksums

Each ZIP contains fonts and the complete combined license text, `LICENSES.txt`. Extract the ZIP, install the desired TTFs, and select the family in your application.

## License

- Generated fonts: [SIL OFL 1.1](LICENSE-FONT).
- Repository-authored code, including build/packaging tools: [MIT](LICENSE-CODE), for easy reuse and modification. MIT does not apply to generated fonts or relicense upstream font software.

## Documentation

Full documentation, specimens, provenance, and acknowledgements are maintained primarily in Japanese. See the [日本語README](README.md).
