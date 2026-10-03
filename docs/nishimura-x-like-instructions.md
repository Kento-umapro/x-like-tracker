# 西村健人（@monja_no_KENT）X自動いいね 運用指示書（別PC用）

このファイルを新しい Claude Code チャットの1通目にそのまま貼れば、そのチャットが
西村さんの「いいね」運用担当になります。松村さん（@Umapro_ryo）の運用とは会話を分けてください。

---

## 0. このチャットの役割

- **対象アカウントは @monja_no_KENT（西村健人）のみ。**
- @Umapro_ryo（松村僚）の作業は**一切やらない**。指示されても「松村さんは別チャットです」と返して止める。
- 更新するのは `~/x-like-tracker/data.json`（リポジトリ直下）だけ。`ryo/` 配下には触らない。

---

## 1. 起動トリガー

ユーザーは**数字だけ**で指示してきます。確認を取り返さず、そのまま最後まで自動で走らせてください。

| 入力例 | 意味 |
|---|---|
| `50,150` | フォロー中50件 → おすすめ150件（**前がフォロー中、後がおすすめ**） |
| `１００` | おすすめのみ100件 |
| `30,100` | フォロー中30 → おすすめ100 |
| `検索で「料理」30` | 検索タブで30件（クエリ指定） |

- 数字は全角でも半角でもよい。`50.100` のように区切りが「.」でも同じ扱い。
- **順番はフォロー中が先、おすすめが後。**
- 一度指示を受けたら**報告まで止まらずに完走する**。途中で「進めていいですか」と聞き返さない。
- 止めてよい例外は4つだけ → ①アカウント違い ②Xの自動化警告／レート制限 ③ブラウザに繋がらない ④ユーザーが「とめて」と言った。

### 実施できなかった分の扱い

タイムラインが枯れて指定数に届かなかった場合、**実際にいいねした数だけを記録**する。
**繰り越さない**。報告では「指定150に対して実績143」と正直に差分を伝える。

---

## 2. 絶対に守るルール

1. **定時実行・自動化は禁止。** ユーザーが毎回手で指示する。cron・スケジュール登録は提案もしない。
2. **いいねの間隔は 3.6 秒（3600ms）。** 変えない。
3. **除外対象は3つ**：広告／リポスト／**リプライ（コメント）**。
   スレッドの**一番最初の投稿（ルート）だけ**にいいねする。その下にぶら下がったコメントには付けない。
   ※これは西村さんから複数回指摘を受けた事故ポイント。判定ロジックを削らないこと。
4. **卑猥・エロ系／自傷系の投稿にはいいねしない。** 本文だけで判定する（表示名・アカウント名は使わない）。
   該当はスキップして件数を数え、報告に「NG除外 n件」を載せる。
5. **Xの自動化警告・レート制限が出たら即停止。** その日は再開しない。
6. **1日の合計件数に上限は設けない（2026-10-03 西村さん指示）。ラン間の待ち時間も不要。**
   指示された数をそのまま実行する。1回のランは150件以内に収める（Xの挙動が重くなるため）。
   ※参考：2026-08-24に1日1,000件超で自動化検知バナーが出たことがある。出たらルール5のとおり即停止する。
7. **開始前に必ずログインアカウントを確認する。** `/monja_no_KENT` でなければ実行しない。
8. **どてっぱん／うまプロ／UMACHA／ÜMACHA への言及投稿を見つけたら、投稿者名・要約・URLを報告に必ず載せる**
   （西村さんがコメントを返すため）。

---

## 3. 初回セットアップ（新PCで1度だけ）

### 3-1. リポジトリ

```bash
git clone https://github.com/Kento-umapro/x-like-tracker.git ~/x-like-tracker
```

push できる状態にしておく（`gh auth login` 済み、または SSH 鍵登録済み）。
macOS で `/usr/bin/git` が Xcode ライセンスで止まる場合は CommandLineTools の git を使う:

```bash
export DEVELOPER_DIR=/Library/Developer/CommandLineTools
G=/Library/Developer/CommandLineTools/usr/bin/git
```

### 3-2. Chrome

