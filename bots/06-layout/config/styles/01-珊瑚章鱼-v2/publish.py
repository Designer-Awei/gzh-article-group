#!/usr/bin/env python3
"""一条命令：同步截图 → 生成 article.html / wechat-paste.html / preview-standalone.html → 预览长图与分段图 → 合规与泄漏检查
用法：python3 publish.py <文章输出目录> <稿件.md> [截图目录] [--no-sync]
例：python3 bots/06-layout/config/master/publish.py projects/2026-10-12-jev-valuation/layout projects/2026-10-12-jev-valuation/draft/draft.md projects/2026-10-12-jev-valuation/source/shots
"""
import sys,os,re,glob,shutil,base64,json,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build
args=[a for a in sys.argv[1:] if not a.startswith("--")]
out,draft=os.path.abspath(args[0]),os.path.abspath(args[1]); shots=args[2] if len(args)>2 else None
img=os.path.join(out,"img"); os.makedirs(img,exist_ok=True)
# 1 同步截图（只拷 shots/ 里的截图，覆盖同名文件）
if shots and "--no-sync" not in sys.argv:
    n=0
    for f in sorted(glob.glob(os.path.join(shots,"*"))):
        if f.lower().endswith((".png",".jpg",".jpeg",".webp",".gif")): shutil.copy2(f,img); n+=1
    print(f"[sync] {n} 张截图 {shots} → {img}")
# 签名头像
here=os.path.dirname(os.path.abspath(__file__))
shutil.copy2(os.path.join(here,"assets","octo-sign.png"),img)
# 2 生成
cfg=json.load(open(os.path.join(out,"layout-map.json"),encoding="utf-8"))
build.BASE[0]=out
frag=build.build(open(draft,encoding="utf-8").read(),cfg)
open(os.path.join(out,"article.html"),"w",encoding="utf-8").write(build.doc(frag,"Jev估值 排版"))
wrap=lambda f:f'<section style="max-width:420px;margin:0 auto;background-color:#fff;">{f}</section>'
open(os.path.join(out,"wechat-paste.html"),"w",encoding="utf-8").write(
  f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>粘贴用</title></head><body style="margin:0;background:#f2f2f2">{wrap(frag)}</body></html>')
mime={"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg","gif":"image/gif","webp":"image/webp"}
def b64(m):
    p=os.path.join(out,m[1]); ext=p.rsplit(".",1)[-1].lower()
    return f'src="data:{mime[ext]};base64,{base64.b64encode(open(p,"rb").read()).decode()}"'
emb=re.sub(r'src="(img/[^"]+)"',b64,frag)
title=os.path.basename(out).split("-",3)[-1]
open(os.path.join(out,"preview-standalone.html"),"w",encoding="utf-8").write(
  f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} 排版预览</title></head><body style="margin:0;background:#f2f2f2"><section style="max-width:420px;margin:0 auto;background-color:#fff;min-height:100vh;">{emb}</section></body></html>')
print("[build] article.html / wechat-paste.html / preview-standalone.html")
# 3 预览图
subprocess.run([os.path.join(here,"render.sh"),out],check=True)
# 4 检查：公开内容不含文件名/内部标记
plain=html.unescape(re.sub(r"<[^>]+>","",frag))
bad=[w for w in re.findall(r"shots/|[\w-]+\.(?:png|jpe?g|gif|webp)\b|初稿|以截图为准|截图：|标注说明",plain)]
print("[leak] 公开文字中的文件名/内部标记：",bad or "无")
print("[todo] 【待补】【待查】：",len(re.findall(r"【待(?:补|查)",plain)),"处")
fam=len(re.findall(r"font-family",frag)); grad=len(re.findall(r"gradient\(",frag)); ta=re.findall(r"text-align:\s*(start|end|justify)",frag); fl=len(re.findall(r"display:\s*flex",frag))
print(f"[spec] font-family={fam} gradient={grad} text-align(start/end/justify)={len(ta)} flex={fl}")
