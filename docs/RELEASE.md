# 紗絡 / Sarack 公開・Release チェックリスト

この文書は、Sarack の公開用treeとGitHub Release配布物の確認事項をまとめます。公開先は `h-hopper/Sarack`、初回公開versionは `v0.1.0` です。公開前Release gateをすべて通過した後、正式な通常GitHub Releaseとして公開します。

## 1. 名称・metadata

- family 名が `Sarack Mono` / `Sarack Mono HS` / `Sarack Term` / `Sarack Term HS` で意図どおり分離されている
- 日本語ブランド表記 `紗絡` は README / 紹介文で使用し、font family metadata は英字名に統一する
- Regular / Bold / Italic / Bold Italic の style linking が正常
- weight 400 / 700 が正しい
- Italic / Bold bits が正しい
- PostScript name が一貫している
- Reserved Font Name に抵触する primary family name を使用していない
- name ID 0 に Sarack の改変著作権表示と必要な上流権利表示が保持されている
- name ID 3（Unique font identifier）が family / style / version ごとに衝突しない
- name ID 5（Version string）が Release version と一致する
- name ID 13 / 14 に OFL 1.1 の license description / URL が設定されている
- `head.fontRevision` が Release version 方針と一致する
- 開発版の `0.1.0-dev` をそのままReleaseへ持ち込まない

## 2. ビルド

- `main` の GitHub Actions が成功する
- `Sarack Mono` / `Sarack Mono HS` / `Sarack Term` / `Sarack Term HS` をそれぞれ4スタイル、合計16 TTF生成できる
- 500 / 1000 の 1:2 を CI / 実TTFで確認する
- 標準版の U+3000 が可視、HS版の U+3000 が不可視である
- Mono / Term のU+2014 EM DASHがそれぞれ全角 / 半角である
- `sources.lock` に `PENDING` 等の未確定値が残っていない
- Sarasa archive と Hack 4 TTF の SHA-256 が `sources.lock` と一致する
- Hack は固定commitから取得する
- `requirements.txt` の依存versionを固定する
- GitHub Actions依存を特定commit SHAへ固定し、workflow内コメントで対応versionを確認できる
- README / docs の上流version表記が `sources.lock` と一致する
- 正式配布候補は `.github/workflows/release-package.yml` からRelease versionを明示して生成する

## 3. 実表示

少なくとも次の環境で実表示を確認する。

- VS Code editor
- VS Code integrated terminal
- Windows Terminal
- PowerShell 7 / SSH
- PuTTY

確認対象:

- `0 O o Q`
- `1 I l |`
- 引用符 `" ' \``
- `. , : ;`
- 日本語 + Latin 混在
- U+3000 全角スペース
- Regular / Bold / Italic / Bold Italic
- 半角 / 全角の桁揃え
- `Sarack Mono` と `Sarack Mono HS` の同時インストール時に family が衝突しないこと
- `Sarack Term` と `Sarack Term HS` の同時インストール時に family が衝突しないこと
- Mono / Termで矢印・幾何学記号・ダッシュ等のspacing差が意図どおり表示されること

## 4. Hinting

- 初回 public release は **Unhinted** とする
- `ttfautohint 1.8.4` によるRegular A/B評価では、12～13 pxで僅かな改善はあったが14 px以上では差が小さく、配布サイズ増加との釣り合いから正式採用しない
- Release TTFに意図せず `cvt ` / `fpgm` / `prep` 等の自動Hinting tableを追加していないことを確認する
- 将来Hintingを再検討する場合は、advance width・outline geometry・U+3000・metadata・Mono/Term spacing semanticsを維持し、12～16 px程度のWindows表示を再確認する

## 5. ライセンス・第三者通知

`LICENSE-CODE` は、このリポジトリで独自に作成したコード・ツール（ビルド・パッケージングツール等）に適用するMIT Licenseである。`LICENSE-FONT` は、生成されるSarackフォントに適用するSIL Open Font License 1.1である。MITは生成フォントには適用せず、上流フォントソフトウェアをMITへ再ライセンスするものではない。

Release archive に少なくとも次を含める。

- `LICENSE-FONT`
- `LICENSE-CODE`（source / build tooling を同梱する場合）
- `LICENSES/Sarasa-Gothic-OFL.txt`
- `LICENSES/Hack-LICENSE.md`
- `THIRD_PARTY_NOTICES.md`
- `ACKNOWLEDGEMENTS.md`

Binary-onlyのMono / Term配布ZIPにはproject-authored source/build toolingを含めないため、`LICENSE-CODE` はZIP内の必須ファイルにはしない。source repositoryには保持する。

さらに次を確認する。

- Sarasa Gothic / Source Han Sans の著作権表示を保持
- Hack / Bitstream Vera の通知を保持
- HackGen は engineering reference としての位置づけが正しく記載されている
- AI支援開発の記載が upstream の権利表示と混同されていない
- TTF `name` table の copyright / license metadata と配布ファイルの内容が矛盾しない

## 6. README / ドキュメント

- `README.md` は日本語メインで、冒頭に `紗絡（Sarack）` と日英の短い概要を示す
- `README.en.md` への導線がある
- README は特徴・利用方法中心で、具体的な補正値を過剰に載せない
- `Mono` / `Term` がspacing variantであり、`Term` がNerd Fontを意味しないことが分かる
- 標準版が U+3000 可視、`HS` が Hidden Space であることが分かる
- 具体的な設計値は `docs/DESIGN.md`
- 再現ビルド手順は `docs/BUILD.md`
- Release 手順は本書 `docs/RELEASE.md`
- 公開先repositoryのURL・badge・Release linkが最終repository名と一致している
- Release ZIPにREADMEを同梱するため、最終repository URLへ切り替えた後に正式配布候補を再生成する
- スクリーンショットが実際の Release TTF で生成されている

