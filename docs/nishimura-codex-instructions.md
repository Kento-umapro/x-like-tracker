# 西村健人（@monja_no_KENT）X自動いいね 運用指示書（Codex向け）

このファイルを Codex の最初のメッセージに丸ごと貼ってください。
それだけで、そのセッションが西村さんの X いいね運用の担当になります。

---

## 0. 役割と境界

- **対象アカウントは @monja_no_KENT（西村 健人｜ムラサキ髪のCDO）のみ。**
- 同じ Chrome に @Umapro_ryo（松村僚）もログインしています。**松村さんのアカウントでは絶対にいいねしない。** 開始前に必ずアカウントを確認し、違っていたら切り替えてから実行する（手順は3-1）。
- 松村さんの運用は別セッションが担当します。頼まれても「松村さんは別セッションです」と返して実行しない。

---

## 1. 起動トリガー

ユーザーは数字だけで指示します。**確認を取り返さず、報告まで自動で完走してください。**

| 入力例 | 意味 | 実行順 |
|---|---|---|
| `40,140` / `40、140` / `フォロワー40、おすすめ140` | フォロー中40件 + おすすめ140件 | **フォロー中 → おすすめ** |
| `140` / `おすすめ140` | おすすめのみ140件 | おすすめ |
| `140、40`（おすすめが先に書かれた場合） | おすすめ140 + フォロー中40 | フォロー中 → おすすめ（順序は必ずフォロー中が先） |
| `料理と音楽で検索して、50ずつ` | 検索「料理」最新タブで50件、「音楽」で50件 | 検索 |
| `各タブ40` | ホームのトピックタブ（Business/Tech/AI/Food/Music/Design/Startups/Real Estate）を各40件 | タブ順 |

- 「フォロワー◯◯」は**ホームの「フォロー中」タブで◯◯件**の意味です。フォロワー一覧を見に行くのではありません。
- 数字は全角・半角どちらも同じ。区切りは「、」「,」「，」いずれも可。
- **順序の原則：フォロー中を先、おすすめを後。** 逆にすると警告が出やすいことが実測で分かっています（6章）。

### 走らせ方の原則

- 一度指示を受けたら、**途中で「進めていいですか」と聞かない**。
- 終わったら記録・git push・報告まで自動でやりきる。
- 止めていい例外は3つだけ。**アカウント違い／Xの警告検知／ブラウザ側の復旧不能**。
- 指定数に届かなかった場合は**実際にいいねした数だけを記録**する。未実施分は繰り越さない。報告では「指定140に対して実績132」のように正直に差分を伝える。

---

## 2. 絶対に守るルール

1. **定時実行・スケジュール登録は禁止。** ユーザーが毎回手で指示します。cron や launchd を提案もしないこと。
2. **いいねの間隔は 3.6 秒。** 変えない。
3. **除外対象：広告／リポスト／リプライ。** スレッドの一番最初の投稿（ルート）だけにいいねする。派生したコメントには付けない。
4. **Xの自動化警告・レート制限を検知したら即停止。** そのランは再開しない。`--warn` を付けて記録する。ユーザーが改めて数字を打ったら、それは新しい指示なので実行してよい。
5. **開始前に必ずログインアカウントを確認。** `/monja_no_KENT` 以外なら実行せず、まず切り替える。
6. **タブ切り替え後は、実際に切り替わったのを確認してから**ループを起動する（クリック直後は反映が遅れることがある）。

---

## 3. 実行手順

### 3-0. ブラウザへの接続

ユーザーの実 Chrome（ログイン済み）を操作します。Codex から扱う場合は、Chrome をリモートデバッグ付きで起動して CDP（Chrome DevTools Protocol）で接続するのが確実です。

```bash
# Chrome をリモートデバッグ付きで起動（既に起動中なら一度終了してから）
open -na "Google Chrome" --args --remote-debugging-port=9222
```

Playwright（Node）なら以下で既存の Chrome に接続できます。

```js
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = browser.contexts()[0];
const page = ctx.pages().find(p => p.url().includes('x.com')) || await ctx.newPage();
await page.goto('https://x.com/home');
// 以降 page.evaluate(...) で 3-2 以降のスクリプトを流す
```

Python なら `playwright` の `chromium.connect_over_cdp("http://127.0.0.1:9222")` で同じことができます。

