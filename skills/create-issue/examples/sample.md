<!-- このファイルは create-issue スキルが生成するmdの出力例です。new-feature テンプレートを使用しています。 -->

**タイトル候補**: feat: ポートフォリオ保有銘柄の損益率をモニタリング画面に表示する

## 概要
<!-- 実装する機能やタスクの概要を簡潔に記述 -->

`asset_monitor.py` のモニタリング出力に損益率（取得原価比）を追加する。
`config/assets.json` に各銘柄の取得原価を記載できるようにし、現在値との差分から損益額・損益率を算出して表示する。


## 背景・目的
<!-- なぜこの機能が必要か、どんな課題を解決するのか -->

現状のモニタリングでは現在値・前日比しか表示されず、保有コストに対する損益がわからない。
取得原価と現在値を並列表示することで、リバランス判断やパフォーマンス評価をポートフォリオ画面上で完結できるようにする。


## 実装内容
<!-- 具体的に何を実装するか -->

`config/assets.json` の各銘柄エントリに `cost_price`（取得原価）フィールドを追加し、
`asset_monitor.py` の表示ロジックで損益額・損益率を算出して出力に含める。

### 表示イメージ

```
銘柄      現在値          取得原価        損益額          損益率
SAMP     120.00 USD      100.00 USD      +20.00 USD      +20.00%
TEST     1,200 JPY       1,000 JPY       +200 JPY        +20.00%
```

### 変更ファイル

- `config/assets.json`：各銘柄に `cost_price` フィールドを追加
- `app/asset_data/`：損益情報を含む TypedDict を追加
- `app/asset_monitor.py`：損益算出・表示ロジックを追加
- `tests/test_asset_monitor.py`：損益計算のテストを追加


## タスク
<!-- 作業を分解してチェックリスト化 -->

- [ ] `config/assets.json` のスキーマに `cost_price` フィールドを追加
- [ ] `app/asset_data/` に損益情報の TypedDict を定義する
  - [ ] `ProfitLossInfo` を定義（`cost_price`, `profit_loss`, `profit_loss_rate`）
- [ ] `asset_monitor.py` を更新
  - [ ] `config/assets.json` から `cost_price` を読み込む
  - [ ] 損益額・損益率の算出ロジックを追加
  - [ ] 表示フォーマットに損益列を追加
- [ ] `tests/test_asset_monitor.py` にテストを追加
  - [ ] `cost_price` ありの場合の損益算出テスト
  - [ ] `cost_price` 未設定の場合の表示テスト（「-」表示になること）


## 完了条件
<!-- どの状態になれば完了とみなすか -->

- [ ] `pytest tests/test_asset_monitor.py -v` が全て通ること
- [ ] `mypy app/` でエラーがないこと
- [ ] `config/assets.json` に `cost_price` を設定した状態で損益率が正しく表示されること
- [ ] `cost_price` 未設定の銘柄は損益列が「-」になること


## 技術メモ
<!-- 使用する技術、ライブラリ、実装方針などのメモ -->

- `cost_price` が `config/assets.json` に未設定の銘柄はスキップし、損益列は「-」と表示する
- 通貨の差異（USD/JPY）は考慮しない。表示は取得時の通貨のまま
- 損益率の算出式：`(current_price - cost_price) / cost_price * 100`


## 参考資料
<!-- 参考にするドキュメント、記事、Issue等のリンク -->

