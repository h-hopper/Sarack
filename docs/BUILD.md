# 紗絡 / Sarack ビルド手順

この文書は、Sarack をローカルまたは GitHub Actions で再生成するための手順をまとめます。

## 前提

現行ビルドは完成済み TTF を `fontTools` で後処理する方式です。Sarasa Gothic のソースツリーは不要です。

主な入力:

- Sarasa Mono J 1.0.41 Unhinted TTF — Mono family base
- Sarasa Term J 1.0.41 Unhinted TTF — Term family base
- Hack 3.003 TTF
- fontTools 4.63.0

上流フォントの取得URL、version、SHA-256は [`sources.lock`](../sources.lock) を正本とします。Hack は v3.003 の immutable commit をURLに使用し、4スタイルそれぞれのSHA-256も検証します。

## 必要環境

- Python 3.13
- `pip`
- `fontTools==4.63.0`
- 7-Zip等（Sarasa配布archiveの展開用）

依存パッケージ:

```bash
pip install -r requirements.txt
```

## 入力フォント

| Style | Mono base | Term base | Hack |
| --- | --- | --- | --- |
| Regular | SarasaMonoJ-Regular.ttf | SarasaTermJ-Regular.ttf | Hack-Regular.ttf |
| Bold | SarasaMonoJ-Bold.ttf | SarasaTermJ-Bold.ttf | Hack-Bold.ttf |
| Italic | SarasaMonoJ-Italic.ttf | SarasaTermJ-Italic.ttf | Hack-Italic.ttf |
| Bold Italic | SarasaMonoJ-BoldItalic.ttf | SarasaTermJ-BoldItalic.ttf | Hack-BoldItalic.ttf |

## 単体ビルド

Mono標準版 `Sarack Mono` の Regular:

```bash
python build.py \
  --sarasa SarasaMonoJ-Regular.ttf \
  --hack Hack-Regular.ttf \
  --style Regular \
  --output out/SarackMono-Regular.ttf
```

Mono Hidden Space版 `Sarack Mono HS` の Regular:

```bash
python build.py \
  --sarasa SarasaMonoJ-Regular.ttf \
  --hack Hack-Regular.ttf \
  --style Regular \
  --hidden-space \
  --output out/SarackMonoHS-Regular.ttf
```

Mono版では `--family` を省略すると、標準版は `Sarack Mono`、`--hidden-space` 指定時は `Sarack Mono HS` になります。

Term標準版 `Sarack Term` の Regular:

```bash
python build.py \
  --sarasa SarasaTermJ-Regular.ttf \
  --hack Hack-Regular.ttf \
  --style Regular \
  --family "Sarack Term" \
  --output out/SarackTerm-Regular.ttf
```

Term Hidden Space版 `Sarack Term HS` の Regular:

```bash
python build.py \
  --sarasa SarasaTermJ-Regular.ttf \
  --hack Hack-Regular.ttf \
  --style Regular \
  --family "Sarack Term HS" \
  --hidden-space \
  --output out/SarackTermHS-Regular.ttf
```

開発版の既定versionは `0.1.0-dev` です。別versionを生成する場合は `--version` を明示します。

```bash
python build.py ... --version 0.1.0-dev
```

## ビルダーが行う処理

`build.py` は次を行います。

1. 指定された Sarasa Mono J / Sarasa Term J をbaseとして読み込む
2. HackのBasic Latin U+0020..U+007Eを1:2セルへフィットして置換
3. 採用済みのLatin・`0`・引用符・句読点補正を適用
4. 標準版ではU+3000可視マーカー、HS版では輪郭のないU+3000を生成
5. Hack字形を置換し得るLatin alternate / ligature featureを除去
6. family / style / version / license等のfont metadataを設定
7. 半角/全角1:2、U+3000、style、metadataを検証
8. TTF保存後に再読込して再検証

Basic Latin以外は指定したSarasa baseを維持するため、Term版ではSarasa Term Jのterminal向け幅設計が残ります。Mono / Term はspacing variantであり、Term版でNerd Fontsのアイコンglyphを追加する処理は行いません。

具体的な字形設計値は [DESIGN.md](DESIGN.md) を参照してください。

