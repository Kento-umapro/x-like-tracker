# Threads 転載（西村 @doteppan_nishimuu）

X の【】付きノウハウ投稿を、同じ日に Threads にも出す運用（2026-09-18 開始）。

- 元データ: `queue.json`（`output/x_posts_batch6.xlsx` 朝枠 と `x_posts_lunch_evening_50x2.xlsx` 昼12時枠シート。Excelの日付は実際のX投稿日より1日後なので −1日で補正済み）
- 時刻: 朝枠 = Threads 07:10（Xは6:40〜6:50）／夕方枠 = Threads 17:30（Xは16:52〜17:10）
- 方法: Threads Web の「新しいスレッド」→ … →「日時を指定...」で本体に予約登録（API・サーバー不要）
- **制限: Threads の予約は同時に25件まで。** 25件を超える分は `status: pending` のまま。
  毎日の X いいね実行のついでに、消化された分だけ pending を予約に追加する（1日2件ずつ空く）。
- `status`: posted / scheduled / draft（Threads の下書きに保存済み・未予約）/ pending

## 追加登録の手順（Claude Code）
1. 西村Chrome（deviceId 79a592bf…）で threads.com を開く（ログイン済み）
2. 新しいスレッド → 本文入力 → 右上「…」→「日時を指定...」→ 日付セル・hh/mm → 完了 →「日時を指定」ボタン
3. 「JSTに投稿予定」トーストを確認して queue.json の status を scheduled に更新