## 7. バッジ

公開時の README badge は情報性の高いものだけにする。

推奨:

- Build status
- Font License: OFL-1.1
- Code License: MIT

初回正式Release後:

- README 冒頭にコメントアウト済みの `Latest Release` badge を有効化する
- badgeは通常Releaseのみを表示し、Pre-releaseは表示対象に含めない。リンク先は `https://github.com/h-hopper/Sarack/releases` とする

原則として追加しない:

- 対応OS・エディタを大量に並べる装飾 badge
- upstream version を badge 化したもの

## 8. 公開repositoryへの移行

公開先の `h-hopper/Sarack` は、旧Private開発repositoryとは独立した新repositoryである。初期importでは、監査済みbaselineを独立したroot commitとして作成済みであり、旧 `Sarack-Code` のcommit ancestry・PR・branch・Actions履歴は移行していない。

初期baseline後の公開準備変更は、通常のreviewed PR / commitとして積み上げてよい。Public化時点で複数commitが存在してよく、history rewriteで1 commitへ戻す必要はない。目的は旧repositoryとの履歴分離であり、Public化まで単一commitを維持することではない。

公開用treeの準備と、repository作成・初期commit投入・Public化・tag / Release公開は別工程として扱う。tree準備だけでは後者を実行しない。旧repositoryのarchive・削除も別途判断する。

Public化前には以下を確認する。

- 移植するtracked treeにsecret / token / 不要な個人情報・ローカルパス・生成物が含まれていない
- 初期importで旧repositoryの `.git` をコピーせず、baselineが独立したroot commitとして作成されている
- baseline後の公開準備変更がreview済みの通常commitとして記録され、旧repositoryのcommit ancestryが混入していない
- README / license / workflow がPublic前提で読める
- repository名・README内URL・badge・Release導線が最終公開先と一致する
- Public化前はrepositoryがPrivateであるため、README内リンクやBuild badgeの外部表示はPublic化後に確認する。workflow自体はrepository名に依存しない
- GitHub Secrets・Actions設定・権限・branch protectionはtreeと別に確認する。旧repositoryの設定が自動移行するとは扱わない
- 新repositoryで `build.yml` と `release-package.yml`（version `0.1.0`）を実行し、CIと生成artifactを確認してからPublic化する

## 9. GitHub Release

初回公開versionは **`v0.1.0`** とし、GitHub Release上では正式な **通常Release** として公開する。Pre-release設定は **OFF** とする。

Pre-releaseは、将来、外部検証が必要なRC / beta等に限定して使用する（例: `v0.2.0-rc.1`）。RC / beta等をPre-releaseとして公開した場合、正式版は別tag（例: `v0.2.0`）として作成し、同一tagをPre-releaseから通常Releaseへ昇格させる運用は原則行わない。`v0.x` であること自体はGitHub Pre-releaseと同義ではない。

正式配布候補は `.github/workflows/release-package.yml` で `0.1.0` を指定して生成し、Release assetは次を基本構成とする。

```text
Sarack-Mono-v0.1.0.zip
Sarack-Term-v0.1.0.zip
SHA256SUMS.txt
```

Mono版 Release archive:

```text
SarackMono-Regular.ttf
SarackMono-Bold.ttf
SarackMono-Italic.ttf
SarackMono-BoldItalic.ttf
SarackMonoHS-Regular.ttf
SarackMonoHS-Bold.ttf
SarackMonoHS-Italic.ttf
SarackMonoHS-BoldItalic.ttf
LICENSE-FONT
THIRD_PARTY_NOTICES.md
ACKNOWLEDGEMENTS.md
README.md
README.en.md
LICENSES/Sarasa-Gothic-OFL.txt
LICENSES/Hack-LICENSE.md
```

Term版 Release archive:

```text
SarackTerm-Regular.ttf
SarackTerm-Bold.ttf
SarackTerm-Italic.ttf
SarackTerm-BoldItalic.ttf
SarackTermHS-Regular.ttf
SarackTermHS-Bold.ttf
SarackTermHS-Italic.ttf
SarackTermHS-BoldItalic.ttf
LICENSE-FONT
THIRD_PARTY_NOTICES.md
ACKNOWLEDGEMENTS.md
README.md
README.en.md
LICENSES/Sarasa-Gothic-OFL.txt
LICENSES/Hack-LICENSE.md
```

各ZIPはvariant/version名の単一root directoryを持たせる。`package_release.py` は固定timestampと固定されたentry順でarchiveを生成し、`SHA256SUMS.txt` に2 ZIPのSHA-256を記録する。

Release前の実ファイル監査では少なくとも次を確認する。

- 2 ZIPのSHA-256が `SHA256SUMS.txt` と一致する
- 各ZIPにTTFが正確に8本含まれる
- family / style / version / PostScript name / OFL metadataが想定どおりである
- half/full widthが500/1000である
- U+3000が1000幅を維持し、標準版は可視・HS版は不可視である
- Mono / TermのU+2014が1000 / 500である
- `cvt ` / `fpgm` / `prep` がなく、Unhinted状態を維持している
- 上流ライセンス原文・第三者通知・READMEが同梱されている

## 10. 公開後

- Public 化後に README badge / links が正常表示されるか確認
- `Latest Release` badge を有効化する
- Release archive を実際にダウンロードし、内容を確認
- `SHA256SUMS.txt` で公開assetを再検証する
- 新規インストール環境で Mono / Mono HS / Term / Term HS の family linking と同時インストールを再確認
- 必要なら `CHANGELOG.md` を v0.x の時点から開始する
