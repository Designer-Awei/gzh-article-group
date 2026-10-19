// [quotegap]（2026-10-19d）：390×844 下两张金句卡不能同屏。用法：node quotegap.js <html> [屏高=844]
// 输出 JSON：每张金句卡的 top/bottom（页面坐标 px）和文字；publish 按相邻两张的间距（后一张顶 − 前一张底）判断
const puppeteer=require('puppeteer');
(async()=>{
 const b=await puppeteer.launch({headless:'new',executablePath:process.env.PUPPETEER_EXECUTABLE_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage();await p.setViewport({width:390,height:+(process.argv[3]||844),deviceScaleFactor:1});
 await p.goto('file://'+require('path').resolve(process.argv[2]),{waitUntil:'load'});
 await p.addStyleTag({content:'body{font-family:mp-quote,PingFang SC,system-ui,-apple-system,BlinkMacSystemFont,Helvetica Neue,Hiragino Sans GB,Microsoft YaHei UI,Microsoft YaHei,Noto Sans CJK SC,Arial,sans-serif}'});
 const r=await p.evaluate(()=>[...document.querySelectorAll('p')].filter(e=>(e.getAttribute('style')||'').replace(/\s/g,'').includes('font-size:17px;line-height:1.75;font-weight:bold')).map(e=>{const q=e.parentElement.getBoundingClientRect();return {top:Math.round(q.top+scrollY),bottom:Math.round(q.bottom+scrollY),text:e.textContent.trim()}}));
 console.log(JSON.stringify(r));await b.close()})();
