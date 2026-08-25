#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.json を読んで index.html を生成する。"""
import io, json, os

BASE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>いいね実績ボード</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="@monja_no_KENT の日々のいいね数とフォロワー増減の記録">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Martian+Mono:wght@400;500;600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230C0A12'/%3E%3Cpath d='M16 25S6.5 19.2 6.5 13.2A4.7 4.7 0 0 1 16 10.6a4.7 4.7 0 0 1 9.5 2.6C25.5 19.2 16 25 16 25z' fill='%23A472FF'/%3E%3C/svg%3E">
<style>
/* dark-first: 盤面がこのページの既定 */
:root{
  --void:#0C0A12; --panel:#151121; --panel-2:#1E1830; --sunk:#0F0C18;
  --rule:#2B2340; --rule-2:#3A3055;
  --ink:#F4F0FC; --ink-2:#C6BEDC; --muted:#8A81A6;
  --vio:#A472FF; --vio-dim:#6A46B8; --vio-ghost:rgba(164,114,255,.13);
  --amb:#FFB247; --amb-dim:#B87A25; --amb-ghost:rgba(255,178,71,.13);
  --mint:#54E5C4; --mint-dim:#2C9C86; --mint-ghost:rgba(84,229,196,.13);
  --pos:#54E5C4; --neg:#FF7A6B;
  --grid:rgba(164,114,255,.10);
  --glow:0 0 0 1px var(--rule), 0 18px 40px -24px rgba(0,0,0,.9);
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --void:#F5F3FA; --panel:#FFFFFF; --panel-2:#F1EEF8; --sunk:#EDEAF5;
    --rule:#DFD9EC; --rule-2:#C7BEDE;
    --ink:#150F24; --ink-2:#443B5E; --muted:#736A8C;
    --vio:#7A34E0; --vio-dim:#B79BEE; --vio-ghost:rgba(122,52,224,.09);
    --amb:#A96C05; --amb-dim:#E3B876; --amb-ghost:rgba(169,108,5,.10);
    --mint:#0B8E74; --mint-dim:#7FCFBC; --mint-ghost:rgba(11,142,116,.10);
    --pos:#0B8E74; --neg:#C93B29;
    --grid:rgba(122,52,224,.08);
    --glow:0 0 0 1px var(--rule), 0 14px 34px -26px rgba(21,15,36,.5);
  }
}
:root[data-theme="light"]{
  --void:#F5F3FA; --panel:#FFFFFF; --panel-2:#F1EEF8; --sunk:#EDEAF5;
  --rule:#DFD9EC; --rule-2:#C7BEDE;
  --ink:#150F24; --ink-2:#443B5E; --muted:#736A8C;
  --vio:#7A34E0; --vio-dim:#B79BEE; --vio-ghost:rgba(122,52,224,.09);
  --amb:#A96C05; --amb-dim:#E3B876; --amb-ghost:rgba(169,108,5,.10);
  --mint:#0B8E74; --mint-dim:#7FCFBC; --mint-ghost:rgba(11,142,116,.10);
  --pos:#0B8E74; --neg:#C93B29;
  --grid:rgba(122,52,224,.08);
  --glow:0 0 0 1px var(--rule), 0 14px 34px -26px rgba(21,15,36,.5);
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--void); color:var(--ink);
  font-family:"Zen Kaku Gothic New","Hiragino Kaku Gothic ProN",system-ui,sans-serif;
  font-size:15px; line-height:1.75; -webkit-font-smoothing:antialiased;
  background-image:radial-gradient(var(--grid) 1px, transparent 1px);
  background-size:22px 22px; background-position:-1px -1px;
}
.wrap{max-width:1020px; margin:0 auto; padding:0 18px 80px; display:flex; flex-direction:column; gap:26px}

.mono{font-family:"Martian Mono",ui-monospace,"SFMono-Regular",monospace; font-variant-numeric:tabular-nums}
.lab{
  font-family:"Martian Mono",monospace; font-size:9.5px; font-weight:600;
  letter-spacing:.2em; text-transform:uppercase; color:var(--muted); line-height:1;
}

