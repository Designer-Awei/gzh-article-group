// [halfscreen]（2026-10-19d）：390px 宽下每张正文图片的显示宽高。用法：node halfscreen.js <html>
const puppeteer=require('puppeteer');
(async()=>{const b=await puppeteer.launch({headless:'new',executablePath:process.env.PUPPETEER_EXECUTABLE_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage();await p.setViewport({width:390,height:844,deviceScaleFactor:1});
 await p.goto('file://'+require('path').resolve(process.argv[2]),{waitUntil:'load'});
 const r=await p.evaluate(()=>[...document.images].filter(i=>i.getAttribute('width')!=='64')  /* 排除签名卡头像（width=64） */.map(i=>{const q=i.getBoundingClientRect();return {name:decodeURIComponent(i.src).split('/').pop(),w:Math.round(q.width),h:Math.round(q.height)}}));
 console.log(JSON.stringify(r));await b.close()})();
