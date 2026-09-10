# Sarack

**Sarack** is a Japanese-capable monospace font for programming and terminal use, based on Sarasa Gothic and Hack.

[日本語](README.md)

[![Build](https://github.com/h-hopper/Sarack/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/h-hopper/Sarack/actions/workflows/build.yml)
<!-- Enable after the first GitHub Release is published
[![Latest Release](https://img.shields.io/github/v/release/h-hopper/Sarack?include_prereleases)](https://github.com/h-hopper/Sarack/releases)
-->
[![Font License: OFL-1.1](https://img.shields.io/badge/font%20license-OFL--1.1-blue.svg)](LICENSE-FONT)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://github.com/h-hopper/Sarack/blob/main/LICENSE-CODE)

The Japanese brand name **紗絡** is a coined name expressing the idea of weaving and combining different typefaces. `Sarack` is also derived from the project's two main typeface sources: Sarasa Gothic and Hack.

## Features

- **Japanese/CJK:** retains the sharp Sarasa Gothic-family glyph design
- **Latin:** based on Hack, optically balanced against Japanese text
- **Strict 1:2 cells:** half-width : full-width = 1 : 2
- **Dotted zero:** designed for clear distinction from `O` / `o`
- **Visible ideographic space:** standard families render U+3000 visibly
- **Hidden Space families:** `HS` families keep U+3000 invisible
- **Mono / Term spacing:** choose non-ASCII symbol spacing appropriate to the target environment
- **Four styles:** Regular / Bold / Italic / Bold Italic
- **Standalone build:** does not require a Sarasa Gothic fork or source-tree checkout

Exact scale factors, punctuation corrections, and OpenType feature handling are documented in [DESIGN.md](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md).

## Variants

`Mono` and `Term` describe **spacing behavior**, not a hard application boundary. Both share the same Hack-derived Basic Latin and normal Japanese glyph design. `Term` retains Sarasa Term J spacing behavior, making many non-ASCII symbols such as arrows and geometric symbols narrow for common terminal usage.

| Variant | U+3000 | Intended use |
| --- | --- | --- |
| `Sarack Mono` | Visible | General programming and editors |
| `Sarack Mono HS` | Hidden | Mono variant without a font-level ideographic-space marker |
| `Sarack Term` | Visible | Terminals where narrow one-cell symbol spacing is preferred |
| `Sarack Term HS` | Hidden | Hidden Space variant of the Term family |

`HS` means **Hidden Space**. The standard `Sarack Mono` / `Sarack Term` families are the visible-space variants.

`Term` does **not** mean Nerd Font. The current `Sarack Term` / `Sarack Term HS` families do not include additional Nerd Fonts icon glyphs.

### PuTTY configuration

When using `Sarack Term` / `Sarack Term HS` in PuTTY, set **Window > Translation > Remote character set** to `UTF-8`. Do not use `UTF-8 (CJK)`: PuTTY then treats East Asian Ambiguous characters such as arrows and geometric symbols as two cells, conflicting with the one-cell Term glyph spacing and causing column misalignment.

## Availability

Release packages are distributed through [GitHub Releases](https://github.com/h-hopper/Sarack/releases). `v0.1.0` is a **Pre-release** containing four families with four styles each, for a total of 16 **Unhinted TTFs**.

- `Sarack-Mono-v0.1.0.zip` — four styles each for Mono / Mono HS (8 TTFs)
- `Sarack-Term-v0.1.0.zip` — four styles each for Term / Term HS (8 TTFs)
- `SHA256SUMS.txt` — SHA-256 checksums for both ZIPs

Extract a published ZIP, install the TTFs for the families you want in your OS, and select the family in your application's font settings. Each family includes Regular / Bold / Italic / Bold Italic.

GitHub Actions development artifacts (`0.1.0-dev`) are separate from release packages.

## Build

The current build post-processes pinned finished TTF inputs with `fontTools`.

Primary inputs:

- **Sarasa Mono J 1.0.41 Unhinted TTF** — Japanese/CJK outlines, base metrics, and OpenType tables for the Mono families
- **Sarasa Term J 1.0.41 Unhinted TTF** — Japanese/CJK outlines, base metrics, and OpenType tables for the Term families
- **Hack 3.003** — Basic Latin outlines

The `v0.1.0` release TTFs are **Unhinted**. A Regular-only A/B evaluation with `ttfautohint 1.8.4` showed only a slight improvement at 12–13 px and little practical difference at 14 px and above, while increasing file size substantially. The evaluation result and rationale are recorded in [DESIGN.md](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md).

The default build produces `Sarack Mono`; passing `--hidden-space` produces `Sarack Mono HS`. Term builds use Sarasa Term J as the base and explicit `Sarack Term` / `Sarack Term HS` family names. See [BUILD.md](https://github.com/h-hopper/Sarack/blob/main/docs/BUILD.md) for local reproduction, supported styles, and CI details.

## Documentation

- [DESIGN.md](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md) — glyph architecture, exact tuning values, and design policy
- [BUILD.md](https://github.com/h-hopper/Sarack/blob/main/docs/BUILD.md) — reproducible build process and CI
- [RELEASE.md](https://github.com/h-hopper/Sarack/blob/main/docs/RELEASE.md) — pre-publication and release checklist
- [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) — upstream projects and engineering references
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — third-party licensing and release notices

## Upstream projects and acknowledgements

Sarack primarily uses:

- **Sarasa Gothic / Sarasa Mono J / Sarasa Term J** — Japanese/CJK and base fonts
- **Hack** — Basic Latin

**HackGen / 白源** font binaries are not incorporated. Its published generator approach and selected values were consulted as an engineering reference for Latin/CJK sizing and selected symbol tuning. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for details.

## Licensing

Licensing is separated by component:

- **Generated Sarack fonts:** [SIL Open Font License 1.1](LICENSE-FONT)
- **Project-authored build tooling:** [MIT License](https://github.com/h-hopper/Sarack/blob/main/LICENSE-CODE)

Verbatim upstream license texts for Sarasa Gothic / Source Han Sans and Hack / Bitstream Vera are retained under `LICENSES/`.

## AI-assisted development

Sarack has been developed with substantial assistance from **ChatGPT by OpenAI**, including research, build-tool implementation, automated validation, and development-workflow support.

Font-design decisions, acceptance decisions, and real rendered-output evaluation are directed and reviewed by the project maintainer. This disclosure describes the development process and does not replace any upstream license or attribution requirement.

## Roadmap

- consider a Nerd Font variant only if a concrete need is confirmed
- expand rendered examples and screenshots for different environments