/* ── masthead ───────────────────────────── */
.masthead{padding:44px 0 22px; border-bottom:1px solid var(--rule-2); display:flex; flex-direction:column; gap:16px}
.rail{display:flex; align-items:center; gap:12px}
.rail .lab{white-space:nowrap}
.rail hr{flex:1; height:1px; border:0; margin:0; background:linear-gradient(90deg,var(--rule-2),transparent)}
h1{
  font-family:"Dela Gothic One","Zen Kaku Gothic New",sans-serif; font-weight:400; margin:0;
  font-size:clamp(31px,7vw,58px); line-height:1.06; letter-spacing:-.015em; text-wrap:balance;
}
h1 em{font-style:normal; color:var(--vio)}
.ident{display:flex; flex-wrap:wrap; align-items:center; gap:8px 16px; font-size:13px; color:var(--ink-2)}
.ident .handle{
  font-family:"Martian Mono",monospace; font-size:11.5px; font-weight:600; color:var(--vio);
  border:1px solid var(--rule-2); border-radius:5px; padding:3px 8px; letter-spacing:.02em;
}
.ident .span{font-family:"Martian Mono",monospace; font-size:11px; color:var(--muted); letter-spacing:.05em}

/* ── hero ───────────────────────────────── */
.hero{display:grid; grid-template-columns:1.55fr 1fr; gap:14px}
.slab{
  background:var(--panel); border-radius:14px; box-shadow:var(--glow);
  padding:22px 24px 20px; display:flex; flex-direction:column; gap:14px; position:relative; overflow:hidden;
}
.slab::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(160deg, var(--tint,transparent) 0%, transparent 46%);
}
.slab.today{--tint:var(--vio-ghost)}
.slab.folw{--tint:var(--mint-ghost)}
.slab-head{display:flex; align-items:baseline; justify-content:space-between; gap:10px}
.stamp{font-family:"Martian Mono",monospace; font-size:10.5px; color:var(--muted); letter-spacing:.08em}

.big{
  font-family:"Martian Mono",monospace; font-variant-numeric:tabular-nums; font-weight:700;
  font-size:clamp(46px,10.5vw,80px); line-height:.92; letter-spacing:-.055em;
}
.big.f{color:var(--mint)}
.unit{font-size:.26em; font-weight:500; letter-spacing:.06em; color:var(--muted); margin-left:.5em; vertical-align:.42em}

.split{display:flex; height:9px; border-radius:5px; overflow:hidden; background:var(--sunk); gap:2px}
.split i{display:block; height:100%; border-radius:2px; transform-origin:left center}
.split i.a{background:var(--vio)} .split i.b{background:var(--amb)}
.readouts{display:flex; gap:26px; flex-wrap:wrap}
.readout{display:flex; flex-direction:column; gap:5px; min-width:92px}
.readout .k{display:flex; align-items:center; gap:6px}
.dot{width:8px; height:8px; border-radius:2px; flex:none}
.dot.a{background:var(--vio)} .dot.b{background:var(--amb)} .dot.c{background:var(--mint)}
.readout .n{font-family:"Martian Mono",monospace; font-variant-numeric:tabular-nums; font-size:21px; font-weight:600; line-height:1}

.chip{
  display:inline-flex; align-items:center; gap:4px; border-radius:999px; padding:3px 10px;
  font-family:"Martian Mono",monospace; font-size:11px; font-weight:700; font-variant-numeric:tabular-nums;
  letter-spacing:.02em; white-space:nowrap;
}
.chip.up{background:var(--mint-ghost); color:var(--pos); box-shadow:inset 0 0 0 1px var(--mint-dim)}
.chip.down{background:rgba(255,122,107,.12); color:var(--neg); box-shadow:inset 0 0 0 1px var(--neg)}
.chip.flat{background:var(--panel-2); color:var(--muted); box-shadow:inset 0 0 0 1px var(--rule)}
.chip.sm{font-size:10px; padding:2px 8px}

