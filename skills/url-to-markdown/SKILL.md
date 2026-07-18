---
name: url-to-markdown
license: MIT
description: >
  WebページのURLをhtml2text経由でMarkdown形式のテキストに変換するスキル。html2text CLIはURLを直接受け付けずファイルパスとして解釈してしまうため、事前にHTTPで取得してから変換する。
  ユーザーがURLを渡して「Markdown化して」「テキストで見たい」「html2textで変換して」「内容を確認したい」と言ったときは、明示されていなくてもこのスキルを参照すること。
argument-hint: [URL]
---

## 前提: なぜこのスキルが必要か

`html2text` CLIは `filename` 位置引数のみを受け付け、URLを渡すと `FileNotFoundError` になる。そのため、URLをMarkdown化するには「HTTPで取得 → html2textに渡す」という2段階の処理が必要であり、それを1コマンドにまとめたものがこのスキル。

## 依存関係の確認

1. `html2text` がインストール済みか確認する。

   ```bash
   python3 -c "import html2text; print(html2text.__version__)"
   ```

2. 未インストール、または `ModuleNotFoundError` の場合は `pip install html2text` の実行可否をユーザーに確認してからインストールする（環境変更を伴うため無断で実行しない）。
3. プロジェクトに `venv` が存在する場合は、インストール・実行の前に `source venv/bin/activate` で有効化する。

## 実行手順

1. 対象URLを引数に、変換スクリプトを実行する。デフォルトで本文抽出が有効。

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/resources/scripts/url_to_markdown.py "<URL>"
   ```

2. 本文抽出をせずページ全体を変換したい場合は `--full` を付ける。

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/resources/scripts/url_to_markdown.py "<URL>" --full
   ```

3. 標準出力に変換後のMarkdownが表示される。そのままユーザーへ提示するか、ユーザーの指示に応じてファイルへ保存する。

## 本文抽出のロジック

技術記事・公式ドキュメントであっても `<article>` タグが必ず使われているとは限らない（`<main>` や独自クラスの `div` で本文を囲むサイトも多い）ため、以下の優先順位でフォールバックする。追加の依存パッケージ（BeautifulSoup等）は増やさず、標準ライブラリの `re` のみで実装している。

1. `<article>` タグがあれば、その内容を使う
2. なければ `<main>` タグを試す
3. それもなければ `class`/`id` に `content` / `post` / `article` / `entry` を含む `div` を探す
4. いずれも見つからなければページ全体（`--full` と同じ結果）を使う

## 出力時の注意点

- 本文抽出のフォールバックはヒューリスティックであり、必ず正確に本文だけを抜き出せるとは限らない。抽出結果が不自然（短すぎる・本文が欠けている等）な場合は `--full` で全体を確認する
- JavaScriptでクライアントサイドレンダリングされるSPA形式のドキュメントサイト（Docusaurus、GitBook等）は、`urllib` での取得では本文がそもそもHTMLに含まれない場合がある。この場合は本文抽出の優先順位以前の問題であり、ヘッドレスブラウザでのレンダリングが必要になる旨をユーザーに伝える
- それでもノイズが残る場合は `html2text.HTML2Text()` のオプション（`ignore_images` / `ignore_links` 等）で情報量を減らす選択肢もある

## 出力例

`examples/sample.md` を参照。