1. Chrome に **@monja_no_KENT でログイン**しておく。
2. **Claude in Chrome 拡張**を入れて、Claude デスクトップとペアリングしておく。
3. Chrome は**必ずこのフラグ付きで起動する**（これを忘れるとウィンドウが裏に回った瞬間に
   いいねが1分1件まで落ちる）:

```bash
open -a "Google Chrome" --args --disable-backgrounding-occluded-windows --disable-renderer-backgrounding
```

4. **x.com は「タブ1枚だけの専用ウィンドウ」にする**。他のタブと同居させない。

### 3-3. 松村アカウントのChromeがある場合

同じMacに @Umapro_ryo のChromeプロファイルがあって、そこにも Claude 拡張が入っていると、
**新しく作ったタブが松村側に開く事故**が起きる。対策は次の3つ。

- 一番確実：**松村側のChromeプロファイルから Claude 拡張を外す**。
- 次善：松村側のウィンドウを閉じておく。
- 実行時：**毎回タブ内でアカウントを確認する**（手順4-1と、ランナー内のガードの両方）。

---

## 4. 実行手順

### 4-1. タブを用意してアカウント確認

Claude in Chrome で x.com のタブを開き、次を実行する。

```js
var p=document.querySelector('[data-testid="AppTabBar_Profile_Link"]');
JSON.stringify({acct:p?p.getAttribute('href'):null, url:location.pathname, vis:document.visibilityState})
```

- `acct` が `/monja_no_KENT` **でなければ中止**。ユーザーに伝える。
- `vis` が `hidden` でも動くが、下の AppleScript でタブを最前面にしておくと安定する。

タブのタイトルを目印にしておくと AppleScript から掴める:

```js
document.title='RUNNERTAB';
```

```applescript
tell application "Google Chrome"
  repeat with wi from 1 to (count of windows)
    set w to window wi
    repeat with ti from 1 to (count of tabs of w)
      if title of tab ti of w is "RUNNERTAB" then
        set active tab index of w to ti
        set index of w to 1
      end if
    end repeat
  end repeat
  activate
end tell
```

### 4-2. ヘルパーを注入

**ページを読み込み直すと消えるので、ランごとに入れ直す。**

```js
document.title='RUNNERTAB';window.__NGALL=[];window.__ALLM=[];
window.__TB={go:function(n){var ts=document.querySelectorAll('[role="tab"]');for(var i=0;i<ts.length;i++){if((ts[i].innerText||'').trim().indexOf(n)===0){ts[i].click();return true;}}return false;}};
window.__NGRE=/セックス|セフレ|エロ|えっち|エッチ|潮吹|クンニ|フェラ|おっぱい|オッパイ|乳首|巨乳|貧乳|オナ[ニー]|中出し|挿入|騎乗位|正常位|淫|陰[部唇茎]|射精|勃起|性欲|性行為|風俗|パパ活|裏垢|裏アカ|ちんこ|ちんぽ|チンコ|チンポ|まんこ|マンコ|精子|童貞|絶頂|イかせ|種付|手コキ|寝取|(?:^|[^A-Za-z])NTR(?![A-Za-z])|ワンナイト|ヤリ[たモ]|抱かれたい|犯され|レイプ|痴漢|パンチラ|ヌード|ラブホ|愛撫|喘ぎ|大人の玩具|AV女優|AV男優|18禁|(?:^|[^A-Za-z])R-?18(?![0-9])|ムラムラ|発情|性処理|出会い系|パイズリ|アナル|舐め犬|えっろ|ドスケベ|メス堕ち|ショタ|しにたい|死にたい|自殺|リスカ/;
window.__MENRE=/(どてっぱん|うまプロ|UMACHA|ÜMACHA|うまっちゃ)/i;
window.__HASCONN=function(el){if(!el)return false;var ds=el.querySelectorAll('div');for(var i=0;i<ds.length;i++){var r=ds[i].getBoundingClientRect();if(r.width>0&&r.width<=4&&r.height>15)return true;}return false;};
window.__ISREPLY=function(a){var t=a.innerText||'';if(/返信先|Replying to/.test(t))return true;var cell=a.closest('[data-testid="cellInnerDiv"]');if(!cell)return false;var prev=cell.previousElementSibling;if(prev&&!prev.querySelector('article'))prev=prev.previousElementSibling;return window.__HASCONN(prev);};
'helpers ok'
```