/* ── totals strip ───────────────────────── */
.strip{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  background:var(--panel); border-radius:14px; box-shadow:var(--glow); overflow:hidden;
}
.cell{padding:16px 18px; display:flex; flex-direction:column; gap:7px; border-left:1px solid var(--rule)}
.cell:first-child{border-left:0}
.cell .n{font-family:"Martian Mono",monospace; font-variant-numeric:tabular-nums; font-size:25px; font-weight:600; line-height:1; letter-spacing:-.03em}
.cell .s{font-size:11.5px; color:var(--muted); line-height:1.4}

/* ── board ──────────────────────────────── */
.sec-head{display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px 18px; margin-bottom:-4px}
h2{font-family:"Dela Gothic One","Zen Kaku Gothic New",sans-serif; font-weight:400; margin:0; font-size:17px; letter-spacing:.01em}
.legend{display:flex; flex-wrap:wrap; gap:16px; font-size:12px; color:var(--ink-2)}
.legend span{display:inline-flex; align-items:center; gap:7px}
.sw{width:10px; height:10px; border-radius:2px; flex:none}
.sw.ln{height:3px; width:18px; border-radius:2px}

.board{background:var(--panel); border-radius:14px; box-shadow:var(--glow); padding:20px 16px 12px; overflow-x:auto}
.board svg{display:block; min-width:560px; width:100%; height:auto}
@media (prefers-reduced-motion:no-preference){
  .grow{transform:scaleY(0); transform-box:fill-box; transform-origin:bottom; animation:rise .62s cubic-bezier(.22,.9,.28,1) forwards}
  @keyframes rise{to{transform:scaleY(1)}}
  .draw{stroke-dasharray:var(--len); stroke-dashoffset:var(--len); animation:trace .9s .35s ease-out forwards}
  @keyframes trace{to{stroke-dashoffset:0}}
}

/* ── ledger ─────────────────────────────── */
.ledger{background:var(--panel); border-radius:14px; box-shadow:var(--glow); overflow-x:auto}
table{border-collapse:collapse; width:100%; min-width:1150px}
td.runs{text-align:left; max-width:300px}
td.runs .runchip{
  display:inline-flex; align-items:center; gap:5px; margin:2px 4px 2px 0;
  background:var(--sunk); border:1px solid var(--rule); border-radius:5px; padding:2px 7px;
  font-size:10.5px; white-space:nowrap;
}
td.runs .runchip b{font-weight:600; color:var(--ink-2)}
td.runs .runchip i{font-style:normal; font-weight:600; font-variant-numeric:tabular-nums}
td.runs .runchip i.fy{color:var(--vio)}
td.runs .runchip i.fl{color:var(--amb)}
td.runs .runchip.warn{border-color:var(--neg)}
.pend{
  margin-left:6px; font-size:9px; letter-spacing:.1em; padding:1px 5px; border-radius:4px;
  background:var(--amb-ghost); color:var(--amb); font-weight:600; vertical-align:1px;
}
thead th{
  font-family:"Martian Mono",monospace; font-size:9.5px; font-weight:600; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); text-align:right; white-space:nowrap;
  padding:14px 16px 11px; border-bottom:1px solid var(--rule-2);
}
thead th:first-child{text-align:left}
tbody td{
  padding:12px 16px; border-bottom:1px solid var(--rule); text-align:right;
  font-family:"Martian Mono",monospace; font-variant-numeric:tabular-nums; font-size:13px;
}
tbody tr:last-child td{border-bottom:0}
tbody tr{transition:background .14s ease}
tbody tr:hover td{background:var(--panel-2)}
tbody tr.top td{background:var(--vio-ghost)}
tbody tr.top:hover td{background:var(--vio-ghost)}
td.d{text-align:left; white-space:nowrap; color:var(--ink)}
td.d .dw{color:var(--muted); margin-left:6px; font-size:11px}
td.d .bg{
  margin-left:9px; font-size:9px; letter-spacing:.14em; padding:2px 7px; border-radius:4px;
  background:var(--vio-ghost); color:var(--vio); font-weight:600; text-transform:uppercase;
}
td.tot{font-weight:700; font-size:14px}
td .z{color:var(--muted); opacity:.55}
.bar{display:flex; height:5px; border-radius:3px; overflow:hidden; background:var(--sunk); min-width:86px; gap:1.5px}
.bar i{display:block; height:100%; border-radius:1.5px}
.bar i.a{background:var(--vio)} .bar i.b{background:var(--amb)}

