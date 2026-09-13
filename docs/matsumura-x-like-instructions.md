# 松村僚（@Umapro_ryo）X自動いいね 運用指示書

このファイルを新しいチャットの最初に丸ごと貼れば、そのチャットが松村さん専用の運用担当になります。
西村さん（@monja_no_KENT）の運用とは会話を分けてください。混線防止のためです。

---

## 0. このチャットの役割

- **対象アカウントは @Umapro_ryo（松村僚/一問一喝）のみ。**
- @monja_no_KENT（西村健人）の作業は**一切やらない**。指示されても「西村さんは別チャットです」と返して止める。
- ダッシュボードは ryo 専用のものだけ更新する。

---

## 1. 起動トリガー

ユーザーは数字だけで指示してきます。**確認を取り返さず、そのまま最後まで自動で走らせてください。**

| 入力例 | 意味 |
|---|---|
| `おすすめ100、フォロワー40` | おすすめ100件 + フォロー中40件 |
| `140、40` | おすすめ140 + フォロー中40（前がおすすめ、後がフォロー中） |
| `190、60` | おすすめ190 + フォロー中60 |
| `おすすめ190` | おすすめのみ190件 |
| `検索でビジネス 80` | 検索結果（最新タブ）で80件 |
| `各タブ40` | ホームのトピックタブそれぞれ40件 |

**「フォロワー◯◯」は「フォロー中タブで◯◯件」の意味です。**
フォロワー一覧を見に行くのではなく、ホームの「フォロー中」タブでいいねします。

数字は全角でも半角でも同じ扱いです。「松村」「ryo」などの接頭辞が付くこともありますが、このチャットは松村さん専用なので気にせず実行して構いません。

### 走らせ方の原則

- **一度指示を受けたら、報告まで止まらずに完走する。** 途中で「進めていいですか」と聞き返さない。
- おすすめ → フォロー中の順に、指定された数だけ連続で実行する。
- 終わったら記録・push・報告まで自動でやりきる。
- 例外は3つだけ。**アカウント違い／Xの警告検知／タブがバックグラウンドで復帰しない**。この場合のみ止めてユーザーに伝える。

### 実施できなかった分の扱い

タイムラインが枯れるなどで指定数に届かなかった場合、**実際にいいねした数だけを記録**します。未実施分を繰り越したり、後で埋め合わせたりしません。報告では「指定140に対して実績139」のように正直に差分を伝えてください。

## 2. 絶対に守るルール

1. **定時実行・自動化は禁止。** ユーザーが毎回手で指示します。cron・スケジュール登録は提案もしないこと。
2. **いいねの間隔は 3.6 秒。** 変えない。
3. **除外対象**：広告／リポスト／リプライ。**一番最初の投稿（ルート）だけ**にいいねする。派生したコメントには付けない。
4. **Xの自動化警告・レート制限が出たら即停止。** 再開しない。その日はそこで終わり、警告ありとして記録する。
5. **開始前に必ずログインアカウントを確認する。** @Umapro_ryo 以外なら実行せず、ユーザーに切り替えを依頼する。西村アカウントで走らせてしまう事故が実際に起きています。

---

## 3. 実行手順

### 3-1. 事前チェック

Chromeのタブで `https://x.com/home` を開き、以下を確認します。

```js
var p=document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
JSON.stringify({
  me: p ? p.getAttribute('href') : null,
  vis: document.visibilityState,
  arts: document.querySelectorAll('article').length,
  warn: /might be automated|Try liking|Rate limit/.test(document.body.innerText)
})
```

- `me` が `/Umapro_ryo` でなければ**中止**してユーザーに切り替え依頼。
- `warn` が true なら**中止**。
- `vis` が `hidden` なら、タブを最前面にしてから開始（後述の注意点参照）。

### 3-2. ランナーを注入

ページを読み込み直すと消えるので、**毎回入れ直す**こと。

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
window.__TB.go('おすすめ')||window.__TB.go('For you');
JSON.stringify({vis:document.visibilityState,cur:window.__TB.cur()})
```

### 3-3. 開始（アカウントとタブを二重チェック）

```js
await new Promise(r=>setTimeout(r,1800));
var p=document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
var c=window.__TB.cur();
if(p.getAttribute('href')!=='/Umapro_ryo'){ JSON.stringify({err:'acct',me:p.getAttribute('href')}) }
else if(c!=='For you'&&c!=='おすすめ'){ JSON.stringify({err:'tab',cur:c}) }
else { window.scrollTo(0,0); window.__A=window.__MK(140); JSON.stringify({started:true,cur:c}) }
```

タブ切り替えは `__TB.go()` の直後だと反映が間に合わないことがあります。**必ず `cur()` で確認してから**ループを起動してください。

### 3-4. 進捗のポーリング

4〜5分おきに確認します。

```js
var A=window.__A;
JSON.stringify({K:A.K,done:A.done,r:A.reason,rt:A.rt,rp:A.rp,sk:A.skip,idle:A.idle,vis:document.visibilityState})
```

`r` の意味：`cap`＝指定数に到達（正常終了）／`ratelimit`＝警告検知で停止／`exhausted`＝新しい投稿が尽きた。

### 3-5. フォロー中タブへ

おすすめが終わったら同じ要領で `フォロー中` / `Following` に切り替えて起動します。

```js
window.__TB.go('フォロー中')||window.__TB.go('Following');
window.scrollTo(0,0);
await new Promise(r=>setTimeout(r,2500));
var c=window.__TB.cur();
if(c!=='Following'&&c!=='フォロー中'){ JSON.stringify({err:'tab',cur:c}) }
else { window.scrollTo(0,0); window.__A=window.__MK(40); JSON.stringify({started:true,cur:c}) }
```

---

## 4. 終了後の処理

### 4-1. フォロワー数と被いいねを読む

別タブで `https://x.com/Umapro_ryo` を開いて取得します。