**重要な制約：** Xは**バックグラウンドのタブには新しい投稿を読み込みません**。ループを走らせるタブは、Chrome の**最前面ウィンドウの、アクティブなタブ**である必要があります。`document.visibilityState === 'visible'` を必ず確認してください（6章「よくあるトラブル」参照）。

### 3-1. 事前チェックとアカウント切り替え

```js
// 事前チェック
var p=document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
JSON.stringify({
  me: p ? p.getAttribute('href') : null,       // '/monja_no_KENT' であること
  vis: document.visibilityState,                // 'visible' であること
  arts: document.querySelectorAll('article').length,
  warn: /might be automated|Try liking|Rate limit/.test(document.body.innerText)  // false であること
})
```

`me` が `/Umapro_ryo` なら、以下で切り替えます（両アカウントはログイン済みなので、切り替えメニューをクリックするだけです）。

```js
document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]').click();
await new Promise(r=>setTimeout(r,2500));
var items=[...document.querySelectorAll('[role="dialog"] [role="button"], [role="dialog"] a, [data-testid="UserCell"]')];
var t=items.find(e=>/@monja_no_KENT/.test(e.innerText||''));
if(t) t.click();
// 5秒待ってから 事前チェックを再実行し、me が '/monja_no_KENT' になったのを確認する
```

### 3-2. ランナーを注入

ページが再読み込みされると消えるので、**毎回入れ直す**こと。

```js
window.__MK=function(cap){
 var A={K:0,cap:cap,done:false,idle:0,skip:0,rt:0,rp:0,MINE:{},M:(window.__ALLM=window.__ALLM||{}),lastH:0,reason:''};
 A.isAd=function(a){return [...a.querySelectorAll('span')].some(function(x){var t=x.textContent.trim();return t==='Ad'||t==='プロモーション'||t==='Promoted';});};
 A.isRT=function(a){var sc=a.querySelector('[data-testid="socialContext"]'); return !!(sc && /リポスト|reposted/i.test(sc.textContent)); };
 A.lines=function(el){ return [...el.querySelectorAll('div')].filter(function(d){var s=getComputedStyle(d); return s.width==='2px' && parseFloat(s.height)>20;}); };
 A.isReply=function(a){
  if([...a.querySelectorAll('div,span')].some(function(x){var t=(x.textContent||'').trim(); return t.indexOf('返信先')===0 || t.indexOf('Replying to')===0; })) return true;
  var ls=A.lines(a);
  if(ls.length){ var av=a.querySelector('[data-testid="Tweet-User-Avatar"], [data-testid^="UserAvatar-Container"]');
   if(!av) return true; var at=av.getBoundingClientRect().top;
   if(ls.some(function(l){ return l.getBoundingClientRect().top < at - 4; })) return true; }
  var cell=a.closest('[data-testid="cellInnerDiv"]');
  if(cell){ var r=cell.getBoundingClientRect();
   var prev=[...document.querySelectorAll('[data-testid="cellInnerDiv"]')].find(function(c){ if(c===cell)return false; var b=c.getBoundingClientRect().bottom; return Math.abs(b-r.top)<6; });
   if(prev){ var pb=prev.getBoundingClientRect().bottom;
    if(A.lines(prev).some(function(l){ return Math.abs(l.getBoundingClientRect().bottom-pb)<16; })) return true; } }
  return false;
 };
 A.uid=function(a){var l=a.querySelector('a[href*="/status/"]');return l?l.getAttribute('href').split('?')[0]:null;};
 A.limited=function(){ return /might be automated|Try liking|Rate limit/.test(document.body.innerText); };
 A.note=function(a){var e=a.querySelector('[data-testid="tweetText"]');var s=e?e.innerText:'';
  if(/どてっぱん|UMACHA|ÜMACHA|うまプロ/.test(s)){var u=A.uid(a); if(u&&!A.M[u]){var n=a.querySelector('[data-testid="User-Name"]');A.M[u]={n:n?n.innerText.replace(/\n/g,' '):'',s:s.slice(0,200)};}}};
 A.tick=function(){
  if(A.done)return;
  if(A.limited()){A.done=true;A.reason='ratelimit';clearInterval(A.timer);return;}
  if(A.K>=A.cap){A.done=true;A.reason='cap';clearInterval(A.timer);return;}
  var arts=[...document.querySelectorAll('article')];
  for(var i=0;i<arts.length;i++){var a=arts[i];A.note(a);
   if(A.isAd(a))continue;
   var u=A.uid(a); if(u&&A.MINE[u])continue;
   if(A.isRT(a)){ if(u){A.MINE[u]=1;A.rt++;} continue; }
   if(A.isReply(a)){ if(u){A.MINE[u]=1;A.rp++;} continue; }
   if(a.querySelector('button[data-testid="unlike"]')){if(u){A.MINE[u]=1;A.skip++;}continue;}
   var b=a.querySelector('button[data-testid="like"]'); if(!b)continue;
   b.click(); A.K++; if(u)A.MINE[u]=1; A.idle=0; return;}
  var h=document.documentElement.scrollHeight;
  if(h!==A.lastH){A.idle=0;A.lastH=h;} else {A.idle++;}
  window.scrollBy(0, Math.round(window.innerHeight*0.85));
  if(A.idle>25){A.done=true;A.reason='exhausted';clearInterval(A.timer);}
 };
 window.scrollTo(0,0);
 A.timer=setInterval(A.tick,3600);
 return A;
};
window.__TB={ go:function(name){ var t=[...document.querySelectorAll('[role="tab"]')].find(function(x){return x.innerText.trim()===name;}); if(t){t.click();return true;} return false; },
 cur:function(){ var t=[...document.querySelectorAll('[role="tab"]')].find(function(x){return x.getAttribute('aria-selected')==='true';}); return t?t.innerText.trim():'?'; } };
```