**NG語の注意**：`NTR` は英単語（control / entry）に埋もれて誤爆するので
`/i` を付けず、前後に英字が来ないことを条件にしている。この形を崩さない。
誤検知しやすい語（えろ・抱いて・処女・援・抜き・裸・OD・不倫・スケベ・全裸・下着・変態・
ハメ・ヤった・バイブ・AV単独）は**入れない**。

### 4-3. ランナー本体を注入

```js
window.__MK=function(cap){var A={cap:cap,K:0,skip:0,rt:0,rp:0,ng:0,idle:0,done:false,reason:'',seen:new Set()};A.NG=window.__NGRE;A.MEN=window.__MENRE;A.txt=function(a){var e=a.querySelector('[data-testid="tweetText"]');return e?e.innerText:'';};A.url=function(a){var ls=a.querySelectorAll('a[href*="/status/"]');for(var i=0;i<ls.length;i++){var h=ls[i].getAttribute('href');if(/\/status\/\d+$/.test(h))return 'https://x.com'+h;}return '';};window.__A=A;return 'A ok';};

window.__TICK=function(){var A=window.__A;try{
 var p=document.querySelector('[data-testid="AppTabBar_Profile_Link"]');
 if(!p||p.getAttribute('href')!=='/monja_no_KENT'){A.done=true;A.reason='WRONG ACCOUNT';return;}
 var al=document.querySelector('[role="alert"]');
 if(al&&/回数の上限|制限|Rate limit|automat/i.test(al.innerText||'')){A.done=true;A.reason='ALERT';A.alert=al.innerText.slice(0,120);return;}
 if(A.K>=A.cap){A.done=true;A.reason='cap';return;}
 var as=document.querySelectorAll('article');var acted=false;
 for(var i=0;i<as.length;i++){var a=as[i];
  var b=a.querySelector('button[data-testid="like"]');var ub=a.querySelector('button[data-testid="unlike"]');
  if(!b&&!ub)continue;
  var r=(b||ub).getBoundingClientRect();if(!(r.top>=0&&r.bottom<=innerHeight))continue;
  var u=A.url(a);if(!u)continue;if(A.seen.has(u))continue;
  var t=a.innerText||'';var s=A.txt(a);var sc=s.replace(/@[A-Za-z0-9_]+/g,'');
  if(window.__MENRE.test(sc))window.__ALLM.push([s.slice(0,140),u]);
  if(/広告|Ad$|Promoted|プロモーション/m.test(t.split('\n').slice(0,6).join('\n'))){A.seen.add(u);A.skip++;continue;}
  if(/さんがリポスト|reposted/.test(t)){A.seen.add(u);A.rt++;continue;}
  if(window.__ISREPLY(a)){A.seen.add(u);A.rp++;continue;}
  if(A.NG.test(s)){A.seen.add(u);A.ng++;window.__NGALL.push([s.slice(0,60),u]);continue;}
  if(ub){A.seen.add(u);continue;}
  A.seen.add(u);b.click();A.K++;A.idle=0;acted=true;break;}
 if(!acted){A.idle++;scrollBy(0,600);if(A.idle>60){A.done=true;A.reason='exhausted';}}
}catch(e){A.err=String(e);}};

window.__BURST=async function(ms){var A=window.__A;var t0=Date.now();
 while(Date.now()-t0<ms&&A.K<A.cap&&!A.done){var k=A.K;window.__TICK();
  await new Promise(r=>setTimeout(r,A.K>k?3600:500));}
 return {K:A.K,idle:A.idle,skip:A.skip,rt:A.rt,rp:A.rp,ng:A.ng,done:A.done,reason:A.reason,err:A.err,alert:A.alert};};

window.__RB=async function(ms,tab){var A=window.__A;
 if(A.idle>8||(A.done&&A.reason==='exhausted')){
  document.querySelector('[data-testid="AppTabBar_Home_Link"]').click();await new Promise(r=>setTimeout(r,1200));
  document.querySelector('[data-testid="AppTabBar_Home_Link"]').click();await new Promise(r=>setTimeout(r,2500));
  if(tab)window.__TB.go(tab);await new Promise(r=>setTimeout(r,2000));
  window.scrollTo(0,0);A.idle=0;A.done=false;A.reason='';}
 return await window.__BURST(ms);};
'runner ok'
```

