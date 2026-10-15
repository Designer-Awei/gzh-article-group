// 字数：汉字每个算 1，英文单词/数字每串算 1，标点不算
// 用法：node orphan.js <html>：390px 宽下测金句卡片、导语卡片每行字数；最后一行 ≤2 字时试着微调内边距/字号
const STYLE='01';
const PROFILE={"quote": "margin:0;font-size:20px;line-height:1.65;font-weight:bold;color:#111111;letter-spacing:1px", "lead": "font-size:20px;line-height:1.7;color:#111111;font-weight:bold;letter-spacing:1px", "cap": "margin:8px00;font-size:12px;line-height:1.6;color:#A1A1AA;text-align:left", "hl": "background-color:#FFE4E6;color:#881337;padding:1px2px", "marker": "border-bottom:1pxsolid#E11D48;font-weight:bold;color:#E11D48", "head": ["margin:0;font-size:21px;line-height:1.45;font-weight:bold;color:#111111;letter-spacing:1px", "margin:0;font-size:17px;line-height:1.5;font-weight:bold;color:#111111;letter-spacing:1px", "margin:0;font-size:16px;line-height:1.6;font-weight:bold;color:#111111;letter-spacing:1px"]}; // 新母版的 publish.py 会生成本文件的副本，把这里换成 theme.PROFILE（各识别样式）
const puppeteer=require('puppeteer');
(async()=>{
 const b=await puppeteer.launch({headless:'new',executablePath:process.env.PUPPETEER_EXECUTABLE_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage();await p.setViewport({width:390,height:900,deviceScaleFactor:2});
 await p.goto('file://'+require('path').resolve(process.argv[2]),{waitUntil:'load'});
 await p.addStyleTag({content:'body{font-family:mp-quote,PingFang SC,system-ui,-apple-system,BlinkMacSystemFont,Helvetica Neue,Hiragino Sans GB,Microsoft YaHei UI,Microsoft YaHei,Noto Sans CJK SC,Arial,sans-serif}'});
 const r=await p.evaluate(([STYLE,PROFILE])=>{
  const lines=el=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const rows=[];let n;
   while(n=w.nextNode()){for(let i=0;i<n.data.length;i++){if(/[\p{P}\p{S}]/u.test(n.data[i]))continue;const sp=/\s/.test(n.data[i]);const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);const q=g.getClientRects()[0];if(!q||(sp&&!q.width&&0))continue;
    let row=rows.find(x=>Math.abs(x.t-q.top)<6);if(!row){row={t:q.top,s:''};rows.push(row)}row.s+=n.data[i]}}
   rows.sort((a,b)=>a.t-b.t);return rows.map(x=>x.s)};
  const cnt=s=>(s.match(/\p{Script=Han}/gu)||[]).length+(s.match(/[A-Za-z0-9]+/g)||[]).length;
  const out=[];
  const st=(e,s)=>(e.getAttribute('style')||'').replace(/\s/g,'').includes(s);
  const cards=[];
  // 各套母版的识别样式（去空白后的 style 片段）。STYLE 由文件头常量决定：01 用内置 '01'；其他母版由 PROFILE 指定
  const P=PROFILE||{'01':{quote:'font-size:17px;line-height:1.75;font-weight:bold',lead:'font-size:16px;line-height:1.8;color:#222;font-weight:bold',
      head:['font-size:18px;line-height:1.5;font-weight:bold;color:#111','font-size:18px;font-weight:bold;color:#111;border-bottom:3px','font-size:16px;line-height:1.6;font-weight:bold;color:#111'],
      cap:'font-size:12px;line-height:1.6;color:#888;text-align:center',hl:'background:#FDE9E6;color:#111;padding:1px2px',marker:'background-color:rgba(242,107,91,0.16);border-bottom:2pxsolid#F26B5B'}}[STYLE];
  const key=s=>s.replace(/\s/g,'').slice(0,12);
  const PAD=a=>a.map(v=>['padding-left',v,'padding-right',v]);
  document.querySelectorAll('p,span,td').forEach(e=>{
   const t=e.textContent;
   if(e.tagName=='TD'&&/^\[[A-Za-z]{0,2}\d+\]$/.test(t.trim())){  // 引用表编号列：整格文字（含方括号）只能占一行
     const g=document.createRange();g.selectNodeContents(e);const tops=[];for(const q of g.getClientRects()){if(q.width&&!tops.some(x=>Math.abs(x-q.top)<4))tops.push(q.top)}
     out.push({kind:'引用编号',key:null,text:t.trim(),per_line:tops.map(()=>1),fix:null});return}
   if(e.tagName=='P'&&st(e,P.quote))cards.push({kind:'金句卡',el:e,box:e.parentElement,key:key(t),
     tries:[...PAD(['16px','14px','24px','26px']),['font-size','16px'],['font-size','16px','padding-left','16px','padding-right','16px']]});
   else if(e.tagName=='P'&&e.parentElement&&st(e.parentElement,P.lead))cards.push({kind:'导语卡',el:e,box:e.parentElement.parentElement,key:'lead',
     tries:PAD(['14px','18px','12px','20px'])});
   else if(e.tagName=='TD'&&st(e,'border:0;font-size:15px;line-height:1.8')){const box=e.closest('section');const f=box.querySelector('td+td')||e;
     cards.push({kind:'重点卡',el:e,box,key:key(f.textContent),tries:PAD(['12px','16px','10px','18px'])})}
   else if(e.tagName!='TD'&&P.head.some(h=>st(e,h)))cards.push({kind:'小标题',el:e,box:e,key:'h:'+key(t),
     tries:[['letter-spacing','0px'],['font-size',(parseFloat(getComputedStyle(e).fontSize)-1)+'px'],['font-size',(parseFloat(getComputedStyle(e).fontSize)-1)+'px','letter-spacing','0px'],['font-size',(parseFloat(getComputedStyle(e).fontSize)-2)+'px'],['font-size',(parseFloat(getComputedStyle(e).fontSize)-2)+'px','letter-spacing','0px']]});
   else if(e.tagName=='P'&&st(e,P.cap))cards.push({kind:'图注',el:e,box:e,tries:[]});
   else if(e.tagName=='SPAN'&&st(e,P.hl))cards.push({kind:'highlight',el:e,box:e,tries:[]});
   else if(e.tagName=='SPAN'&&st(e,P.marker))cards.push({kind:'marker',el:e,box:e,tries:[]});
  });
  for(const c of cards){const L=lines(c.el);const o={kind:c.kind,key:c.key||null,text:c.el.textContent.trim(),per_line:L.map(cnt),fix:null};
   if(cnt(L[L.length-1])<=2&&L.length>1){
    for(const t of c.tries){const save=[c.box.style.cssText,c.el.style.cssText];
     for(let i=0;i<t.length;i+=2){(t[i]=='font-size'||t[i]=='letter-spacing'?c.el:c.box).style.setProperty(t[i],t[i+1])}
     const M=lines(c.el);c.box.style.cssText=save[0];c.el.style.cssText=save[1];
     if(cnt(M[M.length-1])>2){o.fix={try:t,per_line:M.map(cnt)};break}}}
   out.push(o)}
  return out},[STYLE,PROFILE]);
 console.log(JSON.stringify(r));await b.close()})();
