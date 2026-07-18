<!-- このファイルは create-pr スキルが生成するPR本文の出力例です。
     feat/61/fix-pre-push-mismatch ブランチのPR作成を例としています。 -->

---

**入力**: `/create-pr`（feat/61/fix-pre-push-mismatch ブランチで実行）

---

## 確認した状態

- ブランチ: `feat/61/fix-pre-push-mismatch`
- Issue: #61（ブランチ名から抽出）
- コミット:
  - `fix: pre-pushフックのGITHUB_USER取得をlogin名ベースに修正`
  - `feat: skillを追加`
  - `docs: レビューコメント対応用のskillを追加`
- 主要な変更ファイル: `scripts/hooks/pre-push`（1行変更）
- 既存PR: なし

---

## 生成したPRタイトルと本文

**タイトル**: `fix: pre-pushフックのユーザー検証をlogin名ベースに修正`

**本文**:

---

## Issue

― Resolves #61

## 概要

git config user.nameは表示名を返すが、GitHub APIのloginはlogin名を返すため
ユーザー検証の突合が常に失敗していた。gh api userでlogin名を取得するよう修正した。

## 変更内容

- `scripts/hooks/pre-push`
  - GITHUB_USER取得を`git config user.name`から`gh api user --jq '.login'`に変更
    - APIのassignees[].loginと突合するにはlogin名が必要なため

## 変更の種類

- [x] バグ修正 (Bug fix)
- [ ] 新機能 (New feature)
- [ ] 破壊的変更 (Breaking change)
- [ ] ドキュメント更新 (Documentation update)
- [ ] リファクタリング (Refactoring)
- [ ] テスト追加・修正 (Test)
- [ ] その他 (Other)

## 動作確認手順

1. `feat/*` ブランチでオープンなPRを持つリポジトリに移動する
2. `./scripts/hooks/install-hooks.sh` でフックをインストールする
3. 自分がアサインされているPRのブランチで `git push` を実行し、プッシュが通ることを確認する
4. 自分がアサインされていないPRのブランチで `git push` を実行し、ブロックされることを確認する

## 補足情報

gh未インストール時は`git config user.name`にフォールバックする動作は維持している。

---

## 呼び出し方

- `/create-pr` — 引数なし。現在のブランチ状態から自動で判断してPRを作成する
