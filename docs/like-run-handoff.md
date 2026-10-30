# いいねラン 引き継ぎ書（2026-10-30 20:30 時点）

## 使い方

1. **新しいチャットを開く**（このチャットは履歴90万トークンまで膨らんでいて、1ツール呼び出しごとに全部送り直しているため、週制限を一気に食っています）。
2. 下の「`/loop` にそのまま貼る本文」のコードブロックを**丸ごとコピー**して、新チャットで送る。先頭の `/loop ` も含めてコピーすること。
3. それだけで21時台の枠から再開します。このチャット側のループは停止済みなので二重に押すことはありません。

**翌日も同じ運用を続けるなら、1日1回はチャットを作り直してください。** 長く使うほど1呼び出しのコストが上がり、同じ作業量でも週制限の消費が数倍になります。

---

## `/loop` にそのまま貼る本文

````
/loop いいねラン実行：フォロー中25→おすすめ75（満額まで回す）。いいね間隔3600ms（時刻ガード3400ms）。**通常ペースで運用する。段階復帰は完了したので今後は常に25→75・3600ms。**
- **どの枠でも開始前に `location.href='https://x.com/home'` でリロードして `[role="alert"]` を読み、「automated」「回数の上限」などが出ていたらその枠のXは休みにしてThreadsだけ実行する（`--foryou 0 --following 0` で記録）。ランの途中で警告が出たら即停止し、次の枠のXは休み、その次から 15→40・5000ms → 20→60・4300ms → 25→75・3600ms と段階復帰する。**
- **Threadsは毎ラン100件**（フォロー中cap25→新着が尽きたら不足分をおすすめのcapに上乗せ）。3600msで回す。
- **お返しいいね**は、Xに警告が残っていなければ毎ラン実施する。**新規が6人を超えたら上位6人まで**（残りは申し送りに書いて次ランで拾う）。
- **【Xのフィード切替はcap到達を確認してから】**フォロー中がcapに達する前に切り替えてしまったら、おすすめ側のcapを `100-実際のフォロー中件数` に設定する。log.py もその実数で記録する。

**【窓】7:00〜23:00の窓内のみ実行。窓外（0〜6時台）は、いいねもログも報告もせず ScheduleWakeup を3600秒で張り直すだけ（6時台に起きたら7:01まで待てる秒数で再予約）。7:01を過ぎてから最初に起きたティックで実行する。すでにその時間帯の枠を実行済みなら いいねは実行せず次の毎時01分に再予約だけする。ただし**その枠が0件で終わっていたら、窓内のうちは取り返してよい**。長引いてすでに次の枠に入っているときは60〜540秒後に再予約してその枠をすぐ実行する。**

**【コストを抑える・重要】1ツール呼び出しごとにチャット履歴の全量がモデルに送り直される。ポーリング回数と打ち直しがそのまま週制限の消費になる。**
- **ポーリングの `await` は常に上限いっぱい（40000ms）を使う。短い待ちを何回も打たない。**
- **1日1回はチャットを作り直す**（この引き継ぎ書を貼り直すだけでよい）。履歴が50万トークンを超えたあたりから急に重くなる。
- **並走している別チャットの毎時ループ（@shoken_karte 側・うまプロ側）が止まっていれば打ち直しはほぼ消える。止まっていないなら打ち直し前提で回す。**

