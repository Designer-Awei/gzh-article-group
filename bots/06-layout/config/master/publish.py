#!/usr/bin/env python3
"""一条命令：同步截图 → 生成 article.html / wechat-paste.html / preview-standalone.html → 预览长图与分段图 → 合规与泄漏检查
用法：python3 publish.py <文章输出目录> <稿件.md> [截图目录 或 素材目录（自动同步其下 shots/ 和 gifs/）] [--no-sync]
例：python3 bots/06-layout/config/master/publish.py projects/2026-10-12-jev-valuation/layout projects/2026-10-12-jev-valuation/draft/draft.md projects/2026-10-12-jev-valuation/source
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
    srcs=[os.path.join(shots,d) for d in ("shots","gifs") if os.path.isdir(os.path.join(shots,d))] or [shots]
    for f in sorted(sum([glob.glob(os.path.join(d,"*")) for d in srcs],[])):
        if f.lower().endswith((".png",".jpg",".jpeg",".webp",".gif")): shutil.copy2(f,img); n+=1
    print(f"[sync] {n} 张截图 {shots} → {img}")
# 签名头像（可选）：layout-map.json 的 signature.avatar 指向的文件需由用户提供，放在输出目录下
here=os.path.dirname(os.path.abspath(__file__))
# 2 生成
cfg=json.load(open(os.path.join(out,"layout-map.json"),encoding="utf-8"))
build.BASE[0]=out
frag=build.build(open(draft,encoding="utf-8").read(),cfg)
open(os.path.join(out,"article.html"),"w",encoding="utf-8").write(build.doc(frag,os.path.basename(out).split("-",3)[-1]+" 排版"))
# 固定规则（2026-10-15）：副标题不进正文，单独交付 summary.txt（只写副标题原文），用户填到公众号「摘要」栏
if build.CHK["subtitle"]:open(os.path.join(out,"summary.txt"),"w",encoding="utf-8").write(build.CHK["subtitle"]+"\n")
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
bad=[w for w in re.findall(r"shots/|gifs/|[\w-]+\.(?:png|jpe?g|gif|webp)\b|初稿|以截图为准|截图：|标注说明|【(?:代码块|代码卡片|代码窗|截图|GIF|动图)[^】]*】?|排成代码窗|\d\s*×\s*\d\s*组合",plain)]
print("[leak] 公开文字中的文件名/内部标记：",bad or "无")
print("[todo] 【待补】【待查】：",len(re.findall(r"【待(?:补|查)",plain)),"处")
# [head] 成品不能出现标题和副标题原文（标题用户自己填，副标题进 summary.txt）
_n=lambda x:re.sub(r"\s+","",x)
_hits=[k for k,v in (("标题",build.CHK["title"]),("副标题",build.CHK["subtitle"])) if v and _n(v) in _n(plain)]
print(f"[head] 标题/副标题原文出现在成品里："+("、".join(_hits)+"  ✗" if _hits else "无  ✓")+(f"；summary.txt：{build.CHK['subtitle']}" if build.CHK["subtitle"] else "；稿件没有副标题，未生成 summary.txt"))
if build.CHK["cite_move"]:print("[cite] 排版层挪序号：","；".join(build.CHK["cite_move"]))
print("[grid] 图片宫格：",("、".join(f"{n} 格" for n in build.CHK["grid"]) or "无")+"；重复插图（已只留第一份）："+("、".join(build.CHK["dup"]) if build.CHK["dup"] else "无"))
# 出处规则检查（build.CHK 是生成时收集的）
c=build.CHK
# 引用规则（2026-10-15 起）：正文 [xx] 序号 + 文末「编号 | 链接」引用表，一一对应；取代「句尾链接、最多 5 个」
print(f"[link] 正文 Markdown 链接 {len(c['links'])} 个"+("（新规则：正文不放链接，出处改成 [xx] 序号 + 文末引用表，请文案官改）  ✗" if c['links'] else "  ✓"))
for t,u in c['links']:print("       ",t,"→",u)
key=lambda x:(re.sub(r"\d","",x),int(re.sub(r"\D","",x) or 0))
used=[];[used.append(x) for x in c['cite'] if x not in used]
tab=[n for n,_ in c['refs']]; dup=sorted({n for n in tab if tab.count(n)>1},key=key)
miss=[x for x in used if x not in tab]; unused=[n for n in dict.fromkeys(tab) if n not in used]
order_ok=used==sorted(used,key=key); tab_ok=tab==sorted(tab,key=key)
ok=not(miss or unused or dup) and order_ok and tab_ok
rng=lambda a:(f"{a[0]}–{a[-1]}" if len(a)>1 else a[0]) if a else "无"
print(f"[cite] 正文序号 {len(used)} 个（{rng(used)}，共出现 {len(c['cite'])} 次），引用表 {len(tab)} 条"+("，一一对应  ✓" if ok else "  ✗"))
_rep=[x for x in used if c['cite'].count(x)>1]
if _rep:print("       同一引用重复出现（允许）：","、".join(f"{x}×{c['cite'].count(x)}" for x in _rep))
if miss:print("       正文有、引用表没有：",miss)
if unused:print("       引用表有、正文没用到：",unused)
if dup:print("       引用表编号重复：",dup)
if not order_ok:print("       正文序号首次出现不是从小到大：",used)
if not tab_ok:print("       引用表编号没有按顺序排：",tab)
nw=re.findall(r'<td style="([^"]*)"><span leaf="">\[[A-Za-z]{0,2}\d+\]</span></td>',frag)
print(f"[ref]  引用表 {len(c['ref_table'])} 个：{c['ref_table'] or '无'}"+(f"；编号列 white-space:nowrap {sum('white-space:nowrap' in x for x in nw)}/{len(nw)}" if nw else "")
  +("  ✗ "+"；".join(c['ref_bad']) if c['ref_bad'] else ("  ✗ 正文有序号但没有引用表" if used and not tab else ("  ✗ 编号列缺 nowrap" if nw and not all('white-space:nowrap' in x for x in nw) else "  ✓"))))
print("[cap]  图注里的「来源：」类前缀：",(f"{len(c['cap_prefix'])} 处（成品里已自动去掉，请把 layout-map.json 里的原文改掉）："+"；".join(c['cap_prefix'])) if c['cap_prefix'] else "无")
print("[miss] 匹配不上的 highlight/marker/data：",("\n       "+"\n       ".join(f"{k}：{x}" for k,x in c['miss'])+"\n       （成品里没有生效，请按新稿更新 layout-map.json 的原句/锚点）") if c['miss'] else "无")
fam=len(re.findall(r"font-family",frag)); grad=len(re.findall(r"gradient\(",frag)); ta=re.findall(r"text-align:\s*(start|end|justify)",frag); fl=len(re.findall(r"display:\s*flex",frag))
print(f"[spec] font-family={fam} gradient={grad} text-align(start/end/justify)={len(ta)} flex={fl}")
# [nowrap] 数据高亮（data）必须带 white-space:nowrap（2026-10-15g 起，四套都查）：数字和单位不准拆到两行
_dh=[x for x in c["hit"] if x[0]=="data"]; _ds=build.S["data"]; _dn=frag.count(f'style="{_ds}"')
_dok="white-space:nowrap" in _ds.replace(" ","")
print(f"[nowrap] 数据高亮 {len(_dh)} 处（成品里 {_dn} 个 span），样式带 white-space:nowrap："+("是  ✓" if _dok and _dn>=len(_dh) else "否  ✗（请给本套 S['data'] 加 white-space:nowrap）"))
# [codecopy] 代码窗里不能出现「复制」（2026-10-15h 起：微信里复制按钮点了没反应，四套统一用终端代码窗，不放复制按钮/标签，也不放「左右滑动」提示）
_ct=[html.unescape(re.sub(r"<[^>]+>","",x)) for x in c["code_html"]]
_cb1=[t for t in _ct if "复制" in t]; _cb2=[t for t in _ct if "左右滑动" in t]
print(f"[codecopy] 代码窗 {len(_ct)} 个：含「复制」{len(_cb1)} 个，含「左右滑动」{len(_cb2)} 个"+("  ✓" if not (_cb1 or _cb2) else "  ✗"))
# [leadin] 段首加粗引子（**xx：**正文）按段内引子排，不当小标题
print("[leadin] 段首加粗引子：",(f"{len(c['leadin'])} 处："+"、".join(c['leadin'])) if c['leadin'] else "无")

# 5 [orphan] 390px 宽下金句卡片、导语卡片最后一行不能只剩 1–2 个字
import json as _j
env=dict(os.environ,NODE_PATH=os.environ.get("VASS_NODE_PATH","/tmp/vass/cli/node_modules"),PUPPETEER_EXECUTABLE_PATH=os.environ.get("PUPPETEER_EXECUTABLE_PATH","/usr/bin/google-chrome"))
res=_j.loads(subprocess.run(["node",os.path.join(here,"orphan.js"),os.path.join(out,"wechat-paste.html")],capture_output=True,text=True,env=env).stdout.strip().splitlines()[-1])
caps=[r for r in res if r["kind"]=="图注"];refn=[r for r in res if r["kind"]=="引用编号"];res=[r for r in res if r["kind"] not in("图注","引用编号")]
if refn:print(f"[ref]  390px 下引用表编号列 {len(refn)} 格，换行 {sum(len(r['per_line'])>1 for r in refn)} 格"+("  ✓" if all(len(r['per_line'])==1 for r in refn) else "  ✗"))
capbad=[r for r in caps if len(r["per_line"])>1]
print(f"[capline] 图注 {len(caps)} 条，超过一行 {len(capbad)} 条（固定规则：390px 下图注只占一行，超出就精简文字，不缩字号）"+("".join(f"\n       {len(r['per_line'])} 行 {r['per_line']}：{r['text']}" for r in capbad) if capbad else "  ✓"))
bad=[r for r in res if len(r["per_line"])>1 and r["per_line"][-1]<=2]
for r in res:print(f"[orphan] {r['kind']} 每行字数 {r['per_line']}（最后一行 {r['per_line'][-1]} 字）{'  ✗' if r in bad else '  ✓'}：{r['text'][:24]}…")
fixable=[r for r in bad if r["fix"]]
if fixable and os.environ.get("ORPHAN_FIX")!="1":
    mp=os.path.join(out,"layout-map.json");m=_j.load(open(mp,encoding="utf-8"));cf=m.setdefault("card_fit",{})
    for r in fixable:
        t=r["fix"]["try"];box="";txt=""
        for i in range(0,len(t),2):
            if t[i] in("font-size","letter-spacing"):txt+=f"{t[i]}:{t[i+1]};"
            else:box+=f"{t[i]}:{t[i+1]};"
        cf[r.get("key") or ("lead" if r["kind"]=="导语卡" else re.sub(r"\s","",r["text"])[:12])]={"box":box,"text":txt}
    _j.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("[orphan] 已自动微调",len(fixable),"张卡片，写入 layout-map.json 的 card_fit，重新生成…")
    a=[x for x in sys.argv if x!="--no-sync"]+["--no-sync"]
    sys.exit(subprocess.run([sys.executable]+a,env=dict(os.environ,ORPHAN_FIX="1")).returncode)
# [codebreak] 390px 下代码窗检查（2026-10-15i）：命令在空格/逗号处折行，不准在单词中间断开；超宽单词报警；代码窗 ≤ 正文栏、整页不横向溢出；模拟剔除 overflow 后再查
if build.CHK["code_styles"]:
    _sj=os.path.join(out,"_codestyles.json");open(_sj,"w",encoding="utf-8").write(json.dumps(build.CHK["code_styles"],ensure_ascii=False))
    _cb=_j.loads(subprocess.run(["node",os.path.join(here if os.path.exists(os.path.join(here,"codebreak.js")) else os.path.dirname(os.path.abspath(build.__file__)),"codebreak.js"),os.path.join(out,"wechat-paste.html"),_sj],capture_output=True,text=True,env=env).stdout.strip().splitlines()[-1]);os.remove(_sj)
    # 2026-10-15i：命令行 pre-wrap 在空格/逗号处折行；另查代码窗宽度 ≤ 正文栏宽、整页不横向溢出，并模拟微信剔除 overflow/overflow-x 后再查一遍
    _ok=True
    for _k,_nm in (("normal","正常"),("stripped","剔除 overflow 后")):
        _r=_cb[_k]; _L=_r["lines"]; _cmd=[x for x in _L if x["ws"] in("pre","pre-wrap")]
        _bad=[x for x in _L if x["bad"] or x["breakall"]]; _long=[x for x in _L if x["long"]]; _ovl=[x for x in _L if x["overflow"]]
        _cw=[c for c in _r["cards"] if c["over"]]; _pg=_r["page"]>_r["vw"]
        _o=not(_bad or _long or _ovl or _cw or _pg); _ok&=_o
        print(f"[codebreak] {_nm}：代码窗 {len(_r['cards'])} 个、{len(_L)} 行；单词中间断行 {len(_bad)} 行；命令 {len(_cmd)} 行（每行折成 {[x['lines'] for x in _cmd]} 行，white-space={'/'.join(sorted({x['ws'] for x in _cmd})) or '-'}，overflow-x={'/'.join(sorted({x['ox'] for x in _cmd})) or '-'}，等宽 {sum(x['mono'] for x in _cmd)}/{len(_cmd)}）；"
              f"超宽单词 {sum(len(x['long']) for x in _L)} 个；代码窗宽 {[c['w'] for c in _r['cards']]}px / 正文栏 {_r['col']}px，超出 {len(_cw)} 个；整页宽 {_r['page']}px / 视口 {_r['vw']}px"+("  ✓" if _o else "  ✗"))
        for x in _bad:print("       ✗ 单词中间断行",x["bad"],x["text"][:50])
        for x in _long:print("       ✗ 单词比可见区还宽：","；".join(x["long"]))
        for x in _ovl:print("       ✗ 行内容溢出：",x["text"][:50])
    print("[codebreak] 合计"+("  ✓" if _ok else "  ✗"))
else:print("[codebreak] 没有代码窗")
left=[r for r in bad if not r["fix"] or os.environ.get("ORPHAN_FIX")=="1"]
lc=[r for r in left if r["kind"] not in("highlight","marker")];li=[r for r in left if r["kind"] in("highlight","marker")]
print("[orphan] 卡片/小标题最后一行 ≤2 字、调不好需退给文案官：",("；".join(r["text"] for r in lc)) if lc else "无")
print("[orphan] 内联高亮最后一行 ≤2 字（样式不调，退回文案官改句子）：",("".join(f"\n       {r['kind']} {r['per_line']}：{r['text']}" for r in li)) if li else "无")
