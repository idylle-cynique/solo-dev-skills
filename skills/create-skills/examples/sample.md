<!-- このファイルは create-skills スキルが生成するSKILL.mdの出力例です。
     check-review-draft スキルの作成を例としています。 -->

---

**入力**: `PRのレビューコメントを確認して対応方針をmdに書き出すスキルを作りたい。PR番号を引数で受け取り、プロジェクト用に作る。`

---

## 判断内容

**スコープ**: プロジェクト用（`.claude/skills/`）
- 明示的に「プロジェクト用」と指定されているため

**フロントマター**:
- `name: check-review-draft` — ディレクトリ名と一致
- `description` — 自動発動はさせたくない（ユーザーが明示的に呼ぶスキル）が、説明は記述しておく
- `argument-hint: PR番号（省略時は現在のブランチに対応するオープンPRを自動検出）` — 引数ありのため設定
- `disable-model-invocation: true` は**設定しない** — レビューコメントの確認は副作用がなく、Claude が自動判断してもよい

**コンテンツ種別**: タスク型（gh CLI でコメント取得 → 分類 → md 作成という手順を持つ）

---

## 作成したファイル

`.claude/skills/check-review-draft/SKILL.md`:

```markdown
---
name: check-review-draft
description: PRのレビューコメントを取得し、対応方針をmdに書き出す
argument-hint: PR番号（省略時は現在のブランチに対応するオープンPRを自動検出）
---

以下の手順で PR レビューコメントの対応方針ドキュメントを作成してください。

## 入力

PR番号: $ARGUMENTS

## 1. PR・レビューコメント取得
...
```

`.claude/skills/check-review-draft/examples/sample.md`:
- PR #89 Copilot レビューを使った実際の出力例

---

## 呼び出し方

- `/check-review-draft 89` — PR番号を指定して呼び出す
- `/check-review-draft` — 省略時は現在ブランチのオープンPRを自動検出
- Claude が「レビューコメントを確認して」という会話に自動反応する可能性あり（`disable-model-invocation` 未設定のため）