/* ── note / footer ──────────────────────── */
.note{
  background:var(--panel); border-radius:14px; box-shadow:var(--glow);
  padding:20px 22px; font-size:13px; color:var(--ink-2); display:flex; flex-direction:column; gap:10px;
}
.note ul{margin:0; padding-left:1.2em; display:flex; flex-direction:column; gap:6px}
code{
  font-family:"Martian Mono",monospace; font-size:11.5px; color:var(--ink);
  background:var(--sunk); border:1px solid var(--rule); border-radius:5px; padding:2px 6px;
}
footer{display:flex; justify-content:center; padding-top:6px}
.empty{padding:34px 16px; text-align:center; color:var(--muted); font-size:13px}

@media (max-width:720px){
  .hero{grid-template-columns:1fr}
  .cell{border-left:0; border-top:1px solid var(--rule)}
  .cell:nth-child(-n+2){border-top:0}
  .cell:nth-child(even){border-left:1px solid var(--rule)}
  .strip{grid-template-columns:1fr 1fr}
  .masthead{padding-top:32px}
  .wrap{gap:20px}
}
</style>
</head>
<body>

<div class="wrap">
  <header class="masthead">
    <div class="rail"><span class="lab">Daily activity board</span><hr></div>
    <h1>いいね<em>実績</em>ボード</h1>
    <div class="ident">
      <span id="who-name"></span>
      <span class="handle" id="who-handle"></span>
      <span class="span" id="who-range"></span>
    </div>
  </header>

  <div class="hero">
    <div class="slab today">
      <div class="slab-head"><span class="lab">今日のいいね</span><span class="stamp" id="today-date"></span></div>
      <div class="big" id="today-total">—</div>
      <div class="split" id="today-split"></div>
      <div class="readouts">
        <div class="readout"><span class="k"><i class="dot a"></i><span class="lab">おすすめ</span></span><span class="n" id="today-fy">—</span></div>
        <div class="readout"><span class="k"><i class="dot b"></i><span class="lab">フォロー中</span></span><span class="n" id="today-fl">—</span></div>
      </div>
    </div>
    <div class="slab folw">
      <div class="slab-head"><span class="lab">フォロワー</span><span id="folw-chip"></span></div>
      <div class="big f" id="folw-num">—</div>
      <div class="readouts">
        <div class="readout"><span class="k"><i class="dot c"></i><span class="lab">フォロー中</span></span><span class="n" id="folw-ing">—</span></div>
      </div>
    </div>
  </div>

  <div class="strip" id="totals"></div>

  <section>
    <div class="sec-head">
      <h2>推移</h2>
      <div class="legend">
        <span><i class="sw" style="background:var(--vio)"></i>おすすめ</span>
        <span><i class="sw" style="background:var(--amb)"></i>フォロー中</span>
        <span><i class="sw ln" style="background:var(--mint)"></i>フォロワー数</span>
      </div>
    </div>
    <div class="board" id="chart"></div>
  </section>

  <section>
    <div class="sec-head"><h2>日別の記録</h2><span class="lab" id="row-count"></span></div>
    <div class="ledger">
      <table>
        <thead><tr>
          <th>日付</th><th>おすすめ</th><th>フォロー中</th><th>合計</th>
          <th>内訳</th><th>被いいね</th><th>返し率</th><th>フォロワー</th><th>前日比</th><th>転換率</th><th>実行時刻</th>
        </tr></thead>
        <tbody id="rows"></tbody>
      </table>
    </div>
  </section>

  <div class="note">
    <span class="lab">更新のしかた</span>
    <ul>
      <li>「自動いいね」を回すたびに、その日の件数とフォロワー数が追記されます。同じ日に複数回まわした分は合算されます。</li>
      <li>記録の実体は <code>data.json</code>、追記は <code>python3 log.py --foryou 100 --following 50 --followers 447</code></li>
      <li>フォロワーの前日比は、2日目以降から表示されます。</li>
      <li><b>フォロー転換率</b> ＝ フォロワー増加数 ÷ おすすめでいいねした数。<b>いいね返し率</b> ＝ その日の投稿（朝7時・夕方17時ごろの2本）が受け取ったいいね ÷ その日に送ったいいね総数。今日の分の被いいねはまだ伸びるので「集計中」、確定は前日までです。</li>
      <li><b>実行時刻</b>のチップは1回の自動いいね（<span style="color:var(--vio);font-weight:700">紫＝おすすめ</span>／<span style="color:var(--amb);font-weight:700">琥珀＝フォロー中</span>の件数）。赤枠はXの自動化警告で途中停止したランです。</li>
    </ul>
  </div>

  <footer><span class="lab" id="stamp"></span></footer>
