# 西村健人 X／Threads 予約投稿 運用指示書（別PC用）

このファイルを新しい Claude Code チャットの1通目に貼れば、そのチャットが
西村さん（X @monja_no_KENT／Threads @doteppan_nishimuu）の**投稿文の作成と予約登録**の担当になります。
「いいね」運用（`nishimura-x-like-instructions.md`）とは別チャットにしてください。

---

## 0. 全体像（文章はどこから来て、どこへ行くか）

```
松村メッセージ（COOメッセージ・毎朝1本）
  └ https://message.umapro-jp.com/              ← 一次素材。うまプロカルチャー「綴」。毎朝ここに出る
        ├ /notes.js   … vol.1〜484（LINE WORKS 時代の分・自動取得）
        └ /post.php   … vol.485〜（2026-09-30 以降はサイトに直接投稿。毎朝 5:30 前後）
        ↓ 要約・型に流し込み（ルールは「引き継ぎMD」）
  └ ~/どてっぱん/output/x_posts_*.xlsx            ← 文案の在庫（Excel・コピペ可）
        ↓ 1本ずつ予約登録
  ├ X 予約投稿（x.com/compose/post → Schedule）    ← 朝枠 6:40〜6:50／夕方枠 16:52〜17:10
  └ Threads 予約投稿（threads.com → 日時を指定）   ← 朝枠 07:10／夕方枠 17:30（Xの20〜30分後に同文を転載）
        └ ~/x-like-tracker/threads/queue.json     ← Threads側の予約台帳（25件上限の管理用）
```

**正（しょう）は常にX本体の予約一覧（Drafts → Scheduled）。** Excel と queue.json は台帳。ズレたらX側に合わせる。

---

## 1. 2つの枠と、それぞれの文章の出どころ

| 枠 | 投稿時刻（X） | 文章の素材 | 型 | 在庫ファイル |
|---|---|---|---|---|
| **朝枠** | 毎朝 6:40〜6:50 ランダム | **松村メッセージ**を要約 | 「いいね40〜50狙い型」（180〜235字・数字必須・【テーマ】見出し） | `どてっぱん/output/x_posts_batch6.xlsx`（第6弾）＋ 第7弾は `scratchpad/morning20.json`（正はX予約側） |
| **夕方枠** | 毎日 16:52〜17:10 ランダム | **西村自身の飲食現場ネタ**（12店舗・5年の実体験） | 「バズ狙いリスト型」（3選・情報格差フック・実体験数字） | `どてっぱん/output/x_posts_lunch_evening_50x2.xlsx` シート「夕方17時枠_50本」 |

- 朝枠は**会社の思想・マネジメント**（松村メッセージ由来）。
- 夕方枠は**「よくそんなこと知ってるね」路線**の業界裏側知識＋終盤はAI活用ネタ。
- 「飲食のプロが」など**プロ自称はしない**（おこがましいので不使用）。

### 在庫の現状（2026-10-03時点）

| | 予約済み範囲 | 残在庫 |
|---|---|---|
| X 朝枠 | 10/27 まで | 松村メッセージ未使用 vol **21本**（vol.325〜415 のうち未使用分）＋ 新着vol |
| X 夕方枠 | 10/29 まで | 「夕方17時枠_50本」の **No.26〜50（25本）** |
| Threads 朝・夕 | 10/8 まで（7日先までしか予約できない） | X と同文を順に転載するだけ |

---

## 2. 朝枠の文章を作る（松村メッセージ → X投稿）

### 2-1. ルールの正本

`~/Downloads/X投稿量産_引き継ぎドキュメント.md`（566行）。**作成前に必ず全文読む。** 要点だけ抜くと:

| 項目 | ルール |
|---|---|
| 文字数 | **180〜235字（平均210字）** |
| 見出し | 1行目は **【テーマ】**、空行、本文 |
| フック | **逆説型・宣言型**（「〜は、〇〇ではない」「〜は才能ではない」）。問いかけ型は減らす |
| 数字 | **全投稿に1つ以上**（12店舗、3ヶ月、70点、月30万、10秒 など） |
| CTA | **50本中5〜7本のみ**。それ以外は売り込まない |
| 禁止 | ハッシュタグ／絵文字／フック末尾の「…」 |
| トーン | 簡潔・静かな熱量・飲食の比喩（鉄板、仕込み、焼き加減、ガス点火） |
| 重複 | **1投稿＝1vol**。同じvol由来を連続させない |

