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
    # 2026-10-19e：只复制被引用的素材（文件名出现在稿件或 layout-map.json 里），没被引用的（如删掉的截图）不再进 img/
    _ref=open(draft,encoding="utf-8").read()+(open(os.path.join(out,"layout-map.json"),encoding="utf-8").read() if os.path.exists(os.path.join(out,"layout-map.json")) else "")
    _skip=[]
    for f in sorted(sum([glob.glob(os.path.join(d,"*")) for d in srcs],[])):
        if f.lower().endswith((".png",".jpg",".jpeg",".webp",".gif")):
            if os.path.basename(f) in _ref: shutil.copy2(f,img); n+=1
            else: _skip.append(os.path.basename(f))
    print(f"[sync] {n} 张被引用的素材 {shots} → {img}；没被引用、未复制 {len(_skip)} 个")
# 稿件里的【配图：路径，图注】（2026-10-19d）：把图复制进 img/（同名覆盖），成品只用 img/文件名
for _fp in re.findall(r"【配图：([^，】]+)",open(draft,encoding="utf-8").read()):
    _fp=_fp.strip(); _abs=_fp if os.path.isabs(_fp) else os.path.join(os.path.dirname(draft),_fp)
    if os.path.exists(_abs):shutil.copy2(_abs,img);print(f"[fig] 配图 {os.path.basename(_fp)} → img/")
    else:print(f"[fig] ✗ 配图文件不存在：{os.path.basename(_fp)}")