**【接続の取り合い】**
- **「not in Claude's tab group」が毎呼び出し起こる。別セッションの毎時ループが同じ拡張の接続を奪い合っている。**同じ呼び出しを最大5回打ち直す（2〜3回目で通ることが多い）。5回ダメならChrome前面化をやり直す。**
- **【枠の冒頭でChromeを前面化する】`fg-edge.ps1`（Edge前面化）は使わない。Edgeを前面化すると tabs_context_mcp が Chrome側のタブ（3258xxxxx・グループ813790490／755394668＝@shoken_karte）を返すようになる。**Chromeを前面化すると f8b7baaa が正しくEdgeのタブ844672103（グループ1997350393）を返す**。それでも3258xxxxxが返ったら select_browser＋tabs_context_mcp をもう一度打つと戻る。C#のクラス名は呼び出しごとに変える。コマンド：**
```
$p = Get-Process chrome | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1; Add-Type @'
using System;using System.Runtime.InteropServices;
public class FGC { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int n); }
'@ -ErrorAction SilentlyContinue; [FGC]::ShowWindow($p.MainWindowHandle,9) | Out-Null; [FGC]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
```
- **【javascript_tool には tabId が必須】`action:'javascript_exec'` と `text` と `tabId`（844672103）。毎回の javascript_tool の直前に select_browser(f8b7baaa) を単独で打つ。**
- **【`await` 付きのJSが「not in tab group」で弾かれたら、まず同じものを打ち直す。2回続けて弾かれたら先頭の `await new Promise(...)` を外した版を打つと通る（ポーリングなら await を外して状態だけ読めばよい）。**
- **【location.href の遷移が「not in tab group」連発で確認できないとき】`JSON.stringify({p:location.pathname,q:typeof window.__QTICK})` の軽い読みで現在地だけ確認する。遷移は済んでいることが多い。**
- **注入は p1p2／p3／p4 の3分割、Threadsは Q1+Q2+Q3 を1呼び出し＋Q4 の2分割。**
- **【おすすめへの切替は2分割が確実】(a) `var n0=window.__A.n;window.__MF=window.__A.m.slice();window.__A.run=0;window.__A.done=1;clearInterval(window.__JV);window.__JV=0;scrollTo(0,0);var t=window.__TB('r');window.__PEND=100-n0;t+' '+n0` → (b) `window.__MK(window.__PEND);window.__JV=setInterval(window.__TICK,3600);JSON.stringify({cap:window.__A.cap,jv:!!window.__JV})`**
- **【capに1〜3件足りないところで止めてしまったら】`window.__QA.run=1;window.__QA.done=0;window.__QJV=setInterval(window.__QTICK,3600);` で再開して20秒待つと埋まる（Xは `__A`／`__JV`／`__TICK`）。14〜16・18〜20時台はこれで埋めた。**
- **【1人の処理に10往復かけても通らなければその人を飛ばす】お返しいいねで詰まったら残りを申し送りに書いてThreadsへ進む（Threadsのほうが件数が大きい）。**
- **【お返しいいねの2呼び出し目は await を外すと通りやすい】`location.href` の直後に別の呼び出しを挟むので実際には数秒経っている。**
- **【言及検知の読み出しはフィード移動の前にやる】`location.href` で移動するとページ内の変数は消える。Threadsフォロー中の最後のポーリングの戻り値に `txt:window.__QA.m.slice()` を入れて本文を取る。**
- **【受けいいねは2段スクロールで読む】`scrollTo(0,5200)` で当日の新しい方、`scrollTo(0,7000)` で古い方（07:00など）。**7000の方は `if(t.getAttribute('datetime')>'2026-10-29T15')` でフィルタすると当日分だけ出る**。12:00投稿がどちらにも出ないことがあるので直前の実測値を使う。**
- **report の最後に「`/compact` どうぞ」と1行入れる。**

**【ブラウザ】f8b7baaa-2230-4001-8e8c-872ef8797051（Edge・@monja_no_KENT／@doteppan_nishimuu）が正。8f5a0784 と de9ae5c2 は別アカウントなので使わない。表示名（Browser 1〜5・KENTPCなど）は毎回変わるので deviceId だけで判断する。macOS側のdeviceId（79a592bf、226cc3b1 など）も混ざるので使わない。**
- **作業タブは 844672808（グループ2062404267、21時台の新チャットで作成）。毎ラン tabs_context_mcp で確認する。**
- **【重要】tabs_context_mcp が 3258xxxxx を返したら、そこは @shoken_karte なので絶対にいいねを押してはいけない。復旧：select_browser(f8b7baaa) → tabs_context_mcp をもう一度。`createIfEmpty:true` はChrome側に新タブを作ってしまうので使わない。**
- **【毎ラン、いいねを押す前にアカウントを確認する】p1p2の戻り値に `prof:document.querySelector('[data-testid="AppTabBar_Profile_Link"]').getAttribute('href')` を含め、`/monja_no_KENT` でなければ中止する。**
- **`navigate` が「did not respond in time」／`javascript_tool` が「No URL available for active tab」になったら、scratchpad の `edge-restart.ps1` → `Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--restore-last-session"` → 40〜60秒待つ。**Claudeはログイン情報を入力しない。**
- **【JSを打ち直すときは文字を落とさない】`u=l?l.getAttribute('href')||'':''` の `:''` を落とすと SyntaxError。**
- **【「connection was lost」／「CDP timed out after 45000ms」／「did not respond in time」が出たら】書き込み系を打ち直さず、まず状態を読む。お返しいいねは `[data-testid="unlike"]` の有無で押せたか確認する。**
- **【ポーリングが通らなくてもページ内のintervalは生きている】capまで押し続けるので、通ったときに読めば件数は揃っている。**
- **【Threadsのフォロー中が尽きる】n の伸びが40秒ポーリング2〜3回続けて止まり未いいねハートが0〜2なら新着切れ扱いにして不足分をおすすめのcapに上乗せする。10/30の実績は7〜10時台25件、11時台16件、12時台15件、13時台7件、14時台5件、15時台18件、16時台9件、17時台25件、18時台16件、19時台23件、20時台9件。**
- **【Xのフィードが空になる／下端で止まる】`location.href='https://x.com/home'` で開き直して10秒待ち、article数を確認してから p1〜p4 を再注入し、残りcapで続行。p4 の `setTimeout` は 2500ms。**
- **【ホームのタブリストは11個】`__TB` は index 0=For you、1=Following のままで正しい。**