## Font metadata

生成時に少なくとも次をSarack用に設定します。

- family / subfamily / full name / PostScript name
- Unique font identifier（name ID 3）
- Version string（name ID 5）
- OFL 1.1 license description / URL（name ID 13 / 14）
- `head.fontRevision`
- weight / Bold / Italic style linking
- Sarackの改変著作権表示と上流由来の権利表示

## GitHub Actions

`.github/workflows/build.yml` は、関連ファイルの `main` 更新、Pull Request、手動実行に対応します。

CIでは次を実行します。

- `sources.lock` から上流入力を取得
- Sarasa Mono J / Sarasa Term J archiveとHack 4 TTFのSHA-256を検証
- `Sarack Mono` / `Sarack Mono HS` を各4スタイル生成
- `Sarack Term` / `Sarack Term HS` を各4スタイル生成
- 16 TTFすべてについてbuilder内部のwidth / U+3000 / style / metadata検証を実行
- Mono / TermのU+2014 EM DASHがそれぞれ全角 / 半角であることを検証
- Mono / Termを別々のdevelopment artifactとしてアップロード

GitHub Actions自体も特定commit SHAへ固定します。versionコメントは可読性のためworkflow内に併記します。

Mono出力:

```text
SarackMono-Regular.ttf
SarackMono-Bold.ttf
SarackMono-Italic.ttf
SarackMono-BoldItalic.ttf
SarackMonoHS-Regular.ttf
SarackMonoHS-Bold.ttf
SarackMonoHS-Italic.ttf
SarackMonoHS-BoldItalic.ttf
```

Term出力:

```text
SarackTerm-Regular.ttf
SarackTerm-Bold.ttf
SarackTerm-Italic.ttf
SarackTerm-BoldItalic.ttf
SarackTermHS-Regular.ttf
SarackTermHS-Bold.ttf
SarackTermHS-Italic.ttf
SarackTermHS-BoldItalic.ttf
```

Artifact名:

```text
sarack-mono-dev
sarack-term-dev
```

開発artifactは正式Releaseではありません。

## Release package

正式配布候補は `.github/workflows/release-package.yml` で生成します。通常の開発用 `build.yml` と分離し、Release候補では `--version` を明示して16 TTFを再生成します。初回候補versionは `0.1.0` です。

Release workflowはPull Requestで検証できるほか、`workflow_dispatch` ではversionを明示して手動生成できます。上流入力の取得・SHA-256検証、16 TTFのbuilder内部検証、Mono / TermのU+2014幅検証を実施した後、`package_release.py` で配布ZIPを作成します。

初回Release候補の出力:

```text
Sarack-Mono-v0.1.0.zip
Sarack-Term-v0.1.0.zip
SHA256SUMS.txt
```

Mono ZIPには `Sarack Mono` / `Sarack Mono HS` の8 TTF、Term ZIPには `Sarack Term` / `Sarack Term HS` の8 TTFを収録します。各ZIPにはさらに次を同梱します。

```text
LICENSE-FONT
THIRD_PARTY_NOTICES.md
ACKNOWLEDGEMENTS.md
README.md
README.en.md
LICENSES/Sarasa-Gothic-OFL.txt
LICENSES/Hack-LICENSE.md
```

Binary packageにはproject-authored source/build toolingを同梱しないため、`LICENSE-CODE` はZIP内の必須ファイルにはしません。source repository側では `LICENSE-CODE` を保持します。

`package_release.py` は入力TTFのfamily、Release version、OFL metadataを再確認し、固定timestampと固定されたentry順でZIPを生成します。`SHA256SUMS.txt` には2つの配布ZIPのSHA-256を記録し、workflow内で再検証します。

Release候補を実際に配布する前には、生成artifactを展開してTTF metadata、U+3000、Mono / Term spacing、Unhinted状態、ライセンス同梱内容を実ファイルでも最終確認します。

## 上流更新

上流versionを変更する場合は `sources.lock` のURL・version・SHA-256を同時に更新し、新しい入力でMono / Termの全16 TTFを再生成して確認します。

公開Releaseの要件は [RELEASE.md](RELEASE.md) を参照してください。
