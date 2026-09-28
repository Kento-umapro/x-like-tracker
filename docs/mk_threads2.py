# -*- coding: utf-8 -*-
"""Threads 予約バッチ生成（クリップボード貼付版）
使い方: python3 mk_threads2.py <src> <id>
  src: sep = scheduled_2026-09-18_30.json / oct = plan_threads_2026-10-01_06.json
出力: 1行目=情報 / 2行目=STEP1用base64 JS / 3行目=STEP2用base64 JS
本文は /tmp/t.txt に書き出し、クリップボードにも入れる。
"""
import json, sys, base64, subprocess, datetime

TAB = "1617143982"
BASE = "/Users/kentonishimura/matsumura-x-review/hisho/"
SRC = {"sep": "scheduled_2026-09-18_30.json", "oct": "plan_threads_2026-10-01_06.json"}

src, pid = sys.argv[1], sys.argv[2]
rows = json.load(open(BASE + SRC[src]))
p = [r for r in rows if r["id"] == pid][0]
y, m, d = p["date"].split("-")
hh, mm = p["time"].split(":")
text = p["text"]
TODAY = datetime.date.today()
dd = datetime.date(int(y), int(m), int(d))
WD = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
off = (dd - TODAY).days
if off == 0:
    datelab = "今日"
elif off == 1:
    datelab = "明日"
elif 2 <= off <= 6:
    datelab = WD[dd.weekday()]
else:
    datelab = f"{int(m)}月{int(d)}日"

open("/tmp/t.txt", "w").write(text)
subprocess.run(["osascript", "-e",
                'set the clipboard to (read POSIX file "/tmp/t.txt" as «class utf8»)'], check=True)

exp = json.dumps(text, ensure_ascii=False)

# STEP1: composer を開いて空のエディタにフォーカス
step1 = (
 "(async()=>{"
 "var ex=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>e.getBoundingClientRect().width>0&&e.closest('[role=\"dialog\"]'));"
 "if(!ex){var nb=[...document.querySelectorAll('[role=\"button\"],button,a')].find(b=>b.getBoundingClientRect().width>0&&b.innerText.trim()==='投稿');"
 "if(!nb) throw 'no post btn'; nb.click(); await new Promise(r=>setTimeout(r,3000));}"
 "var ce=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>e.getBoundingClientRect().width>0&&e.closest('[role=\"dialog\"]')&&e.closest('[role=\"dialog\"]').innerText.indexOf('新しいスレッド')>=0);"
 "if(!ce) throw 'no composer editor';"
 "if(ce.innerText.trim().length>0) throw 'editor not empty: '+ce.innerText.slice(0,40);"
 "ce.focus(); await new Promise(r=>setTimeout(r,400)); return 'ready';})()"
)

# STEP2: 本文照合 → 日時指定 → 送信
step2 = (
 "(async()=>{"
 f"var exp={exp};"
 "var ce=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>e.innerText.length>30);"
 "if(!ce) throw 'no editor';"
 "var got=ce.innerText.replace(/\\n+$/,'');"
 "if(got!==exp) throw 'text mismatch len'+got.length+'/'+exp.length+' :: '+got.slice(0,40);"
 "var dg=[...document.querySelectorAll('[role=\"dialog\"]')].find(x=>x.getBoundingClientRect().width>0&&x.innerText.indexOf('新しいスレッド')>=0);"
 "if(!dg) throw 'no composer dialog';"
 "var mb=dg.querySelector('[aria-label=\"もっと見る\"]'); if(!mb) throw 'no more btn';"
 "mb.click(); await new Promise(r=>setTimeout(r,2000));"
 "var mi=[...document.querySelectorAll('[role=\"menuitem\"]')].find(x=>x.innerText.indexOf('日時を指定')===0);"
 "if(!mi) throw 'no menuitem'; mi.click(); await new Promise(r=>setTimeout(r,2800));"
 "var g=document.querySelector('[role=\"grid\"]'); if(!g) throw 'no grid';"
 f"var cell=[...g.querySelectorAll('[role=\"gridcell\"]')].find(x=>x.innerText.indexOf('{y}年{int(m)}月{int(d)}日')===0);"
 "if(!cell) throw 'no cell';"
 "if(cell.getAttribute('aria-disabled')==='true') throw 'cell disabled';"
 "(cell.querySelector('[role=\"button\"],button,div[tabindex]')||cell).click();"
 "await new Promise(r=>setTimeout(r,800));"
 "if(cell.innerText.indexOf('選択済み')<0) throw 'cell not selected: '+cell.innerText.slice(0,30);"
 "var setv=(el,v)=>{var s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(el,v);"
 "el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));};"
 "var H=document.querySelector('input[placeholder=\"hh\"]'),M=document.querySelector('input[placeholder=\"mm\"]');"
 "if(!H||!M) throw 'no time inputs';"
 f"setv(H,'{hh}'); setv(M,'{mm}'); await new Promise(r=>setTimeout(r,600));"
 f"if(H.value!=='{hh}'||M.value!=='{mm}') throw 'time not set '+H.value+':'+M.value;"
 "var done=[...document.querySelectorAll('[role=\"button\"],button')].find(x=>x.innerText.trim()==='完了');"
 "if(!done) throw 'no done'; done.click(); await new Promise(r=>setTimeout(r,1800));"
 "var lab=[...document.querySelectorAll('span,div')].map(x=>x.innerText||'').find(t=>/に投稿予定$/.test(t.trim())&&t.length<60);"
 "if(!lab) throw 'no label';"
 f"if(lab.indexOf('{int(hh)}:{mm}')<0) throw 'label bad: '+lab;"
 f"if(lab.indexOf('{datelab}')<0) throw 'label date bad: '+lab;"
 "ce=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>e.innerText.length>30);"
 "if(!ce||ce.innerText.replace(/\\n+$/,'')!==exp) throw 'text changed';"
 "var sub=[...document.querySelectorAll('[role=\"button\"],button')].filter(x=>x.innerText.trim()==='日時を指定');"
 "var sb=sub[sub.length-1]; if(!sb) throw 'no submit'; sb.click();"
 "await new Promise(r=>setTimeout(r,3500));"
 "var still=!![...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>e.innerText.length>30);"
 "return {lab:lab,chars:exp.length,composerStillOpen:still};})()"
)

def wrap(js):
    b = base64.b64encode(js.encode()).decode()
    return "await eval(new TextDecoder().decode(Uint8Array.from(atob('" + b + "'),c=>c.charCodeAt(0))))"

print(f"{p['date']} {p['time']} {p['id']} vol{p.get('vol')} {p.get('title')} chars={len(text)}")
print(wrap(step1))
print(wrap(step2))
