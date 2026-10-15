#!/bin/bash
# 用法：render.sh <目录>：渲染 wechat-paste.html（390px@2x）→ preview.png + preview-N.png（先删旧图）
cd "$1" && rm -f preview.png preview-[1-9]*.png _full.png
sed 's|<body style="|<body style="font-family:mp-quote,PingFang SC,system-ui,-apple-system,BlinkMacSystemFont,Helvetica Neue,Hiragino Sans GB,Microsoft YaHei UI,Microsoft YaHei,Noto Sans CJK SC,Arial,sans-serif;|' wechat-paste.html > _render.html
# 预览用公众号默认字体栈模拟阅读端（只加在渲染临时文件的 body 上，不进入正文片段）
google-chrome --headless=new --no-sandbox --hide-scrollbars --force-device-scale-factor=2 --window-size=390,40000 --screenshot=_full.png "file://$PWD/_render.html" 2>/dev/null
python3 - <<'PY'
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
im=Image.open('_full.png').convert('RGB');w,h=im.size;px=im.load();y=h-1
bg=px[2,h-1]
while y>0 and all(px[x,y]==bg for x in range(0,w,7)):y-=1
im=im.crop((0,0,w,y+40));im.save('preview.png');n=0
for t in range(0,im.size[1],2400):
    n+=1;im.crop((0,t,w,min(t+2400,im.size[1]))).save(f'preview-{n}.png')
print('[render] preview.png',im.size,'分段',n)
PY
rm -f _full.png _render.html