# 签名头像（可选）：layout-map.json 的 signature.avatar 指向的文件需由用户提供，放在输出目录下
here=os.path.dirname(os.path.abspath(__file__))
# 2 生成
cfg=json.load(open(os.path.join(out,"layout-map.json"),encoding="utf-8"))
build.BASE[0]=out
import hashlib as _hlv
_draft_bytes=open(draft,"rb").read(); _draft_md5=_hlv.md5(_draft_bytes).hexdigest(); _draft_mt=os.path.getmtime(draft)  # 2026-10-19e：build 实际读到的定稿版本
frag=build.build(_draft_bytes.decode("utf-8"),cfg)
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
# 可选（2026-10-19b，19c 改）：layout-map 的 standalone = {"jpeg":true,"max_w":700,"quality":90,"nogif":true,"zip_mb":25}
# jpeg：只在 preview-standalone 里把「正文素材截图」（PNG）缩到 max_w（≈2 倍显示宽度）并转成高质量 JPEG 再内嵌；GIF 原样不动；article / wechat-paste / img/ 不变
#   （2026-10-19c）签名卡头像和 master/assets/ 里的一切母版资源一律原样嵌入，不缩、不转 JPEG；publish 的 [embed] 检查拦截
# nogif：另出 preview-standalone-noGIF.html，GIF 位置换成提示框：「此处手动上传 GIF：G0X」+ img/ 里的完整文件名 +「上传后删除本框」（只在这个备用版里有，[leak] 只对这些提示框放行）
# zip_mb：主版超过这个大小（MB）就用 zipfile 打成 <标题>-预览.zip；同时自动写 交付说明.txt（含 build 时定稿的修改时间）。没有 standalone 字段时，输出和以前完全一样
GBOX=f'margin:0;padding:14px 12px;border:2px dashed {build.A};border-radius:8px;background-color:{build.AL};text-align:center;'
_sa=cfg.get("standalone")
_protect={os.path.basename(f) for f in glob.glob(os.path.join(here,"assets","*"))}|({os.path.basename(cfg["signature"]["avatar"])} if isinstance(cfg.get("signature"),dict) and cfg["signature"].get("avatar") else set())
if _sa:
    import io,time
    from PIL import Image as _Im
    _cache={}
    def _b64j(m):
        p=os.path.join(out,m[1]); ext=p.rsplit(".",1)[-1].lower()
        if not _sa.get("jpeg") or ext!="png" or os.path.basename(p) in _protect:return b64(m)  # 母版资源（签名卡头像等）原样嵌入
        if p not in _cache:
            im=_Im.open(p)
            if im.mode in("RGBA","LA","P"):
                im=im.convert("RGBA");bg=_Im.new("RGB",im.size,(255,255,255));bg.paste(im,mask=im.split()[-1]);im=bg
            else:im=im.convert("RGB")
            mw=int(_sa.get("max_w",700))
            if im.size[0]>mw:im=im.resize((mw,round(im.size[1]*mw/im.size[0])),_Im.LANCZOS)
            buf=io.BytesIO();im.save(buf,"JPEG",quality=int(_sa.get("quality",90)),optimize=True,subsampling=0)
            _cache[p]=base64.b64encode(buf.getvalue()).decode()
        return f'src="data:image/jpeg;base64,{_cache[p]}"'
    _page=lambda body:(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} 排版预览</title></head><body style="margin:0;background:#f2f2f2"><section style="max-width:420px;margin:0 auto;background-color:#fff;min-height:100vh;">{body}</section></body></html>')
    _sz0=os.path.getsize(os.path.join(out,"preview-standalone.html"))
    open(os.path.join(out,"preview-standalone.html"),"w",encoding="utf-8").write(_page(re.sub(r'src="(img/[^"]+)"',_b64j,frag)))
    _sz1=os.path.getsize(os.path.join(out,"preview-standalone.html"))
    print(f"[standalone] 正文截图转 JPEG（≤{_sa.get('max_w',700)}px，q{_sa.get('quality',90)}）：{_sz0/1e6:.2f}MB → {_sz1/1e6:.2f}MB；GIF 和母版资源（{'、'.join(sorted(_protect))}）原样嵌入" if _sa.get("jpeg") else f"[standalone] {_sz1/1e6:.2f}MB")
    _ng=[]
    if _sa.get("nogif"):
        def _gbox(m):
            fn=os.path.basename(m[1]); nm=re.match(r"(G\d+)",fn); lab=nm[1] if nm else "GIF"; _ng.append(lab)
            return (f'<section style="{GBOX}">'
              f'<p style="margin:0;font-size:15px;line-height:1.6;font-weight:bold;color:{build.A};"><span leaf="">此处手动上传 GIF：{lab}</span></p>'
              f'<p style="margin:4px 0 0;font-size:12px;line-height:1.6;color:#555;word-break:normal;overflow-wrap:break-word;"><span leaf="">{html.escape(fn)}</span></p>'
              f'<p style="margin:4px 0 0;font-size:12px;line-height:1.6;color:{build.A};"><span leaf="">上传后删除本框</span></p></section>')
        _fg=re.sub(r'<span leaf=""><img src="(img/[^"]+\.gif)"[^>]*></span>',_gbox,frag)
        open(os.path.join(out,"preview-standalone-noGIF.html"),"w",encoding="utf-8").write(_page(re.sub(r'src="(img/[^"]+)"',_b64j,_fg)))
        print(f"[standalone] 备用版 preview-standalone-noGIF.html {os.path.getsize(os.path.join(out,'preview-standalone-noGIF.html'))/1e6:.2f}MB，GIF 提示框 {len(_ng)} 个：{'、'.join(_ng)}")
    _zp=None
    if _sa.get("zip_mb") and _sz1>float(_sa["zip_mb"])*1e6:
        import zipfile
        _zp=os.path.join(out,f"{title}-预览.zip")
        with zipfile.ZipFile(_zp,"w",zipfile.ZIP_DEFLATED) as z:z.write(os.path.join(out,"preview-standalone.html"),"preview-standalone.html")
        print(f"[standalone] 主版超过 {_sa['zip_mb']}MB，已打包 {os.path.basename(_zp)}（{os.path.getsize(_zp)/1e6:.2f}MB）")
    # 交付说明.txt（2026-10-19c）：publish 自动写，定稿版本 = build 时读到的定稿修改时间（本机时区）
    _mt=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(_draft_mt)); _tz=time.strftime("%z")
    _tz=f"UTC{_tz[0]}{int(_tz[1:3])}" if _tz else ""
    _gifs=sorted(dict.fromkeys(os.path.basename(x) for x in re.findall(r'src="(img/[^"]+\.gif)"',frag)))
    _note=[f"交付说明 · {title}（publish 自动生成于 {time.strftime('%Y-%m-%d %H:%M')}{(' '+_tz) if _tz else ''}）",
      f"对应定稿：{os.path.basename(draft)}，修改时间 {_mt}{(' '+_tz) if _tz else ''}",
      f"版本对应：{time.strftime('%H:%M:%S',time.localtime(_draft_mt))} / {_draft_md5[:8]}","",
      "用哪个文件",
      f"- 主版：preview-standalone.html（{_sz1/1e6:.1f}MB，图片"+("和 GIF " if _gifs else "")+"都已内嵌）。"+(f"超过 {_sa['zip_mb']}MB，另打包成「{os.path.basename(_zp)}」（{os.path.getsize(_zp)/1e6:.1f}MB），解压后就是这个文件。" if _zp else ""),
      "- 用法：浏览器打开 → 全选复制 → 粘贴到公众号编辑器 → 逐张检查图片都在"+("、GIF 都会动" if _gifs else "")+"。",
      "- article.html 和 wechat-paste.html 里的图片是相对路径（img/…），公众号读不到，不能拿来粘贴。",
      "- 摘要栏填 summary.txt 里的那一句；标题在编辑器里自己填。"]
    if _sa.get("nogif") and _gifs:
        _note+=["","备用方案（主版粘贴卡顿、丢图或 GIF 不动时用）",
          f"- 打开 preview-standalone-noGIF.html（{os.path.getsize(os.path.join(out,'preview-standalone-noGIF.html'))/1e6:.1f}MB，不含 GIF），全选复制粘贴。",
          f"- 正文里有 {len(_ng)} 个红色虚线框，写着「此处手动上传 GIF：G0X」和文件名。在编辑器里同一位置上传对应 GIF，然后删除这个框；框下面的灰字图注保留。"]
    if _gifs:
        _note+=["","GIF 文件在哪",f"- 本目录 img/ 下："]+[f"  {g}（{os.path.getsize(os.path.join(img,g))/1e6:.2f}MB）" for g in _gifs]
    if build.CHK.get("placeholder"):
        _note+=["","注意",f"- 还有 {len(build.CHK['placeholder'])} 处「配图待补」占位框，发布前必须处理：" ]+[f"  {x}" for x in build.CHK["placeholder"]]
    # 2026-10-19e：layout-map 的 "note_extra" = {"小标题":[行,…],…} 原样追加到交付说明末尾（母版改动、备份位置等）
    for _h,_ls in (cfg.get("note_extra") or {}).items(): _note+=["",_h]+[f"- {x}" for x in _ls]
    open(os.path.join(out,"交付说明.txt"),"w",encoding="utf-8").write("\n".join(_note)+"\n")
    print(f"[standalone] 交付说明.txt 已写入（定稿 {_mt} / {_draft_md5[:8]}）")