</div>

<script>
const DATA = __DATA__;

const days = (DATA.days || []).slice().sort((a,b) => a.date < b.date ? -1 : 1);
const DOW = ["日","月","火","水","木","金","土"];
const nf = n => (n === null || n === undefined) ? "—" : n.toLocaleString("ja-JP");
const parse = d => { const [y,m,dd] = d.split("-").map(Number); return new Date(y, m-1, dd); };
const mmdd = d => { const t = parse(d); return (t.getMonth()+1) + "/" + t.getDate(); };
const dow  = d => DOW[parse(d).getDay()];
const $ = id => document.getElementById(id);

const NOW = new Date();
const TODAY = NOW.getFullYear() + "-" + String(NOW.getMonth()+1).padStart(2,"0") + "-" + String(NOW.getDate()).padStart(2,"0");
days.forEach((d, i) => {
  d.total = (d.foryou || 0) + (d.following || 0);
  const p = i > 0 ? days[i-1] : null;
  d.delta = (p && typeof p.followers === "number" && typeof d.followers === "number")
    ? d.followers - p.followers : null;
  d.pending = d.date >= TODAY;
  d.conv = (d.delta !== null && d.foryou > 0) ? d.delta / d.foryou * 100 : null;
  d.back = (typeof d.likesReceived === "number" && d.total > 0) ? d.likesReceived / d.total * 100 : null;
});
const last = days.length ? days[days.length - 1] : null;

function chipHTML(v, cls){
  const c = cls || "";
  if (v === null || v === undefined) return '<span class="chip flat ' + c + '">前日比 —</span>';
  if (v > 0) return '<span class="chip up ' + c + '">▲ +' + v + '</span>';
  if (v < 0) return '<span class="chip down ' + c + '">▼ ' + v + '</span>';
  return '<span class="chip flat ' + c + '">±0</span>';
}

const pf = v => (v === null || v === undefined) ? "—" : (v >= 0 && v < 10 ? v.toFixed(1) : Math.round(v)) + "%";

/* ── identity ── */
$("who-name").textContent = DATA.displayName || "";
$("who-handle").textContent = "@" + (DATA.account || "");
$("who-range").textContent = days.length
  ? (mmdd(days[0].date) + " — " + mmdd(last.date) + " / " + days.length + "日")
  : "記録なし";

/* ── hero ── */
if (last){
  $("today-date").textContent = mmdd(last.date) + " (" + dow(last.date) + ")";
  $("today-total").innerHTML = nf(last.total) + '<span class="unit">件</span>';
  $("today-fy").textContent = nf(last.foryou);
  $("today-fl").textContent = nf(last.following);
  const t = last.total || 1;
  $("today-split").innerHTML =
    '<i class="a" style="width:' + ((last.foryou||0)/t*100).toFixed(1) + '%"></i>' +
    '<i class="b" style="width:' + ((last.following||0)/t*100).toFixed(1) + '%"></i>';
  $("folw-num").textContent = nf(last.followers);
  $("folw-chip").innerHTML = chipHTML(last.delta, "sm");
  $("folw-ing").textContent = nf(last.followingCount);
}

/* ── totals ── */
const sumAll = days.reduce((s,d) => s + d.total, 0);
const sumFY  = days.reduce((s,d) => s + (d.foryou||0), 0);
const sumFL  = days.reduce((s,d) => s + (d.following||0), 0);
const grow = (days.length > 1 && typeof days[0].followers === "number" && typeof last.followers === "number")
  ? last.followers - days[0].followers : null;
