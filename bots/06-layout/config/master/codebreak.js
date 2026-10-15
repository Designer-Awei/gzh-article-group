// 用法：node codebreak.js <html> <styles.json>：390px 宽下检查代码窗（2026-10-15i 改）
// styles.json 是 build 记下的代码窗行样式（CHK["code_styles"]），按 style 属性精确匹配；四套母版共用
// 1 逐字检查每一行：只准在空格或逗号处折行，不能在单词中间断开；
// 2 单个「词」（空格或逗号之间）比可见区还宽、或被拆到两行，就报警（long）；
// 3 代码窗宽度不能超过正文栏宽，整页不能横向溢出；
// 4 模拟微信把 overflow / overflow-x 剔掉之后再测一遍 2、3。
const puppeteer=require('puppeteer');const fs=require('fs');
(async()=>{
 const sty=[...new Set(JSON.parse(fs.readFileSync(process.argv[3],'utf8')))];
 const b=await puppeteer.launch({headless:'new',executablePath:process.env.PUPPETEER_EXECUTABLE_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage();await p.setViewport({width:390,height:900,deviceScaleFactor:2});
 await p.goto('file://'+require('path').resolve(process.argv[2]),{waitUntil:'load'});
 await p.addStyleTag({content:'body{font-family:mp-quote,PingFang SC,system-ui,-apple-system,BlinkMacSystemFont,Helvetica Neue,Hiragino Sans GB,Microsoft YaHei UI,Microsoft YaHei,Noto Sans CJK SC,Arial,sans-serif}'});
 const measure=(sty)=>{
  const W=/[A-Za-z0-9_@\-.\/:=~+]/;const out=[];  // W 里没有逗号：逗号后折行是允许的
  // 正文栏：带 padding 的最外层 <section>（wrap），栏宽 = 内容区宽
  const wrap=[...document.querySelectorAll('section')].find(s=>/padding:8px 22px/.test(s.getAttribute('style')||''));
  const wr=wrap.getBoundingClientRect(),wcs=getComputedStyle(wrap);
  const colL=wr.left+parseFloat(wcs.paddingLeft),colR=wr.right-parseFloat(wcs.paddingRight);
  const cards=new Set();
  document.querySelectorAll('p').forEach(e=>{
   if(!sty.includes(e.getAttribute('style')))return;
   let card=e;while(card.parentElement&&card.parentElement!==wrap)card=card.parentElement;cards.add(card);
   const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n,prev=null,lines=1,bad=[];let txt='';
   while(n=w.nextNode()){for(let i=0;i<n.data.length;i++){const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);const q=g.getClientRects()[0];txt+=n.data[i];if(!q||!q.width&&n.data[i]==' ')continue;
     if(prev&&q.top>prev.top+4){lines++;if(W.test(prev.ch)&&W.test(n.data[i]))bad.push(prev.ch+'|'+n.data[i])}
     prev={top:q.top,ch:n.data[i]}}}
   // 超宽单词：按空格切词，逐个量宽度，和这一行的可见宽度（clientWidth 减左右内边距）比
   const cs=getComputedStyle(e);const avail=e.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
   const long=[];const tn=[];const tw=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);while(n=tw.nextNode())tn.push(n);
   if(/^pre/.test(cs.whiteSpace))tn.forEach(t=>{const re=/[^\s,]+,?/g;let m;while(m=re.exec(t.data)){const g=document.createRange();g.setStart(t,m.index);g.setEnd(t,m.index+m[0].length);const rs=[...g.getClientRects()];
     const wd=rs.length==1?rs[0].width:Math.max(...rs.map(r=>r.width));if(rs.length>1||wd>avail+0.5)long.push(`${m[0]}（${Math.round(wd)}px > 可见 ${Math.round(avail)}px）`)}});
   out.push({text:txt,lines,bad,long:[...new Set(long)],overflow:e.scrollWidth>e.clientWidth+1,ws:cs.whiteSpace,mono:/mono/i.test(getComputedStyle(e.querySelector('code')||e).fontFamily),
     breakall:cs.wordBreak=='break-all'||cs.overflowWrap=='anywhere',ox:cs.overflowX})});
  const cw=[...cards].map(c=>{const r=c.getBoundingClientRect();return {w:Math.round(r.width),sw:c.scrollWidth,over:r.right>colR+0.5||r.left<colL-0.5||c.scrollWidth>Math.ceil(r.width)+1}});
  const de=document.documentElement;
  return {lines:out,cards:cw,col:Math.round(colR-colL),page:Math.max(de.scrollWidth,document.body.scrollWidth),vw:window.innerWidth};
 };
 const a=await p.evaluate(measure,sty);
 // 模拟微信剔除 overflow / overflow-x / overflow-y（同时剔除行样式里的，用剔除后的样式重新匹配）
 const sty2=sty.map(s=>s.replace(/overflow(-[xy])?:[^;]*;?/g,''));
 await p.evaluate(()=>document.querySelectorAll('[style]').forEach(e=>e.setAttribute('style',e.getAttribute('style').replace(/overflow(-[xy])?:[^;]*;?/g,''))));
 const s=await p.evaluate(measure,sty2);
 console.log(JSON.stringify({normal:a,stripped:s}));await b.close()})();