print("[build] article.html / wechat-paste.html / preview-standalone.html")
# 2026-10-19e：img/ 只留成品引用到的文件（上次 build 留下、这次没被引用的也清掉）
_used=set(re.findall(r'src="img/([^"]+)"',frag))|({os.path.basename(cfg["signature"]["avatar"])} if isinstance(cfg.get("signature"),dict) and cfg["signature"].get("avatar") else set())
_stale=[f for f in sorted(os.listdir(img)) if f not in _used and f.lower().endswith((".png",".jpg",".jpeg",".webp",".gif"))]
for f in _stale: os.remove(os.path.join(img,f))
print(f"[img] img/ 保留被引用的 {len([f for f in os.listdir(img)])} 个文件"+(f"；清掉没被引用的 {len(_stale)} 个：{'、'.join(_stale)}" if _stale else ""))
# 3 预览图
subprocess.run([os.path.join(here,"render.sh"),out],check=True)
# 4 检查：公开内容不含文件名/内部标记
plain=html.unescape(re.sub(r"<[^>]+>","",frag))
bad=[w for w in re.findall(r"/workspace/|/home/|shots/|gifs/|[\w-]+\.(?:png|jpe?g|gif|webp)\b|初稿|以截图为准|截图：|标注说明|【(?:代码块|代码卡片|代码窗|截图|GIF|动图|引文卡片|配图占位|配图)[^】]*】?|排成代码窗|\d\s*×\s*\d\s*组合",plain)]
print("[leak] 公开文字中的文件名/内部标记：",bad or "无")
# [leak] noGIF 备用版（2026-10-19c）：只对 GIF 提示框（GBOX 样式）里的文件名放行，框外照查
_ngp=os.path.join(out,"preview-standalone-noGIF.html")
if os.path.exists(_ngp) and _sa and _sa.get("nogif"):
    _nh=open(_ngp,encoding="utf-8").read(); _nb=len(re.findall(re.escape(f'<section style="{GBOX}">'),_nh))
    _nh=re.sub(re.escape(f'<section style="{GBOX}">')+r'.*?</section>','',_nh)
    _nh=re.sub(r'src="data:[^"]+"','',_nh); _np=html.unescape(re.sub(r"<[^>]+>","",re.sub(r"<title>.*?</title>","",_nh)))
    _nbad=[w for w in re.findall(r"/workspace/|/home/|shots/|gifs/|[\w-]+\.(?:png|jpe?g|gif|webp)\b|初稿|以截图为准|截图：|标注说明|【(?:代码块|代码卡片|代码窗|截图|GIF|动图|引文卡片|配图占位|配图)[^】]*】?|排成代码窗|\d\s*×\s*\d\s*组合",_np)]
    print(f"[leak] noGIF 备用版：放行 GIF 提示框 {_nb} 个；框外文件名/内部标记：",_nbad or "无")