const convDays = days.filter(d => d.conv !== null);
const convTotal = convDays.length
  ? convDays.reduce((s,d) => s + d.delta, 0) / convDays.reduce((s,d) => s + d.foryou, 0) * 100 : null;
const backDays = days.filter(d => d.back !== null && !d.pending);
const backTotal = backDays.length
  ? backDays.reduce((s,d) => s + d.likesReceived, 0) / backDays.reduce((s,d) => s + d.total, 0) * 100 : null;
const cell = (k, n, s) => '<div class="cell"><span class="lab">' + k + '</span><span class="n">' + n + '</span><span class="s">' + s + '</span></div>';
$("totals").innerHTML = days.length ? [
  cell("いいね総数", nf(sumAll), "おすすめ " + nf(sumFY) + " ／ フォロー中 " + nf(sumFL)),
  cell("フォロワー増加", grow === null ? "—" : (grow >= 0 ? "+" : "") + nf(grow), grow === null ? "2日目から表示" : "計測開始から"),
  cell("フォロー転換率", pf(convTotal), "フォロワー増 ÷ おすすめいいね"),
  cell("いいね返し率", pf(backTotal), "被いいね ÷ 送ったいいね（前日まで確定）"),
  cell("計測日数", nf(days.length), "日")
].join("") : '<div class="empty">まだ記録がありません</div>';

/* ── board ── */
(function chart(){
  const host = $("chart");
  if (!days.length){ host.innerHTML = '<div class="empty">記録が入るとここに推移が出ます</div>'; return; }

  const W = 940, H = 280, PL = 50, PR = 62, PT = 14, PB = 38;
  const iw = W - PL - PR, ih = H - PT - PB;
  const n = days.length, band = iw / n;
  const bw = Math.max(7, Math.min(40, band * 0.5));
  const cx = i => PL + band * i + band / 2;

  const maxTotal = Math.max(10, ...days.map(d => d.total));
  const step = Math.max(1, Math.pow(10, Math.floor(Math.log10(maxTotal))) / 2);
  const topY = Math.ceil(maxTotal / step) * step;
  const yL = v => PT + ih - (v / topY) * ih;

  const fv = days.map(d => d.followers).filter(v => typeof v === "number");
  const fmin = fv.length ? Math.min(...fv) : 0, fmax = fv.length ? Math.max(...fv) : 1;
  const pad = Math.max(2, (fmax - fmin) * 0.4);
  const lo = fmin - pad, hi = fmax + pad;
  const yR = v => PT + ih - ((v - lo) / (hi - lo)) * ih;

  let s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="いいね数とフォロワー数の推移">';

  for (let i = 0; i <= 4; i++){
    const v = topY * i / 4, y = yL(v);
    if (i) s += '<line x1="' + PL + '" x2="' + (W-PR) + '" y1="' + y + '" y2="' + y + '" stroke="var(--rule)" stroke-width="1" stroke-dasharray="2 5"/>';
    s += '<text x="' + (PL-11) + '" y="' + (y+3.5) + '" text-anchor="end" font-family="Martian Mono, monospace" font-size="9.5" font-weight="500" fill="var(--muted)">' + v + '</text>';
  }
  s += '<line x1="' + PL + '" x2="' + (W-PR) + '" y1="' + (PT+ih) + '" y2="' + (PT+ih) + '" stroke="var(--rule-2)" stroke-width="1.5"/>';

  days.forEach((d, i) => {
    const x = cx(i) - bw/2, base = PT + ih;
    const hA = (d.foryou||0)/topY*ih, hB = (d.following||0)/topY*ih;
    s += '<g class="grow" style="animation-delay:' + (i*0.045).toFixed(2) + 's">';
    if (hA > 0.6) s += '<rect x="' + x + '" y="' + (base-hA) + '" width="' + bw + '" height="' + hA + '" fill="var(--vio)" rx="2.5"/>';
    if (hB > 0.6) s += '<rect x="' + x + '" y="' + (base-hA-hB-2) + '" width="' + bw + '" height="' + hB + '" fill="var(--amb)" rx="2.5"/>';
    s += '</g>';
    const show = n <= 16 || i % Math.ceil(n/14) === 0 || i === n-1;
    if (show) s += '<text x="' + cx(i) + '" y="' + (H-14) + '" text-anchor="middle" font-family="Martian Mono, monospace" font-size="9.5" font-weight="500" fill="var(--muted)">' + mmdd(d.date) + '</text>';
  });

  const pts = days.map((d,i) => typeof d.followers === "number" ? [cx(i), yR(d.followers)] : null).filter(Boolean);
  if (pts.length > 1){
    const pstr = pts.map(p => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
    let len = 0;
    for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]);
    s += '<polyline fill="none" stroke="var(--mint)" stroke-width="7" stroke-opacity=".14" stroke-linejoin="round" stroke-linecap="round" points="' + pstr + '"/>';
    s += '<polyline class="draw" style="--len:' + Math.ceil(len) + '" fill="none" stroke="var(--mint)" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" points="' + pstr + '"/>';
  }
  pts.forEach((p, i) => {
    const L = i === pts.length - 1;
    if (L) s += '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="9" fill="var(--mint)" opacity=".18"/>';
    s += '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="' + (L ? 4.6 : 2.8) + '" fill="var(--mint)" stroke="var(--panel)" stroke-width="' + (L ? 2.4 : 1.6) + '"/>';
  });
  if (pts.length){
    const p = pts[pts.length-1];
    s += '<text x="' + (W-PR+12) + '" y="' + (p[1]+3.5).toFixed(1) + '" font-family="Martian Mono, monospace" font-size="11" font-weight="700" fill="var(--mint)">' + nf(last.followers) + '</text>';
  }
  host.innerHTML = s + '</svg>';
})();