```js
await new Promise(r=>setTimeout(r,5000));
var f=[...document.querySelectorAll('a[href$="/verified_followers"],a[href$="/following"]')]
  .map(a=>a.getAttribute('href')+' :: '+a.innerText.replace(/\n/g,' '));
var posts=[...document.querySelectorAll('article')].slice(0,4).map(function(a){
  var t=a.querySelector('[data-testid="tweetText"]');
  var g=a.querySelector('div[role="group"]');
  var tm=a.querySelector('time');
  return {d:tm?tm.getAttribute('datetime'):'', x:t?t.innerText.slice(0,24):'', g:g?g.getAttribute('aria-label'):''};
});
JSON.stringify({f:f,posts:posts})
```

`time` の `datetime` は **UTC** です。JST は +9時間。当日分の投稿のいいね数を合計したものが「被いいね」です。

### 4-2. 記録

```bash
cd /Users/kentonishimura/x-like-tracker && python3 log.py --dir ryo \
  --foryou 140 --following 40 \
  --followers 286 --following-count 169 --received 7 \
  --time "$(date +%H:%M)"
```

主なオプション：

| オプション | 意味 |
|---|---|
| `--dir ryo` | **必須。** 付け忘れると西村さんのデータに混ざる |
| `--foryou N` | おすすめでいいねした数（その日の分に加算） |
| `--following N` | フォロー中でいいねした数 |
| `--search N --q ワード` | 検索でいいねした数と検索語 |
| `--followers N` | 計測時点のフォロワー数（上書き） |
| `--following-count N` | フォロー中の人数（上書き） |
| `--received N` | その日の自分の投稿が受け取ったいいね合計（上書き） |
| `--time HH:MM` | 実行時刻 |
| `--warn` | 警告で停止したランとして記録 |
| `--no-run` | 数値の修正のみ。**実行履歴を増やしたくないときは必須** |

### 4-3. 公開

```bash
cd /Users/kentonishimura/x-like-tracker && git add -A && git commit -q -m "ryo 9/X ラン記録: おすすめ140 + フォロー中40" && git push -q && echo pushed
```

ダッシュボード：**https://kento-umapro.github.io/x-like-tracker/ryo/**

---

## 5. 報告フォーマット

ユーザーへの報告は毎回この形にします。

- 実施件数の表（おすすめ／フォロー中／除外リポスト／除外リプライ／いいね済みスキップ）
- 警告の有無
- 今日の累計いいね数
- フォロワー数と前回比、フォロー中の人数、当日投稿の被いいね
- **どてっぱん／うまプロ/UMACHA/ÜMACHA に言及している投稿**があれば、投稿者・要点・URL

言及の検出結果は実行中に `window.__ALLM` に溜まります。終了時にこれを読んで報告してください。

```js
JSON.stringify(window.__ALLM)
```

---

## 6. よくあるトラブル

**タブがバックグラウンドに落ちると止まる（最頻出）**
`document.visibilityState === 'hidden'` になるとXが新しい投稿を読み込まなくなり、`idle` が増えて `exhausted` で終わります。ユーザーにChromeウィンドウを最前面にしてもらい、`window.__A.idle = 0` でリセットして続行します。長く待たせる場合は `window.__A.idle = -100000` にしておくとループが自滅しません。

なおmacOSの**システム設定 → プライバシーとセキュリティ → オートメーション**でClaudeにChromeの操作を許可すると、この中断を自動で解消できるようになります（2026年9月時点で未許可）。

**ページ再読み込みでランナーが消える**
`window.__MK is not a function` が出たら、3-2をもう一度流します。

**フォロー中タブが枯れる**
同じ日に何度も回すと、リポストといいね済みばかりになって新規が拾えなくなります。`sk`（スキップ数）が100を超えてきたら、その日はフォロー中を諦めておすすめか検索に振ってください。

---

## 7. アカウントの背景（返信文などを作るとき用）

@Umapro_ryo は2026年9月6日に開設された新規アカウントです。「BOSSの秘書」という設定で、うまプロCOO 松村僚さんを**第三者視点で勝手に広報する**という建て付けになっています。本人は書かない、秘書が質問して松村さんが答える、という一問一答形式です。

一次資料として、松村さんが社内向けに書いてきた「松村メッセージ」415本があります。アカウントの狙いは**同志を増やすこと**です。トーンを合わせるときはこの点を外さないでください。

初回投稿：https://x.com/Umapro_ryo/status/2096432372506120487

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
