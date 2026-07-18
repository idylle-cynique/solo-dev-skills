<!-- derive-test-cases の出力例。この例では入力源として実装資料（フローチャート）を使用したが、
     実装資料が無い場合はブランチのcommit/diffを直接読んで同じ形式のテーブルを導出する。 -->

# pre-push フックのテストケース一覧（Issue #23）

| # | テストケース | 検証内容 | 期待する結果 |
| --- | --- | --- | --- |
| 1 | GITHUB_USERを特定できない | `GITHUB_USER`/`gh`認証情報がともに無い状態でフックを起動する | `exit 1`。「GitHub loginを特定できません」という趣旨のエラーがstderrに出る |
| 2 | mainブランチへの直push禁止 | `branch_name`が`main`のref行を渡す（force-pushではない通常push） | `exit 1`。「Direct push to main branch is not allowed」 |
| 3 | 全refが正常に処理された場合の正常終了 | 全てのref行がいずれのブロック条件にも該当しない状態でpushする | 最終行まで処理された後「✓ All pre-push validations passed」が出て`exit 0` |

## 既存テストスイートとの対応

`tests/scripts/hooks/` には現在21件のテストが実装済みで、上表のうち **#1 は未実装**。

- **#1（GITHUB_USER特定不可）**: 実装時に意図的にスコープ外とした（テストでは常に`GITHUB_USER`
  環境変数を明示設定し、`gh api user`/`git config`が呼ばれない状態を前提にしているため）