### 2-2. 西村さん本人指定の言い回し（厳守）

1. 前職は「建設業」ではなく **「現場で施工管理」「現場監督」**
2. **「やなく／やない」禁止 → 「じゃなく／じゃない」**（関西弁の「あかん」「やろ」「やから」はOK）
3. 店舗規模のミニマムは **20坪**（想定20〜40坪）

### 2-3. 素材の取り方（毎日投稿されているURLから拾う）

素材は**ローカルのファイルではなく、公開サイト「綴」から取る**（2026-10-03 西村さん指示）。
別PCでもこのURLだけで完結する。

- サイト本体: **https://message.umapro-jp.com/**（うまプロカルチャー「綴」。松村メッセージが毎朝1本ずつ出る）
- データは2系統に分かれている:

| URL | 中身 | 件数の目安 |
|---|---|---|
| `https://message.umapro-jp.com/notes.js` | vol.1〜484。`window.NOTES = [ {vol, date, title, body}, … ]` の JS（新しい号が先頭） | 484本・約1MB |
| `https://message.umapro-jp.com/post.php` | **vol.485〜**。2026-09-30 以降サイトに直接投稿された分。`{"ok":true,"posts":[{id,date,time,title,body,…}]}` の JSON | 毎朝1本ずつ増える |

号数のつながり: post.php の投稿は保存時に号数を持たず、**notes.js の最大vol（484）の次から日付順に 485, 486, … と数える**。

```python
import json, re, urllib.request

# 1) vol.1〜484
js = urllib.request.urlopen('https://message.umapro-jp.com/notes.js').read().decode('utf-8')
notes = json.loads(re.search(r'window\.NOTES\s*=\s*(\[.*?\]);', js, re.S).group(1))
# notes[i] = {'vol': 484, 'date': '2026-09-29', 'title': '面白そう！を行動に変えろ', 'body': 'おはようございます！\n\n…'}

# 2) vol.485〜（サイト直接投稿分）
posts = json.load(urllib.request.urlopen('https://message.umapro-jp.com/post.php'))['posts']
posts.sort(key=lambda p: p['publish_ts'])
base = max(n['vol'] for n in notes)
for i, p in enumerate(posts, 1):
    p['vol'] = base + i          # 485, 486, …
# posts[j] = {'vol': 485, 'date': '2026-09-30', 'time': '05:35', 'title': '仕事を増やす改善は、改善じゃない', 'body': '…'}

allnotes = notes + posts
```

- `body` は「おはようございます！」から始まる本文そのまま。ここを要約して X 投稿にする。
- **使用済み vol を先に確認する。** 第1〜6弾で vol.100〜324 と、vol.325〜415 のうち第6弾50本＋第7弾20本を使用済み。
  未使用は vol.325〜415 の残り21本と、**vol.416 以降の新着**（2026-10-03 時点で vol.488 まで出ているので、未使用は約90本ある）。
- 使ったvolは Excel の「元vol」列（または作業用JSON）に残して、次回の重複防止に使う。
- ローカルの `~/umapro-culture/matsumura_notes.json` は元PCの作業用コピー。**別PCでは使わない**（URLが正）。

### 2-4. Excel出力

列は8列（No.／テーマ／投稿内容／元vol／フック型／CTA有無／投稿日／文字数）。
詳細は引き継ぎMDの5章。**日付列は実予約日と1日ズレていることがある**ので、予約時はX側の日付を正とする。

---

## 3. 夕方枠の文章を作る（飲食現場ネタ → バズ狙いリスト型）

出典シート: `x_posts_lunch_evening_50x2.xlsx` →「夕方17時枠_50本」。列は No.／テーマ／投稿内容／投稿日／時刻／文字数。