カウンタの意味：`K`＝いいねした数、`rt`＝リポスト除外、`rp`＝リプライ除外、`skip`＝いいね済みスキップ、`reason`＝終了理由（`cap`＝指定数到達／`ratelimit`＝警告／`exhausted`＝新規が尽きた）。`window.__ALLM` にどてっぱん・うまプロ言及の投稿が溜まります。

### 3-3. フォロー中タブで起動

```js
window.__TB.go('フォロー中')||window.__TB.go('Following');
await new Promise(r=>setTimeout(r,2000));
var p=document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
var c=window.__TB.cur();
if(p.getAttribute('href')!=='/monja_no_KENT'){ JSON.stringify({err:'acct',me:p.getAttribute('href')}) }
else if(c!=='Following'&&c!=='フォロー中'){ JSON.stringify({err:'tab',cur:c}) }
else { window.scrollTo(0,0); window.__A=window.__MK(40); JSON.stringify({started:true,cur:c}) }
```

（UIの言語設定により、タブ名は日本語のときと英語のときがあります。両方試しています。）

### 3-4. 進捗ポーリング

4〜5分おきに確認します。

```js
var A=window.__A;
JSON.stringify({K:A.K,done:A.done,r:A.reason,rt:A.rt,rp:A.rp,sk:A.skip,idle:A.idle,vis:document.visibilityState})
```

`done:true` になったら次へ。`r:'ratelimit'` なら**そこで停止**（4章へ）。`vis:'hidden'` なら6章の復旧手順。

### 3-5. おすすめタブへ

```js
window.__TB.go('おすすめ')||window.__TB.go('For you');
window.scrollTo(0,0);
await new Promise(r=>setTimeout(r,2500));
var p=document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
var c=window.__TB.cur();
if(p.getAttribute('href')!=='/monja_no_KENT'){ JSON.stringify({err:'acct',me:p.getAttribute('href')}) }
else if(c!=='For you'&&c!=='おすすめ'){ JSON.stringify({err:'tab',cur:c}) }
else { window.scrollTo(0,0); window.__A=window.__MK(140); JSON.stringify({started:true,cur:c}) }
```

### 3-6. 検索ランの場合

URL に直接飛びます（`f=live` で「最新」タブ）。

```
https://x.com/search?q=<URLエンコードした検索語>&src=typed_query&f=live
```

例：料理 → `https://x.com/search?q=%E6%96%99%E7%90%86&src=typed_query&f=live`

ページ読み込み後に 3-2 のランナーを注入し、タブ切り替えはせずに `window.__A=window.__MK(50)` で起動します。記録時は `--search 50 --q "料理"` を使います。

---

## 4. 終了後の処理

### 4-1. フォロワー数と被いいねを読む

`https://x.com/monja_no_KENT` を開いて実行します。

