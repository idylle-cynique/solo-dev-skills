---
name: bulk-review
license: MIT
description: review・code-review・security-review の 3 種レビューに加え simplify による差分提案をサブエージェントで並列実行し、それぞれの結果を統一した md フォーマットでファイルに書き出す。simplify はコードを直接書き換えず、隔離 worktree 内で得た差分案を md に記録するだけにとどめる。「全部レビューして」「3種並列でレビュー」「bulk-review」と言われたとき、または対象コードを網羅的にレビューしたいときは、明示されていなくても必ずこのスキルを使う
argument-hint: 対象（PR番号・ブランチ名・ファイルパス。省略時は現在ブランチの差分）
when_to_use: simplify（差分提案）・review・code-review・security-review を一括で走らせて結果を md に残したいとき
allowed-tools: Read, Grep, Glob, Bash, Agent
---

以下の手順で、simplify（差分提案）を含む 4 種の処理をサブエージェントで並列実行し、結果をそれぞれ md に書き出してください。simplify は実コードを書き換えず、差分案を md に記録するだけにとどめます。

## 入力

対象: $ARGUMENTS

PR 番号が渡された場合は `gh pr view <番号>` でマージ先ブランチを確認してから各エージェントに渡してください。PR 番号がない場合は現在ブランチに紐づくオープン PR を自動検出し、それでも見つからない場合は `origin/HEAD` または `main` を差分ベースとします。

## 1. 対象の確定

レビュー対象のコンテキストを収集します。

```bash
# PR番号が指定された場合（またはブランチから自動検出）
gh pr view <番号または省略> --json number,title,body,baseRefName,headRefName

# ベースブランチが確定したら差分を取得（baseRefName を使う）
git diff origin/<baseRefName>...HEAD --name-only
git diff origin/<baseRefName>...HEAD
```

各サブエージェントに渡すため、以下を確定させてください:

- 対象の説明文（例: `PR #56 "feat: CSVエクスポート順序の変更"` / `ブランチ feat/56/change-order`）
- ベースブランチ名（PR の `baseRefName`。PR がない場合は `origin/HEAD` or `main`）
- Issue 番号（PR から "Resolves #N" を抽出、なければ `null`）
- 各レビューの保存先パス（CLAUDE.md 規約に従い、ここで決定する）:
  - Issue 番号あり: `.vscode/docs/tasks/<issue番号>/simplify.md`・`review.md`・`code-review.md`・`security-review.md`
  - Issue 番号なし: `.vscode/docs/plans/simplify_<YYYY-MM-DD>.md`・`review_<YYYY-MM-DD>.md`・`code-review_<YYYY-MM-DD>.md`・`security-review_<YYYY-MM-DD>.md`
  - ディレクトリが存在しない場合は `mkdir -p` で作成しておく

## 2. 4 エージェントを同時に起動する

**必ず 1 度のメッセージで 4 つの Agent ツール呼び出しを並べ、並列実行してください。**順番に呼び出すと直列になり並列化の意味がなくなります。

各エージェントへのプロンプトは以下のテンプレートを使い、`<対象>` `<baseRefName>` `<保存先パス>` を実際の値に置き換えてください。Agent 2〜4 は各サブエージェントがスキルを呼び出したうえで結果を自分でファイルへ書き出して完結しますが、Agent 1（simplify）だけは隔離 worktree 内で完結させ、ファイル書き出しはオーケストレーター側（このスキルを実行している自分自身）が行います。

---

**Agent 1 — Simplify（差分提案・隔離実行）**

**この Agent 呼び出しには `isolation: "worktree"` を指定してください。** simplify はコードを直接書き換えるスキルのため、隔離 worktree 内で実行することで実際の作業ツリーに影響を与えず、他の 3 エージェントとも安全に並列実行できます。

```
以下の対象に対して `/simplify` スキルを実行し、生成された差分を報告してください（ファイルへの書き出しは行わないこと）。

対象: <対象の説明文>
ベースブランチ: <baseRefName>（差分は origin/<baseRefName>...HEAD で取得すること）

手順:
1. Skill ツールで skill: "simplify" を呼び出す（args に対象情報を渡す）
2. 適用された変更を `git diff` で取得する
3. 変更点ごとに「該当箇所・内容・差分（diff形式）」をまとめ、提案件数とともに最終メッセージとして返す
4. ここでの変更は隔離 worktree 内に閉じるため、実リポジトリへの影響はない
```

