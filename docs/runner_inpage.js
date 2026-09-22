try{Object.defineProperty(document,'visibilityState',{get:()=>'visible',configurable:true});Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});document.addEventListener('visibilitychange',e=>e.stopImmediatePropagation(),true);}catch(e){}
window.__MK=function(cap){
 var A={K:0,cap:cap,done:false,idle:0,skip:0,rt:0,rp:0,ng:0,NGL:[],MINE:{},M:(window.__ALLM=window.__ALLM||{}),lastH:0,reason:''};
 A.NG=/セックス|セフレ|エロ|えっち|エッチ|潮吹|クンニ|フェラ|おっぱい|オッパイ|乳首|巨乳|貧乳|オナ[ニー]|中出し|挿入|騎乗位|正常位|淫|陰[部唇茎]|射精|勃起|性欲|性行為|風俗|パパ活|裏垢|裏アカ|ちんこ|ちんぽ|チンコ|チンポ|まんこ|マンコ|精子|童貞|絶頂|イかせ|種付|手コキ|寝取|NTR|ワンナイト|ヤリ[たモ]|抱かれたい|犯され|レイプ|痴漢|パンチラ|ヌード|ラブホ|愛撫|喘ぎ|大人の玩具|AV女優|AV男優|18禁|R18|R-18|ムラムラ|発情|性処理|出会い系|パイズリ|アナル|舐め犬|えっろ|ドスケベ|メス堕ち|ショタ|しにたい|死にたい|自殺|リスカ/i;
 A.isNG=function(a){var e=a.querySelector('[data-testid="tweetText"]');var s=e?e.innerText:'';return A.NG.test(s);};
 A.isAd=function(a){return [...a.querySelectorAll('span')].some(function(x){var t=x.textContent.trim();return t==='Ad'||t==='プロモーション'||t==='Promoted'||t==='広告';});};
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
 A.limited=function(){ var el=document.querySelector('[role="alert"],[data-testid="toast"]'); return !!(el && /might be automated|Try liking|Rate limit|制限|自動化/.test(el.innerText)); };
 A.note=function(a){var e=a.querySelector('[data-testid="tweetText"]');var s=e?e.innerText:'';
  if(/どてっぱん|UMACHA|ÜMACHA|うまプロ/.test(s)){var u=A.uid(a); if(u&&!A.M[u]){var n=a.querySelector('[data-testid="User-Name"]');A.M[u]={n:n?n.innerText.replace(/\n/g,' '):'',s:s.slice(0,200)};}}};
 A.tick=function(){
  if(A.done)return;
  if(location.pathname!=='/home'){A.done=true;A.reason='navigated';clearInterval(A.timer);return;}
  var p=document.querySelector('[data-testid="AppTabBar_Profile_Link"]'); if(p&&p.getAttribute('href')!=='/Umapro_ryo'){A.done=true;A.reason='acct';clearInterval(A.timer);return;}
  if(A.limited()){A.done=true;A.reason='ratelimit';clearInterval(A.timer);return;}
  if(A.K>=A.cap){A.done=true;A.reason='cap';clearInterval(A.timer);return;}
  var arts=[...document.querySelectorAll('article')];
  for(var i=0;i<arts.length;i++){var a=arts[i];A.note(a);
   if(A.isAd(a))continue;
   var u=A.uid(a); if(u&&A.MINE[u])continue;
   if(u&&u.indexOf('/Umapro_ryo/')===0){A.MINE[u]=1;continue;}
   if(A.isRT(a)){ if(u){A.MINE[u]=1;A.rt++;} continue; }
   if(A.isReply(a)){ if(u){A.MINE[u]=1;A.rp++;} continue; }
   if(A.isNG(a)){ if(u){A.MINE[u]=1;A.ng++;A.NGL.push(u);} continue; }
   if(a.querySelector('button[data-testid="unlike"]')){if(u){A.MINE[u]=1;A.skip++;}continue;}
   var b=a.querySelector('button[data-testid="like"]'); if(!b)continue;
   b.click(); A.K++; if(u)A.MINE[u]=1; A.idle=0; return;}
  var h=document.documentElement.scrollHeight;
  if(h!==A.lastH){A.idle=0;A.lastH=h;} else {A.idle++;}
  window.scrollBy(0, Math.round(window.innerHeight*0.85));
  if(A.idle>40){A.done=true;A.reason='exhausted';clearInterval(A.timer);}
 };
 window.scrollTo(0,0);
 A.timer=setInterval(A.tick,3600);
 return A;
};
window.__TB={ go:function(name){ var t=[...document.querySelectorAll('[role="tab"]')].find(function(x){return x.innerText.trim()===name;}); if(!t)return false; if(t.getAttribute('aria-selected')==='true')return true; t.click();return true; },
 cur:function(){ var t=[...document.querySelectorAll('[role="tab"]')].find(function(x){return x.getAttribute('aria-selected')==='true';}); return t?t.innerText.trim():'?'; } };
