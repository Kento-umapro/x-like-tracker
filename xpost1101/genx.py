import json,sys
items=json.load(open('x_queue_1101_1201.json',encoding='utf-8'))
i=int(sys.argv[1]); it=items[i]
y,m,d=it['date'].split('-'); hh,mm=it['x_time'].split(':')
js=("const T=%s,V=[%d,%d,%d,%d,%d],W=t=>new Promise(r=>setTimeout(r,t));"
"for(let k=0;k<20&&!document.querySelector('[role=dialog] [data-testid=tweetTextarea_0]');k++)await W(500);await W(800);if(document.querySelector('[data-testid=AppTabBar_Profile_Link]')?.getAttribute('href')!='/monja_no_KENT')throw 'me';"
"let ta=document.querySelector('[role=dialog] [data-testid=tweetTextarea_0]');ta.focus();let dt=new DataTransfer();dt.setData('text/plain',T);"
"ta.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));await W(800);"
"document.querySelector('[data-testid=scheduleOption]').click();let s=[];for(let k=0;k<20&&s.length<5;k++){await W(500);s=[...document.querySelectorAll('[role=dialog] select')];}"
"const st=Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set;"
"s.forEach((e,k)=>{st.call(e,String(V[k]));e.dispatchEvent(new Event('change',{bubbles:true}))});await W(500);"
"const sv=s.map(e=>e.value).join('/');document.querySelector('[data-testid=scheduledConfirmationPrimaryAction]').click();await W(1500);"
"const got=document.querySelector('[role=dialog] [data-testid=tweetTextarea_0]').innerText.replace(/\s/g,''),ok=got==T.replace(/\s/g,'');"
"const b=document.querySelector('[role=dialog] [data-testid=tweetButton]');const bt=b.innerText;if(ok&&bt=='Schedule'){b.click();await W(2500);}"
"({i:%d,sv,ok,bt,n:got.length,u:location.href})") % (json.dumps(it['text'],ensure_ascii=False),int(m),int(d),int(y),int(hh),int(mm),i)
print(js)