/* ── ledger ── */
$("row-count").textContent = days.length + " ROWS";
$("rows").innerHTML = days.slice().reverse().map((d, i) => {
  const t = d.total || 1;
  const z = v => v ? nf(v) : '<span class="z">0</span>';
  return '<tr class="' + (i === 0 ? "top" : "") + '">' +
    '<td class="d">' + mmdd(d.date) + '<span class="dw">' + dow(d.date) + '</span>' +
      (d.note ? '<span class="bg">' + d.note + '</span>' : '') + '</td>' +
    '<td>' + z(d.foryou) + '</td>' +
    '<td>' + z(d.following) + '</td>' +
    '<td class="tot">' + nf(d.total) + '</td>' +
    '<td><div class="bar"><i class="a" style="width:' + ((d.foryou||0)/t*100).toFixed(1) + '%"></i>' +
      '<i class="b" style="width:' + ((d.following||0)/t*100).toFixed(1) + '%"></i></div></td>' +
    '<td>' + (typeof d.likesReceived === "number" ? nf(d.likesReceived) + (d.pending ? '<span class="pend">集計中</span>' : '') : '—') + '</td>' +
    '<td>' + (d.back === null ? '—' : pf(d.back) + (d.pending ? '<span class="pend">集計中</span>' : '')) + '</td>' +
    '<td>' + nf(d.followers) + '</td>' +
    '<td>' + chipHTML(d.delta, "sm") + '</td>' +
    '<td>' + pf(d.conv) + '</td>' +
    '<td class="runs">' + ((d.runs && d.runs.length) ? d.runs.map(r =>
      '<span class="runchip' + (r.w ? ' warn' : '') + '"><b>' + r.t + '</b>' +
      (r.fy ? '<i class="fy">' + r.fy + '</i>' : '') +
      (r.fl ? '<i class="fl">' + r.fl + '</i>' : '') + '</span>').join('') : '—') + '</td></tr>';
}).join("");

$("stamp").textContent = "LAST UPDATED " + (DATA.updated || "");
</script>
</body>
</html>
"""

def main():
    with io.open(os.path.join(BASE, "data.json"), encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("updated", "")
    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out = os.path.join(BASE, "index.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("built:", out, "(%d days)" % len(data.get("days", [])))

if __name__ == "__main__":
    main()