# [embed]（2026-10-19c）：standalone 和 noGIF 里签名卡必须原样嵌入母版资源（头像 md5 = master/assets），签名卡 HTML 换回 img/ 路径后和 article 逐字节一致
import hashlib as _hl
_SIG=re.compile(r'<section style="margin:36px 0 12px;padding:14px 12px;border:1\.5px dashed #cfcfcf;.*?</section>',re.S)
_sa_ok=True; _sg=_SIG.search(frag)
for _f in ("preview-standalone.html","preview-standalone-noGIF.html"):
    _p=os.path.join(out,_f)
    if not os.path.exists(_p) or not _sg:continue
    if _f.endswith("noGIF.html") and not (_sa and _sa.get("nogif")):continue
    _h=open(_p,encoding="utf-8").read(); _m=_SIG.search(_h)
    if not _m:print(f"[embed] {_f}：找不到签名卡  ✗");_sa_ok=False;continue
    _imgs=re.findall(r'src="data:([^;]+);base64,([^"]+)"',_m[0]); _res=[]
    for _mime,_d in _imgs:
        _md=_hl.md5(base64.b64decode(_d)).hexdigest(); _src=[a for a in _protect if os.path.exists(os.path.join(here,"assets",a)) and _hl.md5(open(os.path.join(here,"assets",a),"rb").read()).hexdigest()==_md]
        _res.append((_mime,_md[:8],_src[0] if _src else None))
    _back=re.sub(r'src="data:[^"]+"',lambda x,it=iter(re.findall(r'src="(img/[^"]+)"',_sg[0])):f'src="{next(it)}"',_m[0])
    _ok=all(r[2] for r in _res) and _back==_sg[0]; _sa_ok&=_ok
    print(f"[embed] {_f} 签名卡：图片 {[f'{a} {b}（'+(c or '不是母版原件')+'）' for a,b,c in _res]}；HTML 与 article 逐字节一致：{'是' if _back==_sg[0] else '否'}"+("  ✓" if _ok else "  ✗"))
