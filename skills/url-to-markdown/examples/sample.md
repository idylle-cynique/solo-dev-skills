# url-to-markdown 適用例

## 入力

```
https://example.com
```

## 実行コマンド

```bash
python3 resources/scripts/url_to_markdown.py "https://example.com"
```

## 出力

```markdown
# Example Domain

This domain is for use in documentation examples without needing permission. Avoid use in operations.

[Learn more](https://iana.org/domains/example)
```

`example.com` は `<article>`/`<main>` も本文用の `class`/`id` も持たないシンプルなページのため、本文抽出は該当なしとなりページ全体を返す（`--full` と同じ結果）。

## 本文抽出の効果（サンプルHTML）

`<article>` タグでヘッダー・ナビゲーションと本文が分離されている典型的なブログ構造を想定した例。

### 入力HTML（サンプル）

```html
<header><a href="/">Sample Blog</a> <nav><a href="/about">About</a></nav></header>
<article>
  <h1>Sample Article Title</h1>
  <p>This is the main body text of the article.</p>
</article>
<footer>Copyright 2026</footer>
```

### `--full`（抽出なし・ページ全体）

```markdown
[Sample Blog](/) [About](/about)

# Sample Article Title

This is the main body text of the article.

Copyright 2026
```

### デフォルト（`<article>` 抽出）

```markdown
# Sample Article Title

This is the main body text of the article.
```

ヘッダー・ナビゲーション・フッターが除去され、`<article>` 内の本文のみが残っていることが確認できる。