### 型（ノイモスAIのバズ分析から移植）

1. **情報格差フック**：「誰も教えてくれないけど」「知ってたら逆にすごい」「飲食側の人間がこっそり見てる」
2. **3選リスト**：①②③で3つ。TOP5は全部この型だった
3. **本物の有益情報で信頼を作って、自分を自然に挟む**（「12店舗の店長を見てきて」「飲食を5年やって」）
4. **実績数字**
5. **保存誘導**（「明日の朝①だけやってみてください」）

文字数は140〜160字程度（朝枠より短い）。削除済みテーマ: No.9「危ないFC本部の見分け方」（本人指示で不使用）。

### 新規で作るとき

No.26〜50 を使い切ったら、同じ型で新規作成。テーマ候補は「物件」「仕込み」「採用面接」「店長の1日」
「クレーム対応」「原価」「AI活用（売上予報・天気×POS・発注AI・口コミ返信）」。

---

## 4. X 予約投稿の登録手順

Chrome（@monja_no_KENT でログイン済み・Claude in Chrome 拡張ペアリング済み）で
`https://x.com/compose/post` を開いて1本ずつ登録する。

### 4-1. 本文入力は computer の `type` のみ

- `document.execCommand('insertText')` は **改行つき本文だと最終行しか保存されない**（8本やり直した実績）。
- `type` は **和文→半角数字の境目で1文字落ちる**ことがある。
  例:「仕事が速い人の共通点3つ」→ 「…共通点」で1回、「3つ】\n\n…」で2回目、と**境目で分割して type する**。
- 入力後、**先頭の【テーマ】が欠けていないか必ず目視**。

### 4-2. 日時の設定

1. `button[aria-label="Schedule post"]` をクリック
2. ダイアログの5つの `<select>`（月／日／年／時／分）に値を入れる。React なので普通の `.value=` は効かない:

```js
var set=Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set;
function pick(sel,val){set.call(sel,val);sel.dispatchEvent(new Event('input',{bubbles:true}));sel.dispatchEvent(new Event('change',{bubbles:true}));}
// SELECTOR_1..5 = 月・日・年・時・分
```

3. ダイアログを開いた直後は select が DOM に出ない。**最大12秒リトライ**する。
   screenshot と read_page を**同一 batch で撃つ**と accessibility tree に載る。
4. Confirm → Schedule。

### 4-3. 時刻のばらし方

- 朝枠: **6:40〜6:50** の間でランダム（毎日同じ分にしない）
- 夕方枠: **16:52〜17:10** の間でランダム

### 4-4. 予約一覧の確認・削除

- `x.com/compose/post/unsent/scheduled` で一覧。
- 一括削除は **1回5〜7件まで**しか消えない。全部消えるまで繰り返す。
- タブを長く使うと CDP の JS コンテキストが画面とズレて DOM が空に見える。**新しいタブを作り直す**と直る。

### 4-5. 登録後

- Excel ではなく **X予約一覧が正**。カレンダー登録は不要（一度作って全削除済み）。
- 登録した本数・期間・CTA日を報告する。

---

## 5. Threads 予約投稿（Xと同文を転載）

Threads **@doteppan_nishimuu**。Xの【】付きノウハウ投稿（朝・夕の2本）を**同日に同文**で出す。

### 5-1. 台帳

`~/x-like-tracker/threads/queue.json`
各要素: `{date, slot(am/pm), time, theme, text, status}`。`status` は posted / scheduled / draft / pending。

- 文章は X 側と同じ。朝枠は `x_posts_batch6.xlsx`、夕方枠は「夕方17時枠_50本」から。
- **Excel の日付は実投稿日より1日後**なので **−1日補正**して入れる。
- 時刻は 朝 **07:10**／夕 **17:30**。

### 5-2. 制限

- Threads の予約は**同時に25件まで**、かつ**7日先まで**しか選べない。
- だから**毎日のいいね実行のついでに、空いた枠（1日2件）を補充する**。
- **残りが3日分を切ったら、いいね報告に添えて自分から知らせる**（2026-09-27 西村さん指示）。