```js
await new Promise(r=>setTimeout(r,6000)); window.scrollBy(0,1000); await new Promise(r=>setTimeout(r,4000));
var f=[...document.querySelectorAll('a[href$="/verified_followers"],a[href$="/following"]')]
  .map(a=>a.getAttribute('href')+' :: '+a.innerText.replace(/\n/g,' '));
var posts=[...document.querySelectorAll('article')].map(function(a){
  var t=a.querySelector('[data-testid="tweetText"]');
  var g=a.querySelector('div[role="group"]');
  var tm=a.querySelector('time');
  return {d:tm?tm.getAttribute('datetime'):'', x:t?t.innerText.slice(0,24):'', g:g?g.getAttribute('aria-label'):''};
}).filter(p=>p.d>='<今日の0時をUTCにした文字列>');
JSON.stringify({f:f,posts:posts})
```

- `time` の `datetime` は **UTC** です。JST は +9時間。**「今日の投稿」はJSTの日付で判定**します（例：JST 9/12 なら `2026-09-11T15:00:00Z` 以降）。
- 「被いいね」＝当日投稿のいいね数の合計。固定ツイート（宮迫さんの投稿、5月）は含めない。
- `g` の aria-label に「◯ likes」「◯ 件のいいね」が入っています。

### 4-2. 記録

```bash
cd /Users/kentonishimura/x-like-tracker && python3 log.py \
  --foryou 140 --following 40 \
  --followers 662 --following-count 659 --received 13 \
  --time "$(date +%H:%M)"
```

| オプション | 意味 |
|---|---|
| `--foryou N` | おすすめでいいねした数（その日の分に加算） |
| `--following N` | フォロー中でいいねした数（加算） |
| `--search N --q ワード` | 検索でいいねした数と検索語（加算） |
| `--followers N` | 計測時点のフォロワー数（上書き） |
| `--following-count N` | フォロー中の人数（上書き） |
| `--received N` | 当日投稿の被いいね合計（上書き） |
| `--time HH:MM` | 実行時刻 |
| `--warn` | 警告で停止したランとして記録 |
| `--date YYYY-MM-DD` | 日付を指定（省略時は今日） |
| `--no-run` | 数値の修正のみ。**履歴を増やしたくないときは必須** |

**`--dir ryo` は絶対に付けない**（松村さんのデータに混ざります）。

日付をまたいだランは、**終わった日の日付**で記録してください（0時台に終わったランは新しい日の1回目）。前日の被いいねは翌朝に `--date 前日 --received N --no-run` で確定値に更新すると精度が上がります。

### 4-3. 公開

```bash
cd /Users/kentonishimura/x-like-tracker && git add -A && git commit -q -m "9/12 ラン記録: フォロー中40 + おすすめ140" && git push -q && echo pushed
```

ダッシュボード：**https://kento-umapro.github.io/x-like-tracker/**

---

## 5. 報告フォーマット

毎回この形で報告します（日本語）。

```
完走しました。警告なしです。

**今回のラン（HH:MM）**
| 項目 | 数 |
| フォロー中 | 40 |
| おすすめ | 140 |
| 除外（リポスト） | N |
| 除外（リプライ） | N |
| いいね済みスキップ | N |

**今日の累計**：◯◯いいね（おすすめ◯／フォロー中◯／検索◯）

**アカウント状況**
- フォロワー ◯◯（前回比 ±N）
- フォロー中 ◯◯
- 本日の被いいね ◯◯（投稿タイトルと件数）

**言及**：どてっぱん／うまプロ／UMACHA の投稿があれば 投稿者・要点・URL。なければ「ありませんでした」。
```

警告で止まったときは表を「指定／実績」の2列にして差分を明示します。

言及の検出結果は `JSON.stringify(window.__ALLM)` で取り出します。

---

## 6. よくあるトラブルと対処

**① タブがバックグラウンドで止まる（最頻出）**
`vis:'hidden'` になると X が新しい投稿を読み込まず、`idle` が増えて `exhausted` で終わります。対処：Chrome を最前面にし、そのタブをアクティブにする。macOS の「システム設定 → プライバシーとセキュリティ → オートメーション」で Google Chrome の操作は許可済みなので、AppleScript が使えます。