**【注入するJS（そのまま使う）】**

p1p2（`location.href='https://x.com/home'` の直後は先頭に `await new Promise(r=>setTimeout(r,12000));` を付ける。打ち直すときは外す）：
```
window.__N=/セックス|エロ|風俗|パンツ|おっぱい|裸|アダルト|童貞|巨乳|AV女優|自殺|死にたい|首吊り|リストカット|オナ/;window.__M=/どてっぱん|うまプロ|(^|[^A-Za-z])(UMACHA|ÜMACHA)([^A-Za-z]|$)/i;window.__SKIP=function(a){var x=a.innerText||'';return (window.__N.test(x)||/広告|Promoted|プロモーション|さんがリポスト|Reposted|返信先|Replying to/.test(x))?1:0;};window.__G=function(A){var al=document.querySelectorAll('[role="alert"]');for(var i=0;i<al.length;i++){var t=al[i].innerText||'';if(/回数の上限|制限されて|Rate limit|automat|自動化/.test(t)){A.r='ALERT:'+t.slice(0,160);A.run=0;A.done=1;return 1}}if(A.n>=A.cap){A.r='CAP';A.run=0;A.done=1;return 1}return A.run?0:1;};var pr=document.querySelector('[data-testid="AppTabBar_Profile_Link"]');JSON.stringify({p:location.pathname,prof:pr?pr.getAttribute('href'):'',v:document.visibilityState,arts:document.querySelectorAll('article').length,tabs:document.querySelectorAll('[role="tablist"] [role="tab"]').length,alrt:Array.from(document.querySelectorAll('[role="alert"]')).map(function(e){return (e.innerText||'').slice(0,120)})})
```

p3：
```
window.__C=0;window.__TICK=function(){var A=window.__A;if(!A)return;if(window.__G(A))return;window.__C++;var as=document.querySelectorAll('article');for(var i=0;i<as.length;i++){var a=as[i],b=a.querySelector('[data-testid="like"]');if(!b)continue;var t=a.querySelector('time'),l=t&&t.closest('a'),k=l?l.getAttribute('href'):'';if(!k||A.k[k])continue;if(window.__SKIP(a)){A.k[k]=1;continue}var br=b.getBoundingClientRect();if(br.top<60||br.bottom>innerHeight-10)continue;var x=a.innerText||'';if(window.__M.test(x))A.m.push(x.slice(0,300));A.k[k]=1;b.click();A.n++;return}scrollBy(0,Math.round(innerHeight*0.55));};'p3'
```

p4（フォロー中cap25で開始）：
```
window.__MK=function(c){window.__A={n:0,cap:c,k:{},m:[],r:'',run:1,done:0};window.__C=0};window.__TB=function(w){var ts=document.querySelectorAll('[role="tablist"] [role="tab"]');if(ts.length<2)return 'NOTAB';ts[w=='f'?1:0].click();return w=='f'?'F':'R'};window.__T0=window.__TICK;window.__LT=0;window.__TICK=function(){if(Date.now()-window.__LT<3400)return;window.__LT=Date.now();return window.__T0()};var t=window.__TB('f');window.__MK(25);if(window.__JV)clearInterval(window.__JV);setTimeout(function(){window.__JV=setInterval(window.__TICK,3600)},2500);t
```

