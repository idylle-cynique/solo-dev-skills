# format-doc 適用例

## 入力（整形前）

```markdown
## Webhook 実装メモ

- エンドポイントは `POST /webhooks/receive` で、ペイロードは JSON、署名検証には `X-Signature-256` ヘッダーを使う（HMAC-SHA256、シークレットは環境変数 `WEBHOOK_SECRET` から取得）。
- 受信したイベントはキューに積んで非同期処理する。キューには Redis を使い、ワーカープロセスが別途 `jobs/webhook_worker.rb` で動く。失敗時は最大3回リトライし、それでも失敗したら `webhook_failures` テーブルに記録して管理画面から再送できるようにする。
- ローカル開発では ngrok でトンネルを張って外部サービスからのリクエストを受け取る。`.env.local` に `WEBHOOK_SECRET` と `REDIS_URL` を設定する必要があり、`.env.example` にサンプルあり。
- テストは `spec/requests/webhooks_spec.rb` に書く。署名検証の正常系・異常系とペイロード形式のバリデーションをカバーすること。
```

## 出力（整形後）

```markdown
## Webhook 実装メモ

- エンドポイント: `POST /webhooks/receive`
  - ペイロード形式: JSON
  - 署名検証ヘッダー: `X-Signature-256`（HMAC-SHA256）
  - シークレット取得元: 環境変数 `WEBHOOK_SECRET`
- 受信イベントはキューに積んで非同期処理する
  - キュー実装: Redis
  - ワーカー: `jobs/webhook_worker.rb`（別プロセス）
  - 失敗時は最大3回リトライする
  - リトライ全失敗時は `webhook_failures` テーブルに記録し、管理画面から再送できる
- ローカル開発には以下の準備が必要
  - ngrok でトンネルを張り、外部サービスからのリクエストを受け取る
  - `.env.local` に `WEBHOOK_SECRET` と `REDIS_URL` を設定する
  - サンプル: `.env.example`
- テスト: `spec/requests/webhooks_spec.rb`
  - 署名検証の正常系・異常系
  - ペイロード形式のバリデーション
```

## 適用した変更

- 原則1+4: 1行目「エンドポイント」「ペイロード」「署名検証」「シークレット」を `語: 語` 記法の子項目に分割
- 原則1+2: 2行目「キュー処理」を事実・実装詳細・失敗時挙動に分割し、子項目へ
- 原則1+2: 3行目「ローカル開発」を目的ごとに分割し、設定項目を子項目リストに整理
- 原則1+2: 4行目「テスト」を `語: 語` 記法に変え、カバー範囲を子項目に分割
- 原則3: 全項目末尾の `。` を除去
