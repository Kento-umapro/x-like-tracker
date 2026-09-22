window.__UNL=function(maxScan){var U={scanned:0,unliked:[],done:false,idle:0,lastH:0,seen:{},r:''};
U.NG=/セックス|セフレ|エロ|えっち|エッチ|潮吹|クンニ|フェラ|おっぱい|オッパイ|乳首|巨乳|貧乳|オナ[ニー]|中出し|挿入|騎乗位|正常位|淫|陰[部唇茎]|射精|勃起|性欲|性行為|風俗|パパ活|裏垢|裏アカ|ちんこ|ちんぽ|チンコ|チンポ|まんこ|マンコ|精子|童貞|絶頂|イかせ|種付|手コキ|寝取|NTR|ワンナイト|ヤリ[たモ]|抱かれたい|犯され|レイプ|痴漢|パンチラ|ヌード|ラブホ|愛撫|喘ぎ|大人の玩具|AV女優|AV男優|18禁|R18|R-18|ムラムラ|発情|性処理|出会い系|パイズリ|アナル|舐め犬|えっろ|ドスケベ|メス堕ち|ショタ|しにたい|死にたい|自殺|リスカ/i;
U.tick=function(){ if(U.done)return; if(location.pathname.indexOf('/likes')<0){U.done=true;U.r='navigated';clearInterval(U.t);return;}
 var arts=[...document.querySelectorAll('article')];
 for(var i=0;i<arts.length;i++){var a=arts[i]; var l=a.querySelector('a[href*="/status/"]'); var u=l?l.getAttribute('href').split('?')[0]:null; if(!u||U.seen[u])continue; U.seen[u]=1; U.scanned++;
  var e=a.querySelector('[data-testid="tweetText"]'); var tx=e?e.innerText:''; var n=a.querySelector('[data-testid="User-Name"]'); var un=n?n.innerText:'';
  if(U.NG.test(tx)){ var b=a.querySelector('button[data-testid="unlike"]'); if(b){ b.click(); U.unliked.push({u:u,t:tx.slice(0,60).replace(/\n/g,' ')}); return; } } }
 if(U.scanned>=maxScan){U.done=true;U.r='max';clearInterval(U.t);return;}
 var h=document.documentElement.scrollHeight; if(h!==U.lastH){U.idle=0;U.lastH=h;}else{U.idle++;}
 window.scrollBy(0,Math.round(innerHeight*0.85)); if(U.idle>25){U.done=true;U.r='end';clearInterval(U.t);} };
U.t=setInterval(U.tick,2000); return U;};