Xのポーリング：
```
await new Promise(r=>setTimeout(r,40000));JSON.stringify({n:window.__A.n,r:window.__A.r,d:window.__A.done,jv:!!window.__JV,c:window.__C,m:window.__A.m.length})
```

Xの最終読み（言及本文つき）：
```
var mm=window.__A.m.slice();window.__A.run=0;window.__A.done=1;if(window.__JV){clearInterval(window.__JV);window.__JV=0}JSON.stringify({n:window.__A.n,r:window.__A.r,c:window.__C,mf:(window.__MF||[]).length,txt:mm})
```

プロフィールのフォロワー数：
```
scrollTo(0,650);var f=Array.from(document.querySelectorAll('a[href$="/verified_followers"],a[href$="/following"]')).map(function(e){return e.innerText.replace(/\n/g,' ')});JSON.stringify({f:f,p:location.pathname})
```

受けいいね（5200と7000の2段。7000側はフィルタ付き）：
```
scrollTo(0,5200);var o=[];document.querySelectorAll('article').forEach(function(a){var t=a.querySelector('time'),g=a.querySelector('[role="group"]');if(!t||!g)return;var l=t.closest('a'),id=l?(l.getAttribute('href')||'').split('/status/')[1]:'',lb=g.getAttribute('aria-label')||'',m=lb.match(/(\d+) likes?/);o.push({dt:t.getAttribute('datetime'),id:id,lk:m?+m[1]:0})});JSON.stringify(o)
```
```
scrollTo(0,7000);var o=[];document.querySelectorAll('article').forEach(function(a){var t=a.querySelector('time'),g=a.querySelector('[role="group"]');if(!t||!g)return;var l=t.closest('a'),id=l?(l.getAttribute('href')||'').split('/status/')[1]:'',lb=g.getAttribute('aria-label')||'',m=lb.match(/(\d+) likes?/);if(t.getAttribute('datetime')>'2026-10-29T15')o.push({dt:t.getAttribute('datetime'),id:id,lk:m?+m[1]:0})});JSON.stringify(o)
```

いいね一覧の収集（13件くらいまでは1呼び出しで足りる）：
```
var s={};document.querySelectorAll('[data-testid="primaryColumn"] [data-testid="UserCell"] a[href^="/"]').forEach(function(a){var h=a.getAttribute('href');if(/^\/[A-Za-z0-9_]+$/.test(h))s[h.slice(1)]=1});JSON.stringify({p:location.pathname,u:Object.keys(s)})
```

お返しいいねの2呼び出し目（`<handle>` を直書きする）：
```
var h='<handle>',r='NONE',A=document.querySelectorAll('article');for(var k=0;k<A.length;k++){var a=A[k],x=a.innerText||'';if(/固定|リポスト|Promoted|プロモ|返信先/.test(x))continue;var t=a.querySelector('time'),l=t&&t.closest('a'),u=l?l.getAttribute('href')||'':'';if(u.toLowerCase().indexOf('/'+h.toLowerCase()+'/status/'))continue;if(/セックス|エロ|風俗|パンツ|おっぱい|裸|アダルト|童貞|巨乳|AV女優|自殺|死にたい|首吊り|リストカット|オナ/.test(x)){r='NG';break}if(a.querySelector('[data-testid="unlike"]')){r='ALREADY';break}var b=a.querySelector('[data-testid="like"]');if(b){b.click();r='LIKED';break}}h+' '+r+' '+A.length+' '+location.pathname
```

