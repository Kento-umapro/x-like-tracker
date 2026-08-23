# いいね実績ボード

X（@monja_no_KENT）の日々の活動記録。

- **おすすめ（For you）でいいねした数**
- **フォロー中（Following）でいいねした数**
- **フォロワー数と、その日ごとの増減**

公開ページ → https://kento-umapro.github.io/x-like-tracker/

## 使い方

記録の実体は `data.json`。追記すると `index.html` が作り直されます。

```bash
python3 log.py --foryou 100 --following 50 --followers 447
```

- 同じ日に複数回まわした分は、その日の合計に足し込まれます（`--replace` で上書き）
- 過去の日を埋めるときは `--date 2026-08-22`
- `build.py` は `data.json` から `index.html` を生成するだけのスクリプトです

フォロワーの前日比は、記録が2日分たまってから表示されます。
