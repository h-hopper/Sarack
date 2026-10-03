# 紗絡 / Sarack Releaseチェックリスト

公開先は `h-hopper/Sarack`。Releaseごとに、その対象commitから候補を生成し、CIと実物監査を通過してから公開する。日本語READMEを主文書とし、英語READMEは利用者向けの簡潔な案内とする。

## 1. Versionと公開方針

- 正式版 `vX.Y.Z` は通常のGitHub Releaseとし、Draft / Pre-releaseはOFF
- `v0.x` であること自体はPre-releaseと同義ではない
- 外部検証が必要なRC / betaは `vX.Y.Z-rc.1` 等の別tagでPre-releaseとして公開可能
- 正式版は別tagで作成し、同じtagをPre-releaseから通常Releaseへ昇格させる運用は原則行わない
- 開発版の `-dev` を正式Releaseへ混入させない
- 公開済みtagを移動せず、公開assetを差し替えない。修正は新versionとして公開する

## 2. Build・source lock

- Release対象commitとmain、候補runのhead SHAを記録する
- `.github/workflows/release-package.yml` を対象commitのmainから実行し、`version` に `X.Y.Z` を明示する
- 固定されたSarasa / Hack入力とSHA-256が `sources.lock` に一致
- `PENDING` 等の未確定値なし、Hack取得元は固定commit
- README / docsの上流versionとsource lockが一致
- Python依存versionとActionsのcommit SHA固定を維持
- Mono / Mono HS / Term / Term HSを各4スタイル、計16 TTF生成
- PRではbuild / validationを維持し、artifact uploadは行わない
- dispatch時だけartifact upload、retentionは3日。正式候補は開発artifactと区別する

## 3. Font metadata・自動検証

全16 TTFについて次を確認する。

- familyが `Sarack Mono` / `Sarack Mono HS` / `Sarack Term` / `Sarack Term HS` に分離
- Regular / Bold / Italic / Bold Italicのstyle linkingが正常
- weight 400 / 700、Bold / Italic bitsが正しい
- PostScript nameが一貫し、name ID 3がfamily / style / versionごとに衝突しない
- name ID 5がRelease version、`head.fontRevision` がversion方針に一致
- name ID 0にSarack改変著作権と必要な上流権利表示を保持
- name ID 13 / 14はOFL 1.1のdescription / URL
- Reserved Font Nameに抵触するprimary family nameを使わない
- Basic Latinは500、日本語/CJKは1000、半角:全角=1:2
- U+3000は1000幅、標準版は可視、HSは不可視・輪郭なし
- U+2014はMono / Mono HS=1000、Term / Term HS=500（全styles）
- Unhinted: `cvt ` / `fpgm` / `prep` が存在しない
- 保存後に再openしたTTFでもbuilder validationを通過

現行配布はUnhinted。Regularの `ttfautohint 1.8.4` A/B評価では12～13 pxの改善が小さく、14 px以上の差とサイズ増加を考慮して不採用とした。再検討時はgeometry / spacing / metadataを維持し、Windowsで12～16 px程度の表示を再確認する。

## 4. 実表示

VS Code editor / integrated terminal、Windows Terminal、PowerShell 7 / SSH、PuTTYで確認する。

- `0 O o Q` / `1 I l |` / 引用符 / 句読点
- 日本語とLatin混在、半角・全角の桁揃え、U+3000
- 全4 stylesとMono / Termの矢印・幾何学記号・ダッシュのspacing差
- 同時インストール時の4 family分離とstyle linking
- PuTTYのTerm設定は `UTF-8`（`UTF-8 (CJK)` ではない）
- README見本画像は実Sarack TTFからレンダリングし、clipping / tofuを確認

## 5. License・package

`LICENSE-CODE` はrepository独自コード / build・package toolingのMIT License、`LICENSE-FONT` は生成SarackフォントのSIL OFL 1.1。MITは生成fontには適用せず、上流fontをMITへ再ライセンスするものではない。

各binary ZIPはvariant/versionの単一rootと、次の**9ファイルのみ**を持つ。

- Mono: Mono / Mono HS × 4 stylesの8 TTF
- Term: Term / Term HS × 4 stylesの8 TTF
- 共通: `LICENSES.txt` 1本

`package_release.py` は次の正本全文を、見出しとseparator付きで連結する。改行のみ決定的に正規化し、本文を要約・改変しない。

1. `LICENSE-FONT`
2. `LICENSES/Sarasa-Gothic-OFL.txt`
3. `LICENSES/Hack-LICENSE.md`

確認事項:

- Mono / Termの `LICENSES.txt` はbyte-identical
- OFL全文、Sarasa著作権、Adobe / Sourceのnotice、Hack著作権、MIT、Bitstream Vera本文が欠落しない
- ZIPにはREADME、ACKNOWLEDGEMENTS、独立THIRD_PARTY_NOTICES、LICENSES directory、source / tooling / cacheを入れない
- `LICENSE-CODE` はsource repoに保持し、binary-only ZIPには不要
- HackGenはengineering referenceでありbinary dependencyではない。repoのACKNOWLEDGEMENTS / THIRD_PARTY_NOTICESで由来を保持
- TTFの権利表示・license metadataとlicense bundleが矛盾しない
- ZIP内の重複、余計なentry、複数rootなし。固定timestamp / entry順とCRCが正常

## 6. Candidate実物監査

正式候補artifactの内側の3ファイルを取得する。

```text
Sarack-Mono-vX.Y.Z.zip
Sarack-Term-vX.Y.Z.zip
SHA256SUMS.txt
```

- 2 ZIPのSHA-256を独立再計算し、SHA256SUMSと一致
- 各ZIPが8 TTF + LICENSES.txtのみであることを実物から確認
- LICENSES.txtを正本全文と照合
- 全16 TTFのmetadata / width / U+3000 / U+2014 / Unhintedを確認
- 設計変更なしのReleaseでは前versionとglyph / cmap / metrics / OpenType tablesを比較
- artifact ID、run ID、対象SHA、hash、失効時刻を記録。再buildした別物に置き換えない

## 7. 公開

- 公開前にrepoがPublic、default branch=main、対象SHA・tag未存在を確認
- PR経由の変更とmain保護、Actions read権限、fork PR設定を維持
- target commitに新tagを作成し、正式ReleaseのDraft / Pre-releaseをOFFにする
- 日本語主体のRelease notesに変更内容・配布物・font licenseを記載
- 添付は2 ZIPとSHA256SUMSの正確に3件。Actions artifact外側ZIPやdev artifactは添付しない
- READMEのLatest Release badgeは通常Releaseを表示し、Release一覧へリンクする

## 8. 公開後

- 未認証のRelease URL / README / badge / images / linksの表示確認
- 公開Releaseから3assetを再downloadし、SHA256SUMSと期待hashを再照合
- tag targetとRelease identity、Draft / Pre-release、asset名・件数を確認
- 新規環境で4 familyのstyle linkingと同時インストールを再確認
- 次開発versionへの移行はRelease後の別PR。公開tagはRelease commitに固定

## 公開履歴

`h-hopper/Sarack` は旧Private開発repoと独立したbaselineから開始し、reviewed PRを積み上げて公開した。v0.1.0は初回正式Release。以降も履歴を書き換えず、versionごとに新tag / Releaseを作成する。