print("[todo] 【待补】【待查】：",len(re.findall(r"【待(?:补|查)",plain)),"处")
print("[citecard] 引文卡片：",(f"{len(build.CHK['cite_card'])} 张  ⚠ 【引文卡片】已停用（2026-10-19d 起引用原文一律用截图），请文案官把标记换回【截图：…】" if build.CHK.get("cite_card") else "无"))
print("[todo] 配图占位（发布前换成正式配图）：",(f"{len(build.CHK['placeholder'])} 处："+"；".join(build.CHK["placeholder"])) if build.CHK.get("placeholder") else "无")
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
# [citemax]（2026-10-19d，用户规则）：每篇最多 6 个引用（不同编号数），超了标 ✗；layout-map 可写 cite_max 改上限
_cm=int(cfg.get("cite_max",6))
print(f"[citemax] 不同引用 {len(used)} 个，上限 {_cm} 个"+(f"  ✗ 超出 {len(used)-_cm} 个（请文案官删减到 {_cm} 个以内）" if len(used)>_cm else "  ✓"))
if build.CHK.get("pairs") or build.CHK.get("pair_miss"):print("[pair] 并排双图：",("、".join("＋".join(os.path.basename(x).split("-")[0] for x in g) for g in build.CHK.get("pairs",[])) or "无")+("".join(f"\n       ⚠ side_by_side 组的第一张 {os.path.basename(x)} 后面紧跟的不是同组第二张，已按单张排" for x in build.CHK.get("pair_miss",[]))))
if build.CHK.get("body_tables"):print("[table] 正文表格 v2：","、".join(f"{r} 行 × {k} 列" for r,k in build.CHK["body_tables"]))
if build.CHK.get("body_tables"):print("       不拆开的小段（nowrap span）：",("、".join(f"「{w}」" for w in dict.fromkeys(build.CHK.get("bt_nowrap",[])))) or "无")
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
# [quotegap]（2026-10-19d，用户规则）：390×844 下两张金句卡不能同屏 = 相邻两张的间距（后一张顶 − 前一张底）不能小于一屏 844px
_qg=_j.loads(subprocess.run(["node",os.path.join(here if os.path.exists(os.path.join(here,"quotegap.js")) else os.path.dirname(os.path.abspath(build.__file__)),"quotegap.js"),os.path.join(out,"wechat-paste.html"),"844"],capture_output=True,text=True,env=env).stdout.strip().splitlines()[-1] or "[]")
_qbad=[(a,b2,b2["top"]-a["bottom"]) for a,b2 in zip(_qg,_qg[1:]) if b2["top"]-a["bottom"]<844]
print(f"[quotegap] 金句卡 {len(_qg)} 张"+("".join(f"\n       第 {i+1} 张 top {q['top']}px：{q['text'][:20]}…" for i,q in enumerate(_qg)))
  +("".join(f"\n       ✗ 同屏：「{a['text'][:14]}…」和「{c['text'][:14]}…」间距 {g}px < 844px" for a,c,g in _qbad) if _qbad else ("\n       相邻间距 "+"、".join(f"{c['top']-a['bottom']}px" for a,c in zip(_qg,_qg[1:]))+"，均 ≥ 844px  ✓" if len(_qg)>1 else "  ✓")))
# [halfscreen]（2026-10-19d）：390px 下每张图（截图/GIF/配图）显示高度不能超过半屏 422px；layout-map 的 tall_ok: {文件名: 原因} 单独放行
_hs=_j.loads(subprocess.run(["node",os.path.join(here if os.path.exists(os.path.join(here,"halfscreen.js")) else os.path.dirname(os.path.abspath(build.__file__)),"halfscreen.js"),os.path.join(out,"wechat-paste.html")],capture_output=True,text=True,env=env).stdout.strip().splitlines()[-1] or "[]")
_ok_t=cfg.get("tall_ok",{}); _hb=[x for x in _hs if x["h"]>422 and x["name"] not in _ok_t]; _hp=[x for x in _hs if x["h"]>422 and x["name"] in _ok_t]
print(f"[halfscreen] 图片 {len(_hs)} 张，最高 {max([x['h'] for x in _hs] or [0])}px；超过 422px："+("无" if not(_hb or _hp) else "")
  +"".join(f"\n       ✗ {x['name'][:3]}… {x['w']}×{x['h']}px" for x in _hb)+"".join(f"\n       放行 {x['name'][:14]}… {x['w']}×{x['h']}px（{_ok_t[x['name']]}）" for x in _hp)+("  ✓" if not _hb else "  ✗"))
left=[r for r in bad if not r["fix"] or os.environ.get("ORPHAN_FIX")=="1"]
lc=[r for r in left if r["kind"] not in("highlight","marker")];li=[r for r in left if r["kind"] in("highlight","marker")]
print("[orphan] 卡片/小标题最后一行 ≤2 字、调不好需退给文案官：",("；".join(r["text"] for r in lc)) if lc else "无")
print("[orphan] 内联高亮最后一行 ≤2 字（样式不调，退回文案官改句子）：",("".join(f"\n       {r['kind']} {r['per_line']}：{r['text']}" for r in li)) if li else "无")

# 2026-10-19e：build 之后定稿又变了就报出来（交付说明里写的是 build 实际读到的版本）
import time
_now=_hlv.md5(open(draft,"rb").read()).hexdigest()
print(f"[draft] build 读到的定稿：{time.strftime('%H:%M:%S',time.localtime(_draft_mt))} / {_draft_md5[:8]}"+("；检查结束时定稿未变  ✓" if _now==_draft_md5 else f"；⚠ 检查结束时定稿已变成 {time.strftime('%H:%M:%S',time.localtime(os.path.getmtime(draft)))} / {_now[:8]}，需要重出"))
