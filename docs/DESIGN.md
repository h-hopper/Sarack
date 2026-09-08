# 紗絡 / Sarack 設計仕様

この文書は、Sarack の字形構成、メトリクス、補正値、および恒久的な設計方針を記録します。

利用方法は `README.md`、再現ビルドは `docs/BUILD.md`、公開前の検証項目は `docs/RELEASE.md` を参照してください。

## 設計方針

Sarack は、日本語と英数字が混在するコード表示で次を重視します。

- Sarasa Gothic 系の日本語字形
- Hack 系の欧文字形
- 半角 : 全角 = **1 : 2** のセル幅
- `0` / `O` / `o` など紛らわしい字形の識別性
- 日本語と欧文の視覚的な大きさ・太さのバランス
- Mono / Termそれぞれのspacing用途に適したSarasaの幅設計を維持すること

## フォント構成

完成済み TTF を `fontTools` で後処理して生成します。

- Mono familyのCJK、基本メトリクス、OpenType table: **Sarasa Mono J 1.0.41 Unhinted TTF**
- Term familyのCJK、基本メトリクス、OpenType table: **Sarasa Term J 1.0.41 Unhinted TTF**
- Basic Latin U+0020..U+007E: **Hack 3.003**
- 後処理: **fontTools 4.63.0**

Sarasa Gothic のソースツリーや内部 build helper には依存しません。

### スタイル対応

| Sarack style | Mono base | Term base | Basic Latin donor |
| --- | --- | --- | --- |
| Regular | Sarasa Mono J Regular | Sarasa Term J Regular | Hack Regular |
| Bold | Sarasa Mono J Bold | Sarasa Term J Bold | Hack Bold |
| Italic | Sarasa Mono J Italic | Sarasa Term J Italic | Hack Italic |
| Bold Italic | Sarasa Mono J Bold Italic | Sarasa Term J Bold Italic | Hack Bold Italic |

Italic / Bold Italic のCJKには、それぞれ対応するSarasaのItalic / Bold Italicを使用します。

## メトリクス

Basic Latinと通常の全角文字について次を固定します。

```text
half width = 500
full width = 1000
ratio      = 1 : 2
```

Basic Latin の字形を補正しても advance width は 500 のまま維持します。U+3000 IDEOGRAPHIC SPACE の advance width は 1000 とします。

Term familyでは、Basic Latin以外についてSarasa Term Jのterminal向け幅設計を維持します。代表例としてU+2014 EM DASHは、Mono baseのSarasa Mono Jでは全角、Term baseのSarasa Term Jでは半角です。矢印・幾何学記号などにもMono / Term間のspacing差があります。

`Term` はNerd Fontを意味しません。Nerd Fonts由来の追加アイコンglyphは現行familyには含めません。

## Basic Latin のフィッティング

Hack の字形を Sarasa の半角セルへ合わせる際、HackGen の公開 generator に由来する次の値を engineering reference として使用します。

```text
reference em         = 1024
reference half width = 540
X scale              = 0.88
Y scale              = 0.97
```

Sarasa の half width 500 / UPM 1000 に対する基準 X scale は次の換算です。

```text
0.88 × (500 / 540) × (1024 / 1000) ≈ 0.83437
```

さらに日本語との視覚バランスを合わせるため、セル幅を変えず Latin geometry を補正します。

```text
LATIN_VISUAL_SCALE       = 1.03
LATIN_VISUAL_CENTER_Y_EM = 0.35
```

Mono / Termで同じBasic Latin補正値を使用します。

## `0` の中央点

Hack の dotted zero をベースに、中央点の形状を次の値へ補正します。

```text
ZERO_DOT_SIZE = 120
```

- 目標サイズ: 120 × 120 font units
- X位置: 半角セル中央
- Y位置: `0` 外形の上下中央

## 引用符・句読点

日本語と混在した際の視覚バランスを合わせるため、対象記号を選択的に補正します。

### 引用符

対象:

- U+0022 `"`
- U+0027 `'`
- U+0060 `` ` ``

```text
QUOTE_SCALE = 1.10
```

### 句読点

対象:

- U+002E `.`
- U+002C `,`
- U+003A `:`
- U+003B `;`

```text
PUNCT_SCALE = 1.08
```

縦位置補正には HackGen の generator 値を engineering reference として使用し、base UPM に比例換算して適用します。

```text
;  +18
.   +5
,   -8
```

上記値は reference UPM 1024 に対する値です。

## U+3000 IDEOGRAPHIC SPACE

標準 family `Sarack Mono` / `Sarack Term` では、U+3000 に可視マーカーを持たせます。

```text
IDEOGRAPHIC_SPACE_DOT_SIZE = 60
```

マーカーは各Sarasa baseの U+00B7 MIDDLE DOT の輪郭を縮小・複製して構成し、advance width 1000 を維持します。

全角スペースを不可視にする派生 family は `Sarack Mono HS` / `Sarack Term HS` とします。`HS` は **Hidden Space** を表し、U+3000 の advance width 1000 は維持したまま輪郭を持たせません。

## OpenType feature

Basic Latin を Hack に置換した後、Sarasa / Iosevka 側の Latin alternate が Hack の字形を置換しないよう、次の feature を除去します。

```text
liga
clig
dlig
calt
zero
cv01..cv99
ss01..ss20
```

CJK に必要な `locl`、`vert` 等は維持します。

## CJK 字形

日本語/CJK は、対応する Sarasa Mono J / Sarasa Term J の字形を原則として変更しません。

HackGen に含まれる日本語向け独自字形調整は取り込まず、Sarasaの字形方針を維持します。

## バリアント

### Mono

- `Sarack Mono`: Sarasa Mono J base、U+3000 可視
- `Sarack Mono HS`: Sarasa Mono J base、U+3000 不可視

### Term

- `Sarack Term`: Sarasa Term J base、U+3000 可視
- `Sarack Term HS`: Sarasa Term J base、U+3000 不可視

Mono / TermはBasic Latinの字形補正を共有し、Basic Latin以外ではそれぞれのSarasa baseが持つ幅設計を維持します。両者は利用アプリを固定する区分ではなく、spacing設計の違いです。

### Hinting

初回 public release は **Unhinted** を標準とします。

2026-09-04に `Sarack Mono Regular` / `Sarack Term Regular` を対象として、最終生成TTFへ `ttfautohint 1.8.4 --no-info` を後処理するA/B評価を実施しました。機械検証では全glyphのadvance width・outline geometry、U+3000、family/style/version metadata、`head.fontRevision`、Mono/Term spacing semanticsが不変であることを確認しました。

Windowsで12 / 13 / 14 / 16 pxを比較した結果、12～13 pxではHinted版がわずかに締まって見えるものの差は小さく、14 pxではほぼ互角、16 pxでは実用上ほぼ同等でした。日本語側に目立つ改善・悪化は確認されませんでした。一方、RegularのTTFサイズはHinting後に約1.86倍となりました。

このため、初回ReleaseではHintingによる小サイズ表示の軽微な改善よりも、生成工程・依存関係・配布サイズを増やさないことを優先し、Unhintedを採用します。将来、対象環境や描画条件の変化により具体的な必要性が生じた場合は再評価できます。

### Nerd Font

追加 glyph が必要な用途に限り、Mono / Term の基本 family と分離した variant として扱います。

## HackGen の位置づけ

HackGen / 白源のフォントバイナリは使用しません。

サイズ比や一部記号補正など、公開された generator の考え方・具体値を engineering reference として参照しています。出典とライセンス上の扱いは `ACKNOWLEDGEMENTS.md` および `THIRD_PARTY_NOTICES.md` に記載します。