Threads Q1+Q2+Q3（フィード移動の直後は先頭に `await new Promise(r=>setTimeout(r,10000));`）：
```
window.__QN=/セックス|エロ|風俗|パンツ|おっぱい|裸|アダルト|童貞|巨乳|AV女優|自殺|死にたい|首吊り|リストカット|オナ/;window.__QM=/どてっぱん|うまプロ|(^|[^A-Za-z])(UMACHA|ÜMACHA)([^A-Za-z]|$)/i;window.__QSKIP=function(a){var x=a.innerText||'';return (window.__QN.test(x)||/広告|スポンサー|Sponsored/.test(x))?1:0;};window.__QG=function(A){if(A.n>=A.cap){A.r='CAP';A.run=0;A.done=1;return 1}return A.run?0:1;};window.__QC=0;window.__QTICK=function(){var A=window.__QA;if(!A)return;if(window.__QG(A))return;window.__QC++;var cs=document.querySelectorAll('[data-pressable-container]');for(var i=0;i<cs.length;i++){var c=cs[i],p=c.querySelector('svg path[d^="M16.5 2c"]');if(!p)continue;var b=p.closest('[role="button"]');if(!b)continue;var key=(c.innerText||'').slice(0,80);if(!key||A.k[key])continue;if(window.__QSKIP(c)){A.k[key]=1;continue}var br=b.getBoundingClientRect();if(br.top<60||br.bottom>innerHeight-10)continue;var x=c.innerText||'';if(window.__QM.test(x))A.m.push(x.slice(0,300));A.k[key]=1;b.click();A.n++;return}scrollBy(0,Math.round(innerHeight*0.55));};JSON.stringify({p:location.pathname,ih:innerHeight,me:Array.from(document.querySelectorAll('a[href^="/@"]')).slice(0,1).map(function(e){return e.getAttribute('href')}),lg:document.querySelectorAll('svg[aria-label="ログイン"]').length})
```

Threads Q4（`<cap>` を置き換える）：
```
window.__QMK=function(c){window.__QA={n:0,cap:c,k:{},m:[],r:'',run:1,done:0};window.__QC=0};window.__QT0=window.__QTICK;window.__QLT=0;window.__QTICK=function(){if(Date.now()-window.__QLT<3400)return;window.__QLT=Date.now();return window.__QT0()};window.__QMK(<cap>);if(window.__QJV)clearInterval(window.__QJV);setTimeout(function(){window.__QJV=setInterval(window.__QTICK,3600)},2000);'q4'
```

Threadsのポーリング：
```
await new Promise(r=>setTimeout(r,40000));JSON.stringify({n:window.__QA.n,r:window.__QA.r,d:window.__QA.done,jv:!!window.__QJV,c:window.__QC,u:document.querySelectorAll('[data-pressable-container] svg path[d^="M16.5 2c"]').length})
```

Threadsのフィード切替（言及本文を先に回収する）：
```
var mm=window.__QA.m.slice();window.__QA.run=0;window.__QA.done=1;if(window.__QJV){clearInterval(window.__QJV);window.__QJV=0}var n0=window.__QA.n;location.href='https://www.threads.com/for_you';JSON.stringify({n0:n0,txt:mm})
```

