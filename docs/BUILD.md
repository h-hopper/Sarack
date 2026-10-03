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

開発版の既定versionは `0.2.0-dev` です。別versionを生成する場合は `--version` を明示します。

```bash
python build.py ... --version 0.2.0-dev
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
- workflow_dispatch時だけMono / Termを別々のdevelopment artifactとしてアップロード（retention 3日）。PRではuploadせず、superseded PR runをcancelする

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

正式配布候補は `.github/workflows/release-package.yml` で生成します。`workflow_dispatch` の `version` に `X.Y.Z` を明示し、Release用versionで16 TTFを再生成します。PRでも同じbuild / validationを実施しますが、artifactはuploadしません。

Release候補の出力:

```text
Sarack-Mono-vX.Y.Z.zip
Sarack-Term-vX.Y.Z.zip
SHA256SUMS.txt
```

Mono ZIPはMono / Mono HS各4 styles、Term ZIPはTerm / Term HS各4 stylesの**8 TTFとLICENSES.txtのみ**を収録します。variant/version名の単一root directoryとし、README・ACKNOWLEDGEMENTS・独立THIRD_PARTY_NOTICES・LICENSES directoryは入れません。

`LICENSES.txt` は `LICENSE-FONT`、`LICENSES/Sarasa-Gothic-OFL.txt`、`LICENSES/Hack-LICENSE.md` の全文をseparator付きで連結します。改行のみ正規化し、必要な権利表示・license本文を維持します。両ZIPのLICENSES.txtはbyte-identicalです。独自source / toolingを同梱しないので、`LICENSE-CODE` はsource repoにのみ保持します。

`package_release.py` は全16 TTFのfamily / Release version / OFL metadata / 500・1000幅 / U+3000 / Mono・Term U+2014 / Unhintedを再検証します。ZIPの正確な9ファイル、license text、CRC、固定timestampとentry順も検証します。SHA256SUMSには2 ZIPのSHA-256を記録し、workflow内で再照合します。

候補を公開する前には、artifact実物のTTF・package構成・license全文とSHAを監査します。Actions development artifactは正式Releaseとは別です。

## 上流更新

上流versionを変更する場合は `sources.lock` のURL・version・SHA-256を同時に更新し、新しい入力でMono / Termの全16 TTFを再生成して確認します。

公開Releaseの要件は [RELEASE.md](RELEASE.md) を参照してください。