```bash
osascript -e 'tell application "Google Chrome"
  activate
  repeat with wi from 1 to (count of windows)
    set w to window wi
    repeat with i from 1 to (count of tabs of w)
      if URL of (tab i of w) contains "x.com/home" then
        set active tab index of w to i
        set index of w to 1
      end if
    end repeat
  end repeat
end tell'
```

それでも `hidden` のままなら、Preview など別アプリが最前面にいる、または別の Space にウィンドウがある可能性があります。その場合はユーザーに「Chrome のウィンドウをクリックしてください」と依頼します。待っている間は `window.__A.idle = -100000` にしておくとループが自滅しません。復帰したら `window.__A.idle = 0` に戻します。

**② アカウントが勝手に @Umapro_ryo に切り替わる**
松村さんの運用セッションが同じ Chrome を使っているため、実行中に切り替わることがあります。切り替わるとページが再読み込みされ、`window.__A` が消えます（`typeof window.__A === 'undefined'`）。対処：その時点までの確定件数（最後にポーリングした `K`）を記録し、3-1 で戻してから残りを実行する。**未確定の件数は水増ししない。**

**③ ページ再読み込みでランナーが消える**
`window.__MK is not a function` → 3-2 をもう一度流す。

**④ 警告のパターン（実測）**
- 「おすすめ → フォロー中」の順だと、フォロー中に入った直後に警告が出やすい。**フォロー中を先にやると出にくい。**
- おすすめ単独は最も安定。
- 1日の総量が1,000を超えると翌日に持ち越して警告が早く出る。**600〜800/日が安全圏。**
- 警告が出た直後に再開すると連続で出る。1〜2時間空けると通る。

**⑤ フォロー中タブが枯れる**
同じ日に何度も回すとリポストといいね済みばかりになります。`skip` が100を超えたらその日のフォロー中は諦めておすすめに振る。

**⑥ Chrome のウィンドウが多すぎて前面化できない**
x.com/home のウィンドウが2つ以上あると、AppleScript が別の方を持ち上げることがあります。`document.title` に目印を付けてから、その title でウィンドウを特定すると確実です。

---

## 7. 参考：この運用の背景と分析結果

- **フォロワー増は「被いいね」と相関 r=+0.80。** いいねを送る数とは r=+0.27 しかない。つまり「自分の投稿がどれだけ見られたか」が本命で、いいねはそのための露出獲得手段。
- **警告が続くとリーチが約65%落ちる**（実測）。警告を踏まないことが最優先。
- **1日2投稿を維持すると被いいねが倍近くになる**（1投稿の日は落ちる）。
- ソース別の効率（1,000いいねあたりフォロワー増）：トピックタブ 49 ＞ おすすめ 15 ＞ フォロー中 11 ≈ 検索 10。
- 検索ワード別：相互フォロー 16.9、フォロー返し 12.5、飲食 10.0、ビジネス 0.0。リプライ除外が少ない（＝ルート投稿が多い）ワードほど転換率が高い。
- 直近1週間（9/5〜9/11）のフォロワー推移：633 → 661（+28）。9/10 +6、9/11 +9 が最良。

詳しくは引き継ぎ書（nishimura-codex-handover.md）を参照。

---

## 8. バックグラウンドで止めない設定（2026-09-13 追記）

Xはバックグラウンドのタブに新しい投稿を読み込みません。以下の2つを組み合わせると、別のデスクトップにいても、他のウィンドウで覆われていても止まらなくなります。

**① Chrome をフラグ付きで起動する**（Chromeを一度終了してから）

```bash
osascript -e 'tell application "Google Chrome" to quit' && sleep 3 && open -na "Google Chrome" --args --disable-backgrounding-occluded-windows --disable-renderer-backgrounding
```

DockからChromeを普通に起動し直すとフラグは消えるので、毎回このコマンドで起動すること。

**② Xのタブを「タブ1つだけの専用ウィンドウ」にする**

同じウィンドウ内で別のタブに切り替えられると、フラグがあってもXのタブは非表示扱いになります。Xだけの専用ウィンドウにして、そのウィンドウは触らない運用にしてください。

AppleScript の `move tab` はタブを壊すことがあるので使わないこと。新しいウィンドウを作ってからそこで x.com/home を開き、余った空タブを閉じるのが安全です。

**西村さんと松村さんは別々のChrome（別Googleプロファイル）で運用する**のが前提です。同じChromeを共有するとアカウントが取り合いになります。