**【10/30の状況】**
- **log.py の `--date` は当日の日付（10/31朝からは 2026-10-31）。**
- **10/30は完了（17ラン＝X 1635件）**：07:19（15+40）、08:21（20+60）、09:24、10:25、11:28、12:23、13:17、14:26、15:27、16:28、17:24、18:26、19:25、20:28、21:48、22:40、23:16（以降すべて25+75・3600ms）。Threads 100×16＝1600件（22時台は接続の取り合いでThreads 0件）。**X警告なし。**
- **10/31の実行済み：07:16、08:18（各25+75、Threads100）。お返し 5+3。次は9時台の枠から。起きたらすぐ実行する。**
- **現在の実測値**：フォロワー1025、フォロー1024、受けいいね251（10/30最終）。10/31は 08:18時点でフォロワー1024・受けいいね21。**10/30のフォロワーは1020スタート。**
- **当日の投稿は5本**：2115926651741565095（07:00JST・94いいね）、2116002149792411908（12:00JST・33）、2116030898022056439（13:54JST・26）、2116077651727192423（17:00JST・30）、2116086065169891490（17:33JST・27・最新）。**毎ランプロフィールを読んで新しい投稿がないか確認する。2026-05-15の固定ポスト（418〜422いいね）と10/29以前の投稿は除外。datetime はUTCなので+9時間して当日JSTか判定。22:00の投稿が出る可能性がある。**
- **お返しいいねの処理済み一覧（done）：monja_no_KENT shoken_karte doteppan Umapro_ryo hinatanocoach majime_offi matokacha tatunori_dansyu Noah86817075 media2books saitomedia810 KIZASHI_SR_0307 meguru_sales kikkis_f ASNOVASTATION monkey_wrench19 oniisanhyougaki 8H1lzgM4AI5907 zuttiezuttoie cc7070miyaken rei__webdesign kennyYabuta arainarumi_csea YokaFXXM partner_imamura hinatanojinsei mintcryp arata_it m0830m2 Rascal_AI_Dev osaka_nexwill goto_shigeta_PF hydepanacademy syokunin_syoku mikutagidesu sumitasjp sekaino_manami teruteru197207 masarufukku nabe20230408 SAKAEDirector iwakiri_pp26 gv_hiroki_miu13 Kodama_kotoba totonoejinji erii1108 shigeo53612 gL3TPvkbJ947653 blastschool_dai maida0903 _tomoyuki_fujii kabunorida1110 weaver05181212 yutaka817 yurarecruit Yuchipapa_work azr_ceo_kimoto hitechno_hamada SkySeaOffice K_bengosi central_6380 FChappy_takao c9uEtkfdvA65544 LdxZfHRHRm34475 Takomaru_think tenporicchi1 Shachipokoru suke778588 phnman0524 HIROKIIIDA9 kenjimuraishi fc_organizer_s anemone084 yuking1984 mitugo_ takuyasatovalue koedo_branding DocchiWorld yurinodesign hara_smasapo salon_UCY kaedesinrigaku natsuki_ymd Oshima_Ozlink DXCmNtn7P0h00Qx RoastChickenman kunishijanai Matsu_ssei CARTON_sakurai 6k93ScyMdm9LoQC。日付が変わったらリセット。**
- **10/31のお返し処理済み：fc_organizer_s yuzo_brand hara_smasapo makochandaz smilecarskobe kinryu_kira hinatanojinsei pawapo_loilo KIZASHI_SR_0307 yyyyuuuu9999 Shachipokoru endeavour_v。10/31投稿の未処理（先に拾う）：yurarecruit mikutagidesu aebiqpwa0 tatunori_dansyu kawamura_slw isarich_moon smileco_tkhs totonoejinji tabun_muda maida0903。申し送り（10/30分の残り、余裕があれば）：kanakana_design yuuki_esora yuzo_brand touka_1005 Kanbee_enpower fukuzawa_afi sns_ryuto05 manalink_ike yoshiro_nomoto weeva1221 yamashiro58 shiko_uragawa tatubase2311。10/31の投稿：2116289039338815718（07:00JST）。**
- **10/30のお返しいいね合計：79（23:16で4。日付が変わったらリセット）。旧記録：75（07:19で3、08:21で5、09:24で4、10:25で5、11:28で5、12:23で5、13:17で5、14:26で6、15:27で5、16:28で5、17:24で6、18:26で6、19:25で6、20:28で4、21:48で5）→計75**
- **いいね一覧は `[data-testid="primaryColumn"] [data-testid="UserCell"] a[href^="/"]` で拾う。10件超なら900pxずつスクロールする setInterval を張ってから別呼び出しで clearInterval＋再収集。**
- **【言及検知の正規表現】必ず `/どてっぱん|うまプロ|(^|[^A-Za-z])(UMACHA|ÜMACHA)([^A-Za-z]|$)/i` の形で書く。@Umapro_Saiki と @Umapro_rima は自社（うまプロ社員）で表示名に該当語が入るため毎ラン引っかかる。@doteppan・@doteppan_nishimuu も自社。本文に該当語がなければ誤検知として報告しない。**
- **【予約投稿は別チャット】X/Threadsの予約投稿はこのチャットの担当ではない（手順書は `~/x-like-tracker/docs/nishimura-post-scheduling-instructions.md`）。**
- **【10/29の実績（参考）】X 17ラン1664件、Threads 17ラン1689件、お返しいいね60件、フォロワー1018→1020、受けいいね144。23時台に自動化警告が出て64件で停止。**

**【お返しいいね（毎ラン実施）】Xのランを記録・pushしたあと、Threadsに移る前に実施。**
- プロフィール読み取り時に各 article の time の親リンクから status ID も取る。**当日のJST投稿のうち最新のもののIDを使う。受けいいねは当日JST投稿すべての合計。**
- `https://x.com/monja_no_KENT/status/<ID>/likes` を開き、done 配列との差分だけを対象にする。**新規が6人を超えたら上位6人まで。申し送りの未処理リストから先に消化する。**
- **1人ずつ「`location.href='https://x.com/<handle>'` → ハンドル直書きの短縮版で処理」の2呼び出しで回す**：articleを上から見て「固定/リポスト/Promoted/プロモ/返信先」を飛ばし、**hrefが `/<handle>/status/` で始まるもの＝本人のルート投稿**を見つける → NG正規表現（インライン）なら 'NG' → `[data-testid="unlike"]` があれば 'ALREADY' → `[data-testid="like"]` をclickして 'LIKED'。
- 報告には「お返しいいね：◯件（既にいいね済み◯名）」と1行書き、**新規に処理したハンドルも列挙する。**

