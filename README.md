# 紗絡（Sarack）

**紗絡（Sarack）** は、Sarasa Gothic と Hack をベースにした、日本語対応のプログラミング／ターミナル向け等幅フォントです。  
**Sarack** is a Japanese-capable monospace font for programming and terminal use, based on Sarasa Gothic and Hack.

[English](README.en.md)

[![Build](https://github.com/h-hopper/Sarack/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/h-hopper/Sarack/actions/workflows/build.yml)
<!-- 初回 GitHub Release 公開後に有効化
[![Latest Release](https://img.shields.io/github/v/release/h-hopper/Sarack)](https://github.com/h-hopper/Sarack/releases)
-->
[![Font License: OFL-1.1](https://img.shields.io/badge/font%20license-OFL--1.1-blue.svg)](LICENSE-FONT)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://github.com/h-hopper/Sarack/blob/main/LICENSE-CODE)

日本語ブランド名の **「紗絡」** は、異なる書体を「紗」のように織り、「絡」めて一つにするイメージから付けた造語です。`Sarack` という名称も、主要な書体ソースである Sarasa Gothic と Hack に由来します。

## 特徴

- **日本語/CJK:** Sarasa Gothic系のシャープな字形を維持
- **英数字:** Hack をベースに、日本語との視覚バランスを調整
- **半角 : 全角 = 1 : 2:** コードやターミナルでの桁揃えを重視
- **中央点付き `0`:** `O` / `o` との識別性を重視
- **全角スペースを可視化:** 標準版では U+3000 を可視化
- **Hidden Space版:** `HS` familyでは U+3000 を不可視化
- **Mono / Term spacing:** 用途に応じて非ASCII記号のセル幅設計を選択可能
- **4スタイル:** Regular / Bold / Italic / Bold Italic
- **独立ビルド:** Sarasa Gothic のforkやソースツリーに依存せず再生成可能

具体的な拡大率、記号補正値、OpenType feature の扱いなどは [設計仕様](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md) に分離しています。

## バリアント

`Mono` と `Term` は、利用アプリそのものではなく **spacing（文字幅）設計の違い**を表します。Basic Latin と通常の日本語字形は共通し、`Term` は Sarasa Term J 由来の設計を維持して、矢印・幾何学記号など多くの非ASCII記号を一般的なターミナル利用に合わせて狭く扱います。

| Variant | U+3000 | 主な用途 |
| --- | --- | --- |
| `Sarack Mono` | 可視 | 一般的なプログラミング、エディタ |
| `Sarack Mono HS` | 不可視 | Mono版で全角スペースをフォント側表示したくない場合 |
| `Sarack Term` | 可視 | ターミナルで記号を1セル幅中心に扱いたい場合 |
| `Sarack Term HS` | 不可視 | Term版のHidden Space variant |

`HS` は **Hidden Space** を表します。標準の `Sarack Mono` / `Sarack Term` は全角スペース可視版です。

`Term` は **Nerd Font を意味しません**。現行の `Sarack Term` / `Sarack Term HS` に Nerd Fonts の追加アイコンglyphは含まれていません。

### PuTTYでの設定

`Sarack Term` / `Sarack Term HS` をPuTTYで使用する場合、**Window > Translation > Remote character set** は `UTF-8` を選択してください。`UTF-8 (CJK)` では East Asian Ambiguous 扱いの矢印・幾何学記号などをPuTTYが2セルとして処理し、1セル幅のTerm glyphと衝突して桁がずれます。

## 入手

配布物の入手先は [GitHub Releases](https://github.com/h-hopper/Sarack/releases) です。`v0.1.0` は初回正式Releaseで、4ファミリー × 4スタイル、計16本の **Unhinted TTF** を収録します。

- `Sarack-Mono-v0.1.0.zip` — Mono / Mono HS 各4スタイル（8 TTF）
- `Sarack-Term-v0.1.0.zip` — Term / Term HS 各4スタイル（8 TTF）
- `SHA256SUMS.txt` — 2つのZIPのSHA-256

公開されたZIPを展開し、使用するファミリーのTTFをOSへインストールして、アプリのフォント設定で選択してください。各ファミリーには Regular / Bold / Italic / Bold Italic が含まれます。

GitHub Actionsの開発用artifact（`0.1.0-dev`）は配布用Release packageと区別してください。

## ビルド

現行ビルドは、固定した完成済み TTF を `fontTools` で後処理する方式です。

使用している主な入力:

- **Sarasa Mono J 1.0.41 Unhinted TTF** — Mono版の日本語/CJK字形、基本メトリクス、OpenType table のベース
- **Sarasa Term J 1.0.41 Unhinted TTF** — Term版の日本語/CJK字形、基本メトリクス、OpenType table のベース
- **Hack 3.003** — Basic Latin 字形

`v0.1.0` の配布TTFは **Unhinted** です。Regularで `ttfautohint 1.8.4` を用いたA/B評価では、12～13 pxで僅かな改善は見られたものの14 px以上では差が小さく、配布サイズ増加との釣り合いから採用を見送りました。評価結果と判断理由は [設計仕様](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md) に記録しています。

標準Mono版は既定動作で `Sarack Mono` を生成し、`--hidden-space` を指定すると `Sarack Mono HS` を生成します。Term版はSarasa Term Jをbaseにし、family名を `Sarack Term` / `Sarack Term HS` として生成します。ローカルでの再生成手順、対応スタイル、GitHub Actions の動作は [ビルド手順](https://github.com/h-hopper/Sarack/blob/main/docs/BUILD.md) を参照してください。

## ドキュメント

- [設計仕様](https://github.com/h-hopper/Sarack/blob/main/docs/DESIGN.md) — 字形構成、具体的な補正値、設計方針
- [ビルド手順](https://github.com/h-hopper/Sarack/blob/main/docs/BUILD.md) — 再現ビルド、入力バージョン、CI
- [公開・Releaseチェックリスト](https://github.com/h-hopper/Sarack/blob/main/docs/RELEASE.md) — Public化・配布前の確認事項
- [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) — 上流プロジェクトとengineering referenceの由来
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — 第三者ライセンス・配布時通知

## 上流プロジェクトと謝辞

紗絡 / Sarack は主に次のオープンソースフォントを利用しています。

- **Sarasa Gothic / Sarasa Mono J / Sarasa Term J** — 日本語/CJKとbase font
- **Hack** — Basic Latin

**HackGen / 白源** のフォントバイナリは使用していませんが、Latin/CJKのサイズ設計や一部記号補正について、公開されている生成方式・値を engineering reference として参照しています。詳細は [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) を参照してください。

## ライセンス

コンポーネントごとにライセンスを分けています。

- **生成される Sarack フォント:** [SIL Open Font License 1.1](LICENSE-FONT)
- **このリポジトリの独自コード（ビルド・パッケージングツール等）:** [MIT License](https://github.com/h-hopper/Sarack/blob/main/LICENSE-CODE)

MIT Licenseは、このリポジトリで独自に作成したコード・ツールへ適用し、再利用・改変しやすい形で公開するために採用しています。生成されるSarackフォントには適用せず、上流フォントソフトウェアをMITへ再ライセンスするものではありません。

Sarasa Gothic / Source Han Sans、Hack / Bitstream Vera などの上流ライセンス原文は `LICENSES/` に保持しています。

## AI支援による開発

Sarack は **OpenAIのChatGPTによる大幅な開発支援**を受けています。調査、ビルドツール実装、自動検証、開発フロー整備などにAIを利用しています。

フォントとしての設計判断、採否、実際の表示確認と評価はプロジェクト管理者が行っています。この記載は開発経緯の透明性を目的とするもので、上流フォントのライセンスや権利表示を置き換えるものではありません。

## 今後の予定

- 必要性が確認できた場合のみ Nerd Font variant を検討
- 利用環境に応じた表示例・スクリーンショットの充実
