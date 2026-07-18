# PR #34 仕様整合性チェック

**対象 Issue:** #5 feat(exporter): データのバッチエクスポートをページ単位処理に変更
**確認日:** 2026-01-15

---

## Issue タスクの反映状況

| タスク | ファイル / 関数 | 状態 |
|--------|---------------|------|
| `batchExportProcessor.js` をページ単位処理に書き換え | `batchExportProcessor.js`: `startBatchExport`, `processChunk`, `completeExport`, `resetBatchExport` | 完了 |
| `background.js` に import 追加 | `background.js` 冒頭の import 文 | 完了 |
| `startExport()` 後に `startBatchExport()` 呼び出しを追加 | `handleStartExport` 等2ハンドラ内 | 完了 |
| `CHUNK_DATA_RESULT` ハンドラで `processChunk()` 呼び出しを追加 | `background.js:134` | 完了 |
| `resetState()` 内で `resetBatchExport()` を呼ぶ | `resetState()` 内 | 完了 |
| エクスポート完了ログを `appendLog()` で出力 | `background.js:138-142` | 完了 |

## Issue 完了条件の確認

| 完了条件 | 確認内容 | 状態 |
|---------|---------|------|
| 各ページのデータ受信時に即座に書き出される | `CHUNK_DATA_RESULT` で `processChunk` を呼び出している | 満足 |
| 再実行時に重複行が書き出されない（冪等性） | `processedKeys` Set でインメモリ dedup が実装されている | 満足 |
| エクスポート失敗がデータ取得パイプラインをブロックしない | `processChunk` は常に `{ok,...}` を返し reject しない | 満足 |
| TypeA / TypeB 全種別で動作する | 2ハンドラ全てに `startBatchExport` / `processChunk` が追加されている | 満足 |

## PR 本文と実装差分の整合性

| PR 記述 | 差分での確認結果 | 判定 |
|---------|---------------|------|
| `startBatchExport` / `processChunk` / `completeExport` / `resetBatchExport` の追加 | `batchExportProcessor.js` に全関数が存在 | OK |
| `startExport()` を `startBatchExport()` に置き換え | 2ハンドラ全てで置き換え済み | OK |
| `appendLog()` に直列化キュー追加 | `_logQueue` と `resetLogs` が追加されている | OK |
| 「完了」ログを `completeExport()` 完了後に書き込むよう変更 | `onDataComplete` 内で `completeExport` await 後に `appendLog` | OK |
| `popup.js` で `msg.status` を反映 | `popup.js` の `*_EXPORT_PROGRESS` case に `status` 反映あり | OK |

## 齟齬・懸念事項

### 未実装 / 記述漏れ（要対応）

なし

### 記述過剰（PR本文に書いてあるが差分にない）

なし

### 要確認（判断が難しい）

- PR 本文「セッショントークンで旧セッションの `.then()` が新セッション状態を汚染しないようガード」→ `_batchSessionToken` によるガードは実装済みだが、`completeExport` 完了前に `exportErrors++` が実行されない microtask 順序の問題が別途存在（レビューコメント #2 参照）

---

## 総合判定

**要修正（1件）** — `exportErrors` と `completeExport` の競合により、最終ページのエクスポート失敗がフォールバック判断に反映されない可能性があります。詳細は「要確認」セクションを確認してください。
