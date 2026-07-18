---
name: create-agent
license: MIT
description: 新しいサブエージェントの定義ファイルを作成する。特定のタスクに特化したAIアシスタントを追加したいときに使う
argument-hint: エージェントの名前と目的の説明
disable-model-invocation: true
when_to_use: 新しいサブエージェントを追加したいとき
---

以下の手順でサブエージェントの定義ファイルを作成してください。

## 入力

エージェントの説明: $ARGUMENTS

## 1. スコープの選択

| スコープ | パス | 使い分け |
|---------|------|---------|
| プロジェクト用 | `.claude/agents/<name>.md` | このリポジトリ専用。チームで共有可能 |
| 個人用 | `~/.claude/agents/<name>.md` | 全プロジェクトで利用する汎用エージェント |

明示的な指定がない場合はプロジェクト用（`.claude/agents/`）を選択してください。

## 2. フロントマターの設計

以下の判断基準でフィールドを設定してください。

**`name`**（必須）
- 小文字とハイフンのみ。スラッシュコマンドや @-mention で使われる
- 例: `code-reviewer`, `self-review-checker`

**`description`**（必須）
- Claude が自動委譲するかどうかの判断に使われる重要フィールド
- 「いつ使うか」を含めて具体的に記述する
- 積極的に委譲させたい場合は "Use proactively when..." を含める
- 例: `Reviews code for quality and security. Use proactively after writing or modifying code.`

**`tools`**（省略時は全ツールを継承）
- 読み取り専用なら: `Read, Grep, Glob, Bash`
- 編集も必要なら: `Read, Edit, Write, Bash, Grep, Glob`
- 不要なツールを除外するには `disallowedTools` も使える

**`model`**（省略時は親会話から継承）
- `haiku` — 高速・低コスト（探索・検索向き）
- `sonnet` — バランス（分析・レビュー向き）
- `opus` — 高性能（複雑な推論向き）
- `inherit` — 親会話と同じモデル

**`permissionMode`**（省略時は `default`）
- `default` — 通常の権限チェック
- `acceptEdits` — ファイル編集を自動承認
- `plan` — 読み取り専用（プランモード）

**`memory`**（省略時はなし）
- `project` — `.claude/agent-memory/<name>/`（バージョン管理可能、推奨デフォルト）
- `user` — `~/.claude/agent-memory/<name>/`（全プロジェクト共通）
- `local` — `.claude/agent-memory-local/<name>/`（バージョン管理しない）
- 会話をまたいで学習を蓄積させたい場合に設定する

**`skills`**（省略時はなし）
- スタートアップ時にスキルの全コンテンツをコンテキストに注入する
- 親会話のスキルは継承されないため、必要なスキルは明示的にリストする

**`maxTurns`**（省略時は無制限）
- エージェントが停止するまでの最大ターン数

## 3. システムプロンプトの設計

markdown 本体がシステムプロンプトになります。以下の構成を意識してください：

```markdown
あなたは〇〇の専門家です。

呼び出されたとき:
1. まず〇〇を確認する
2. 次に〇〇を行う
3. 結果を〇〇の形式で返す

レビュー/分析のチェックリスト:
- 観点1
- 観点2
...

出力フォーマット:
- 重要度で優先順位をつける
- 具体的な改善例を示す
```

**ポイント:**
- サブエージェントは Claude Code のデフォルトシステムプロンプトを受け取らない。必要な前提知識はすべて記述する
- 「何をするか」だけでなく「どの順序で・どの形式で」まで明示する
- `memory` を使う場合は、いつメモリを読み書きするかをプロンプトに含める

## 4. ファイルの作成

以下の形式でファイルを作成してください:

```markdown
---
name: <name>
description: <description>
tools: <tool-list>
model: <model>
---

<system prompt>
```

## 5. 完了報告

以下を報告してください:

- 作成したファイルのパス
- 選択したフロントマターとその理由
- 呼び出し方（自動委譲 / @-mention / `/agents` から呼び出し）

## 参考

出力の品質・フォーマットの参考として `examples/sample.md` を参照してください。