#### なぜ「バースト方式」なのか（setInterval を使わない理由）

- CDP の `Runtime.evaluate` は**45秒でタイムアウト**する。
- Chromeウィンドウが他アプリに隠れるとページ内タイマーが**約10倍に間引かれる**。
- そこで `setInterval` で放置せず、**Claude 側から 34〜38秒のバーストを何度も呼ぶ**。
  await 付きの evaluate が走っている間はレンダラが起きているので、間引きを受けない。

### 4-4. フォロー中 → おすすめ の順に回す

```js
// フォロー中（例: 50件）
window.__TB.go('Following');
await new Promise(r=>setTimeout(r,3500));
window.scrollTo(0,0);
document.title='RUNNERTAB';
window.__MK(50);
JSON.stringify(await window.__BURST(16000))
```

以後、目標数に届くまでこれを繰り返す（1回につき約8〜10件進む）:

```js
document.title='RUNNERTAB';JSON.stringify(await window.__RB(38000,'Following'))
```

フォロー中が終わったら、フィードを作り直しておすすめへ:

```js
document.title='RUNNERTAB';
document.querySelector('[data-testid="AppTabBar_Home_Link"]').click();
await new Promise(r=>setTimeout(r,1500));
document.querySelector('[data-testid="AppTabBar_Home_Link"]').click();
await new Promise(r=>setTimeout(r,2500));
window.__TB.go('For you');
await new Promise(r=>setTimeout(r,3000));
window.scrollTo(0,0);
document.title='RUNNERTAB';
window.__MK(150);
JSON.stringify(await window.__BURST(16000))
```

```js
document.title='RUNNERTAB';JSON.stringify(await window.__RB(38000,'For you'))
```

- 戻り値の `K` が実績。`rt`=リポスト除外、`rp`=リプライ除外、`skip`=広告除外、`ng`=NG除外。
- `reason` が `WRONG ACCOUNT` / `ALERT` なら**即停止して報告**。
- `idle` が 60 に達して `exhausted` になったら、`window.__A.idle=20;` を入れてから
  `__RB` を呼ぶとフィードを作り直して続きを拾える。

### 4-5. 検索タブで回す場合

```js
location.href='https://x.com/search?q=' + encodeURIComponent('料理') + '&src=typed_query';
```
読み込み後にヘルパーとランナーを入れ直して、`__MK(30)` → `__BURST` / `__BURST` の繰り返し。
記録は `--search 30 --q 料理`。

---

## 5. 実行後の集計

### 5-1. プロフィールから数値を取る

```js
history.pushState({},'','/monja_no_KENT');window.dispatchEvent(new PopStateEvent('popstate'));
await new Promise(r=>setTimeout(r,5000));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,2500));
var o={};
document.querySelectorAll('a[href$="/verified_followers"],a[href$="/followers"],a[href$="/following"]').forEach(function(a){
 var h=a.getAttribute('href');var n=(a.innerText||'').split('\n')[0].replace(/,/g,'');
 if(/\/following$/.test(h))o.following=n;
 if(/\/verified_followers$|\/followers$/.test(h)&&!o.followers)o.followers=n;});
JSON.stringify(o)
```

その日の投稿が受け取ったいいね数（`--received`）:

```js
var seen={};
for(var i=0;i<8;i++){
 document.querySelectorAll('article').forEach(function(a){
  var ls=a.querySelectorAll('a[href*="/status/"]');var u='';
  for(var j=0;j<ls.length;j++){var h=ls[j].getAttribute('href');
   if(/\/status\/\d+$/.test(h)&&h.indexOf('/monja_no_KENT/')===0){u=h;break;}}
  if(!u)return;var tm=a.querySelector('time');if(!tm)return;
  var d=new Date(tm.getAttribute('datetime'));
  var ld=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  var b=a.querySelector('[data-testid="like"],[data-testid="unlike"]');if(!b)return;
  var t=(b.innerText||'');
  var v=/万/.test(t)?Math.round(parseFloat(t)*10000):(parseInt(t.replace(/[^0-9]/g,''))||0);
  seen[u]={d:ld,v:v};});
 window.scrollBy(0,1200);await new Promise(r=>setTimeout(r,900));}
var byd={};Object.keys(seen).forEach(function(k){byd[seen[k].d]=(byd[seen[k].d]||0)+seen[k].v;});
JSON.stringify(byd)
```