このAgentの完了報告を受け取ったら、オーケストレーター自身が以下の md テンプレートに整形し、Write ツールで `<simplify.md のパス>` に書き出してください（ファイルが既存なら Edit で差分のみ適用する）:

## md テンプレート:

# Simplify 差分提案

| 項目       | 内容                                  |
| ---------- | ------------------------------------- |
| 種別       | Simplify（提案型・未適用）            |
| 対象       | <対象の説明文>                        |
| 実施日     | <YYYY-MM-DD>                          |
| レビュアー | Claude Sonnet 4.6（サブエージェント） |
| 提案件数   | N件                                   |

## サマリー

<日本語で 2〜4 文>

## 提案する変更

### <タイトル>

- 該当箇所: `path/to/file.js:42`
- 内容: <何をどう簡略化する提案か>
- 差分案:
  ```diff
  - 変更前
  + 変更後
  ```

<提案順に列挙。なければ「提案なし」と書く>

## 次のアクション

- [ ] ...

---

**Agent 2 — 総合レビュー**

```
以下の対象に対して `/review` スキルを実行し、結果を指定ファイルに書き出してください。

対象: <対象の説明文>
ベースブランチ: <baseRefName>（差分は origin/<baseRefName>...HEAD で取得すること）
保存先: <review.md のパス>

手順:
1. Skill ツールで skill: "review" を呼び出す（args に対象情報を渡す）
2. スキルの結果を以下の md テンプレートに整形する
3. Write ツールで保存先に書き出す（ファイルが既存なら Edit で差分のみ適用する）
4. 書き出したパスと検出件数（重要度別）を報告する

md テンプレート:
---
# 総合レビュー レビュー結果

| 項目 | 内容 |
|---|---|
| レビュー種別 | 総合レビュー |
| 対象 | <対象の説明文> |
| 実施日 | <YYYY-MM-DD> |
| レビュアー | Claude Sonnet 4.6（サブエージェント） |
| 検出件数 | Critical: N / High: N / Medium: N / Low: N / Info: N |

## サマリー

<日本語で 2〜4 文>

## 指摘事項

### [High] <タイトル>

- 該当箇所: `path/to/file.js:42`
- 内容: <主要な事実を1文で。複数事実がある場合は子項目に分割>
  - <補足事実>
- 推奨対応: <主要な対応を1文で>
  - <代替案や補足があれば子項目に>
- 根拠: <High 以上は必須。リスト末尾に句読点をつけない>

<重要度の高い順に列挙。指摘がなければ「指摘事項なし」と書く>

## 補足・対応不要

- <Info 相当>

## 次のアクション

- [ ] ...
---
```

**Agent 3 — コードレビュー**

```
以下の対象に対して `/code-review` スキルを実行し、結果を指定ファイルに書き出してください。

対象: <対象の説明文>
ベースブランチ: <baseRefName>（差分は origin/<baseRefName>...HEAD で取得すること）
保存先: <code-review.md のパス>

手順:
1. Skill ツールで skill: "code-review" を呼び出す（args に対象情報を渡す）
2. スキルの結果を上記と同じ md テンプレートに整形する（レビュー種別は「コードレビュー」）
3. Write ツールで保存先に書き出す（ファイルが既存なら Edit で差分のみ適用する）
4. 書き出したパスと検出件数（重要度別）を報告する
```

**Agent 4 — セキュリティレビュー**

```
以下の対象に対して `/security-review` スキルを実行し、結果を指定ファイルに書き出してください。

対象: <対象の説明文>
ベースブランチ: <baseRefName>（差分は origin/<baseRefName>...HEAD で取得すること）
保存先: <security-review.md のパス>

手順:
1. Skill ツールで skill: "security-review" を呼び出す（args に対象情報を渡す）
2. スキルの結果を上記と同じ md テンプレートに整形する（レビュー種別は「セキュリティレビュー」。サマリーは日本語で書く）
3. Write ツールで保存先に書き出す（ファイルが既存なら Edit で差分のみ適用する）
4. 書き出したパスと検出件数（重要度別）を報告する
```

---

## 3. 報告待ち・集約

4 エージェントの完了報告が揃ったら、以下を集約してユーザーに報告してください:

- 対象
- 作成・更新した 4 ファイルのパス
- simplify の提案件数、および残り 3 種それぞれの検出件数（重要度別）
- 全種を通じて最優先で対応すべき指摘 1〜3 件の要約
