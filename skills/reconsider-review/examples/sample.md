<!-- このファイルは reconsider-review スキルが生成するmdの出力例です。PR #42（Copilot レビュー）を使用しています。 -->

# PR #42 レビュー対応方針

**レビュアー:** GitHub Copilot
**確認日:** 2026-03-28

---

## コメント一覧と対応方針

### 1. メモリ使用量（`daily_sales_repository.py:107`） — 対応不要

**指摘内容:** `all_records` に全件溜めてから upsert するため、CSVが大きい場合にメモリ使用量が増える。

**検証:** インポート対象の CSV は日次売上データで最大366件。メモリ上の懸念は発生しない。

**対応方針:** 対応不要。

---

### 2. `alembic/env.py` docstring（`env.py:31`） — 修正対象

**指摘内容:** docstring に「未設定の場合は alembic.ini のディレクトリを基準」と書かれているが、`config_file_name` が `None` の場合はカレントディレクトリにフォールバックする実装になっており、説明が食い違っている。

**対応方針:** docstring を実装に合わせて修正する。

```python
# 修正前
未設定の場合は alembic.ini のディレクトリを基準に絶対パスを解決する。

# 修正後
未設定の場合は alembic.ini のディレクトリ（取得不可の場合はカレントディレクトリ）を
基準に絶対パスを解決する。
```

---

### 3. SQLite bind parameter 上限（`daily_sales_repository.py:168`） — 修正対象

**指摘内容:** `sqlite_insert(...).values([...])` でマルチ VALUES を生成すると、レコード数 × カラム数が SQLite の bind parameter 上限（デフォルト 999）を超えて `OperationalError: too many SQL variables` になり得る。

**対応方針:** executemany 形式に変更して上限を回避する。

```python
rows = [
    {"date": r.date, "symbol": r.symbol, "sales_amount": r.sales_amount}
    for r in records
]
stmt = sqlite_insert(DailySalesRecord)
upsert_stmt = stmt.on_conflict_do_update(
    index_elements=["date", "symbol"],
    set_={"sales_amount": stmt.excluded.sales_amount},
)
with Session(self.engine) as session:
    session.execute(upsert_stmt, rows)
    session.commit()
```

---

### 4. `create_all` と docstring の矛盾（`daily_sales_repository.py:29`） — 対応保留

**指摘内容:** docstring では「Alembic で管理」と案内しているが `__init__` で `create_all` が走る。

**対応方針:** 対応保留。別途 Issue #33 で管理済み。

---

### 5. ログレベルの変更（`service.py:42`） — 要議論

**指摘内容:** `logger.info` → `logger.warning` に変更する提案。

**検証:** Issue #29 のタスクリストでは `logger.info` と明示されている。`warning` が意味的に適切かどうかは判断が難しく、仕様変更を伴う可能性がある。

**対応方針:** 要議論。Issue #29 の仕様意図をレビュアーと確認する。

---

### 6. `_collect_row_records` の日付 `ValueError` 非捕捉（`daily_sales_repository.py:130`） — 修正対象

**指摘内容:** 不正な日付行が1つでもあるとインポート全体が停止する。価格パースでは無効値をスキップしているので、挙動を一貫させるべき。

**対応方針:** 価格パースと同じパターンで `ValueError` を捕捉し、その行をスキップして警告ログを出す。

```python
try:
    target_date = date.fromisoformat(date_str)
except ValueError as e:
    logger.warning(
        "無効な日付データをスキップしました: ファイル=%s, 日付=%s, エラー=%s",
        csv_path.name, date_str, e,
    )
    return []
```

---

## 対応まとめ

| # | 対象箇所 | ステータス |
|---|---------|------|
| 1 | `import_from_csv` メモリ使用量 | 対応不要 |
| 2 | `env.py` docstring | **修正対象** |
| 3 | `_bulk_upsert` bind parameter 上限 | **修正対象** |
| 4 | `create_all` docstring 矛盾 | 対応保留（Issue #33） |
| 5 | ログレベル変更 | **要議論** |
| 6 | `_collect_row_records` 日付 ValueError | **修正対象** |