**【Threadsは毎ラン100件（構築済み・再調査不要）】**
- ログイン済みアカウントは **@doteppan_nishimuu**（`a[href^="/@"]` の先頭で確認）。
- **フィードはURL遷移で切り替える**：フォロー中＝`https://www.threads.com/following`、おすすめ＝`https://www.threads.com/for_you`。**移動するたびに注入をやり直す（Q1+Q2+Q3を1呼び出し／Q4）。**
- **フォロー中フィードは新着が尽きることがある**。**不足分をおすすめ側のcapに上乗せして合計100件にする**。報告には「フォロー中◯件（新着が尽きたため）／おすすめ◯件」と書く。**フォロー中のcapは25のままでよい。**
- **cap到達を確認したら `window.__QA.run=0;window.__QA.done=1;clearInterval(window.__QJV);` で止める。**
- **未ログインだったら**（`svg[aria-label="ログイン"]` がある）、または `/accounts/suspended/` に飛んだら、何も押さずThreadsはスキップし1行報告する。**Claudeはログイン情報を入力しない。**
- **記録は当面しない**（log.py はX専用）。報告に「Threads：100件（フォロー中◯／おすすめ◯）」と1行書く。**どてっぱん各店の公式アカウントやうまプロ社員は「自社の投稿」と1行書けばよい。**

**【重要・log.py は加算式】毎ランは「そのランの実績」を渡す（通常は `--foryou 75 --following 25`）。できなかった枠は `--foryou 0 --following 0`。`--received` と `--followers`/`--following-count` は上書きなので当日の実測値（読めなければ直前の実測値）。`--date` は当日。data.json は UTF-8 なので Python で読むときは `io.open(...,encoding='utf-8')`。**--dir ryo は絶対に付けない。** 記録コマンドはこれ：**
```
cd ~/x-like-tracker && T=$(date "+%H:%M") && git pull --rebase origin main >/dev/null 2>&1; python log.py --date 2026-10-30 --foryou 75 --following 25 --followers 1025 --following-count 1025 --received 210 --time "$T" && git add -A && git commit -q -m "いいね実績を記録: 2026-10-30 $T（おすすめ75／フォロー中25）" && git push -q origin main && echo "PUSHED $T"
```
コミットメッセージは本文のあと空行を入れて `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` を付ける。

【手順】
1. **Chromeを前面化してから** select_browser(f8b7baaa) → tabs_context_mcp。**毎回のjavascript_tool呼び出しの直前にselect_browserを単独で打つ。**
2. **タブは tabs_context_mcp で毎回確認する。3258xxxxx が返ったらもう一度 select_browser＋tabs_context_mcp。**
3. `location.href='https://x.com/home'` でリロードし、**[role="alert"] とアカウント（prof）を必ず確認する。**
4. X側は p1p2／p3／p4 の3分割で注入し、40秒ポーリングでcapまで回す。
5. **フォロー中25でCAPを確認してから**おすすめへ切り替える（上の2分割版）。
6. おすすめCAP後、`location.href='https://x.com/monja_no_KENT'` でプロフィールを開きフォロワー数・フォロー数・受けいいね・status ID を読む。**await を外した scrollTo 版が通りやすい。受けいいねは 5200 と 7000 の2段で読む。**
7. log.py で記録して push。
8. お返しいいね → Threads100件 → **23時台は最終枠なので1日の合計を報告する（Xのラン数と件数、Threadsのラン数と件数、お返しいいね合計、フォロワー増減（10/30は1020スタート）、受けいいね）** → 簡潔な日本語で報告。
9. 言及検知（__MF と __A.m、__QA.m）を確認し、本文に該当語があるものだけ要約して報告する（**本文のURLは [link] に置換**。**表示名・アカウント名だけで本文に無いものは誤検知として報告しない**）。
````