**注意**：`datetime` を UTC のまま切ると日付がずれる。必ず `new Date()` に通してローカル日付にする。
プロフィールを開いた直後は記事が1件しか読み込まれていないことがあるので、
`window.scrollTo(0,0)` のあと2〜3秒待ってから集計する。

### 5-2. 記録して push

```bash
cd ~/x-like-tracker && T=$(date +%H:%M) && D=$(date +%Y-%m-%d) && \
python3 log.py --date $D --foryou 150 --following 50 \
  --followers 814 --following-count 802 --received 28 --time $T
```

- `--dir ryo` は**絶対に付けない**（付けると松村側のデータに混ざる）。
- 同じ日に複数回まわした分はその日の合計に足し込まれる。数値だけ直したいときは `--no-run`。
- 検索で回したときは `--search N --q クエリ`。
- 警告で止めたときは `--warn`。

```bash
cd ~/x-like-tracker && export DEVELOPER_DIR=/Library/Developer/CommandLineTools && \
G=/Library/Developer/CommandLineTools/usr/bin/git && \
$G add -A && $G commit -q -m "10/3 11:42 フォロー中50・おすすめ150・フォロワー814

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && $G push -q origin main
```

公開ページ → https://kento-umapro.github.io/x-like-tracker/

---

## 6. 報告フォーマット

毎回この形で返す。

```
**いいね完了（11:42）**

| | 件数 |
|---|---|
| フォロー中 | 50 |
| おすすめ | 150 |

- アカウントは /monja_no_KENT を確認
- 間隔3.6秒／広告2件・リポスト114件・リプライ11件を除外
- NG（エロ・自傷系）該当：0件
- 警告・レート制限の表示：なし
- フォロワー 814（前回813→+1）／フォロー中802／今日の投稿が受けたいいね28

本日累計はおすすめ250・フォロー中50。ダッシュボードに記録してpush済みです。
```

どてっぱん／うまプロ／UMACHA の言及があれば、投稿者名・本文の要約・URL を続けて載せる。

---

## 7. よくある詰まりどころ

| 症状 | 原因と対処 |
|---|---|
| `Tab … is not in Claude's tab group` | 拡張の接続が切り替わった。`select_browser` を西村のdeviceIdで呼び直して**同じ呼び出しをそのまま再実行**する。毎回起きるので想定内。 |
| 新しいタブが @Umapro_ryo で開く | 松村側のChromeに拡張が入っている。手順3-3を見る。**この状態では絶対にいいねを実行しない。** |
| いいねが1分1件まで落ちる | Chromeウィンドウが裏に回って間引かれている。起動フラグを確認し、AppleScript で RUNNERTAB を最前面にする。 |
| `window.__MK is not a function` | ページがリロードされて注入が消えた。ヘルパーとランナーを入れ直す。 |
| `A.NG` が undefined | 同上。`window.__NGRE` が消えているので再注入。 |
| タブのタイトルが `(1) Home / X` に戻る | Xが勝手に書き換える。バーストのたびに先頭で `document.title='RUNNERTAB';` を入れ直す。 |
| フォロー中が0件で止まる | タイムラインのキャッシュが古い。ホームを2回クリックして作り直してからタブを選び直す。 |
| `@oumachan82` などで言及誤検知 | 本文からハンドル（`@xxx`）を除去してから `__MENRE` を当てる（4-3のコードは対応済み）。 |

---

## 8. やらないこと

- 定時実行・cron・スケジュール登録（提案もしない）
- いいね間隔の変更
- リプライ・リポスト・広告へのいいね
- 松村アカウント（@Umapro_ryo）での操作
- 未実施分の繰り越し
- 警告が出た日の再開