### 5-3. 登録手順（Threads Web）

1. `https://www.threads.com/` を開き、ログインが `a[href="/@doteppan_nishimuu"]` であることを確認。
2. 「新しいスレッド」（`[aria-label="新しいスレッド"]`）→ `[contenteditable="true"]` に本文。
   **cmd+V は効かない。** 合成 paste で入れる:

```js
var ta=document.querySelector('[contenteditable="true"]');ta.focus();
var dt=new DataTransfer();dt.setData('text/plain',txt);
ta.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));
```

3. 右上「…」（約 637,54）→「日時を指定...」（約 449,168）→ カレンダーで日付 → `<input type=text>` 2つ（時・分）→「完了」→「日時を指定」ボタン（約 578,275）。
   **メニュー類は JS の dispatchEvent が効かない。computer ツールの実クリックを使う。**
   座標はウィンドウサイズで変わるので、**予約作業中はウィンドウを触らない**。
4. 「JSTに投稿予定」のトーストを確認したら、queue.json の `status` を `scheduled` に更新してコミット。

### 5-4. 補充のときの手順

```
1. queue.json を見て status=pending の先頭2件（朝・夕）を取る
2. Threads で2本予約する
3. status を scheduled にして git commit / push
4. 残り日数を数えて、3日分を切っていれば報告に書く
```

### 5-5. 現状の課題（保留中）

Threads のフォロワーは **0のまま**（8月末から毎日2本転載しても増えていない）。
続けるなら Threads 側でいいね／返信の導線が別途必要、という論点は保留中。
※ 松村亮さんの Threads @mcdryo へ西村アカウントから毎朝いいねする運用は別チャット（`threads-mcdryo-like`）。

---

## 6. 毎回の報告フォーマット

```
**X予約 追加完了**
- 朝枠：10/28〜11/16 の20本（vol.xxx〜）、CTAは 11/1・11/9・11/15
- 夕方枠：10/30〜11/23 の25本（No.26〜50）
- 予約一覧で先頭【テーマ】の欠けなし確認済み
- 残在庫：朝枠 vol 未使用1本＋新着／夕方枠 0本（次回は新規作成）

**Threads予約 補充**
- 10/9朝・10/9夕 の2本を予約、queue.json 更新・push済み
- Threads予約は 10/9 まで（残り6日分）
```

---

## 7. 絶対にやらないこと

- **X本体の予約以外を「正」にしない**（Excel・JSONはあくまで台帳）
- 同じvol由来を2本作らない
- ハッシュタグ／絵文字／「…」終わり
- 「やなく／やない」「建設業」「飲食のプロが」
- CTAを50本中8本以上入れる
- `insertText` での本文入力（最終行しか残らない）
- Threads の本文に cmd+V（効かない）
- 定時実行・cronでの自動投稿（予約は X／Threads 本体の機能だけを使う）

---

## 8. 関連ファイル一覧

| 用途 | パス |
|---|---|
| 作成ルールの正本 | `~/Downloads/X投稿量産_引き継ぎドキュメント.md` |
| 一次素材（松村メッセージ） | **https://message.umapro-jp.com/notes.js**（vol.1〜484）＋ **https://message.umapro-jp.com/post.php**（vol.485〜） |
| 朝枠 第6弾 文案 | `~/どてっぱん/output/x_posts_batch6.xlsx` |
| 夕方枠 文案（50本） | `~/どてっぱん/output/x_posts_lunch_evening_50x2.xlsx` シート「夕方17時枠_50本」 |
| Threads 台帳 | `~/x-like-tracker/threads/queue.json`（README.md も同じ場所） |
| Threads 予約ヘルパー（旧） | `~/x-like-tracker/docs/mk_threads2.py` |
| いいね運用の指示書 | `~/x-like-tracker/docs/nishimura-x-like-instructions.md` |

※ `~/Downloads/` と `~/どてっぱん/output/` は **別PCには無い**。
最初に元PCからコピーするか、同じ場所に置いてから始める（`x-like-tracker` は git clone で取れる）。
松村メッセージは上のURLから取れるので、別PCへのコピーは不要。
