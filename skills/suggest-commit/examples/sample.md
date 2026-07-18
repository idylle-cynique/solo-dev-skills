# suggest-commit 出力例

**入力状況**: pre-push フックのスクリプトを修正、ステージ済み

```
git diff --cached --stat
 scripts/hooks/pre-push | 18 +++++++++---------
 1 file changed, 9 insertions(+), 9 deletions(-)
```

---

## コミットメッセージ案

### 案1（推奨）
**理由**: バグ修正であり、スコープは変更対象のフック名が明確なため

```
fix(pre-push): GITHUBユーザー取得をlogin名ベースに修正
```

### 案2
**理由**: スコープをディレクトリ名にする場合

```
fix(hooks): pre-pushフックのユーザー識別ロジックを修正
```

### 案3（body付き）
**理由**: 修正の背景（なぜ変えたか）を残したい場合

```
fix(pre-push): GITHUBユーザー取得をlogin名ベースに修正

name フィールドは表示名のため一致しないケースがあった。
gh api /user の login フィールドを使うよう変更。
```
