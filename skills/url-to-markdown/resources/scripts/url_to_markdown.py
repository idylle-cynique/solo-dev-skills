import re
import sys
import urllib.request

import html2text


def _extract_balanced_tag(html: str, tag: str, start_pos: int) -> str | None:
    """start_pos以降で最初に現れるtagの開始〜対応する終了タグまでを抜き出す。
    見つからない/閉じタグが対応しない場合はNoneを返す。
    """
    open_re = re.compile(rf"<{tag}\b[^>]*>", re.IGNORECASE)
    close_re = re.compile(rf"</{tag}\s*>", re.IGNORECASE)

    m = open_re.search(html, start_pos)
    if not m:
        return None

    depth = 1
    pos = m.end()
    while depth > 0:
        next_open = open_re.search(html, pos)
        next_close = close_re.search(html, pos)
        if not next_close:
            return None
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()
    return html[m.start():pos]


def extract_main_content(html: str) -> str:
    """本文とみなせる要素をこの優先順位で探し、見つからなければページ全体を返す。
    1. <article> 2. <main> 3. content/post/article/entry を含むclass・idのdiv
    """
    article = _extract_balanced_tag(html, "article", 0)
    if article:
        return article

    main = _extract_balanced_tag(html, "main", 0)
    if main:
        return main

    div_re = re.compile(
        r'<div\b[^>]*(?:class|id)="[^"]*(?:content|post|article|entry)[^"]*"[^>]*>',
        re.IGNORECASE,
    )
    m = div_re.search(html)
    if m:
        div = _extract_balanced_tag(html, "div", m.start())
        if div:
            return div

    return html


def fetch_as_markdown(url: str, full_page: bool = False) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        charset = res.headers.get_content_charset() or "utf-8"
        html = res.read().decode(charset, errors="replace")

    target_html = html if full_page else extract_main_content(html)

    converter = html2text.HTML2Text()
    converter.body_width = 0
    return converter.handle(target_html)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 url_to_markdown.py <URL> [--full]", file=sys.stderr)
        sys.exit(1)

    target_url = sys.argv[1]
    use_full_page = "--full" in sys.argv[2:]
    print(fetch_as_markdown(target_url, full_page=use_full_page))
