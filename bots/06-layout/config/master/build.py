#!/usr/bin/env python3
"""排版母版 v2.1（gzh-design-skill + 微信内容结构规范兼容）：python3 build.py 稿件.md out.html layout-map.json"""
import re, sys, json, html
A="#F26B5B"; AL="#FDE9E6"; T="#2b2b2b"; G="#888"; LN="#eee"; BG="#f7f7f7"
FONT=None  # 微信规范第3节：不设置 font-family，使用公众号默认字体栈
S={
 "wrap":f"padding:8px 22px;box-sizing:border-box;color:{T};font-size:15px;line-height:1.8;letter-spacing:0.5px;word-break:break-word;background:#fff;",
 "h1":"font-size:22px;line-height:1.45;font-weight:bold;color:#111;margin:24px 0 8px;",
 "subtitle":f"font-size:14px;color:{G};margin:0 0 18px;",
 "p":"margin:0 0 18px;text-align:left;",
 "strong":"font-weight:bold;color:#111;",
 # 重点句：珊瑚色底纹 / 马克笔下划线（底部 40% 半透明色带）
 "hl":f"background:{AL};color:#111;padding:1px 2px;border-radius:2px;",
 "marker":f"background-color:rgba(242,107,91,0.16);border-bottom:2px solid #F26B5B;color:#111;font-weight:bold;padding:0 1px;",
 "data":f"color:{A};font-weight:bold;font-size:17px;padding:0 1px;white-space:nowrap;",  # 2026-10-15g：加 nowrap（同 02–04），数字和单位不拆到两行
 "link":f"color:{A};text-decoration:underline;",
 "linkurl":f"font-size:12px;color:{G};",
 "note":"background:#fff4d6;color:#8a5a00;padding:0 3px;font-size:14px;",
 "quote":f"margin:0 0 20px;padding:12px 14px;background:{BG};border-left:3px solid {A};color:#555;font-size:14px;line-height:1.75;",
 "img":"display:block;max-width:100%;height:auto;margin:0 auto;border-radius:4px;",
 "shot":f"display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid {LN};border-radius:4px;box-sizing:border-box;",
 "fig":"margin:8px 0 22px;",
 "cap":f"margin:6px 0 0;font-size:12px;line-height:1.6;color:{G};text-align:center;",
 "table":"width:100%;table-layout:auto;border-collapse:collapse;font-size:12px;line-height:1.6;margin:0 0 20px;",
 "th":f"background:{AL};border:1px solid {LN};padding:6px;text-align:left;font-weight:bold;color:#111;",
 "td":f"border:1px solid {LN};padding:6px;vertical-align:top;word-break:break-all;",
 # 引用：正文 [xx] 序号 + 文末引用表（2026-10-15 起，取代「句尾链接、最多 5 个」）
 "cite":f"font-size:11px;line-height:1;color:{A};vertical-align:super;padding:0 1px;white-space:nowrap;",
 "ref_table":"width:100%;table-layout:auto;border-collapse:collapse;font-size:12px;line-height:1.6;margin:0 0 20px;",
 "ref_th":f"background:{AL};border:0;border-bottom:1px solid {LN};padding:6px 8px;text-align:left;font-weight:bold;color:#111;",
 "ref_num":f"width:44px;min-width:44px;white-space:nowrap;padding:6px 8px;border:0;border-bottom:1px solid {LN};vertical-align:top;color:{A};font-weight:bold;",
 "ref_url":f"padding:6px 8px;border:0;border-bottom:1px solid {LN};vertical-align:top;color:{G};word-break:normal;overflow-wrap:break-word;",
 # 行内代码 `x`（2026-10-15）：浅灰底小圆角；用 <code> 标签让阅读端走等宽字体（不写 font-family），短的整段不换行
 "icode":"background-color:#F3F4F6;color:#24292F;font-size:13px;padding:1px 4px;border-radius:3px;letter-spacing:0px;word-break:normal;overflow-wrap:normal;",
 # 章节内小标题（### 或整行 **加粗**，2026-10-15）：16px 加粗 + 左侧 4px 珊瑚短竖条，比章节大序号低一级
 "sub":"margin:0;font-size:16px;line-height:1.6;font-weight:bold;color:#111;",
 # 段首加粗引子（段落开头的 **xx：** / **xx**，2026-10-15g）：珊瑚色加粗 + 3×14 珊瑚短竖条，和章节内小标题的 4×16 竖条同一套；还是正文段落，不是小标题
 "leadin":f"font-weight:bold;color:{A};",
}
CUR=[""]
CN="一二三四五六七八九十"
CHK={"narrow":[],"code_html":[],"leadin":[],"links":[],"cite":[],"ref_table":[],"refs":[],"ref_bad":[],"cap_prefix":[],"hit":[],"miss":[],"title":"","subtitle":"","cite_move":[],"code_styles":[],"dup":[],"grid":[]}
META={}  # 开头区元信息：tag / date / mins（阅读分钟）/ chapters（编号章节数）
LINK_MAX=5
def short_domain(url):
    """链接后面只显示短域名：去掉协议、www.、端口和路径，例如 arstechnica.com；不加括号"""
    h=re.sub(r"^https?://","",url).split("/")[0].split("?")[0].split("#")[0].split(":")[0].lower()
    return h[4:] if h.startswith("www.") else h
def link_html(text,url):
    """句尾出处链接。公众号正文里外链不可点（编辑器会去掉非公众号文章的 <a>），
    所以链接文字珊瑚色加下划线，后面跟一个空格和灰色小字的短域名（不加括号，不写路径）；
    只有 mp.weixin.qq.com 的公众号文章链接才保留 <a>，可以点。"""
    tx=html.escape(text,quote=False); u=html.escape(url,quote=True)
    if re.match(r"https?://mp\.weixin\.qq\.com/",url):
        return f'<a href="{u}" style="{S["link"]}">{tx}</a>'
    return f'<span style="{S["link"]}">{tx}</span><span style="{S["linkurl"]}"> {html.escape(short_domain(url),quote=False)}</span>'
LEADIN_MAX=12  # 引子不超过 12 个字时整段 nowrap（标记和文字不分家）
def leadin(inner,raw):
    """段首加粗引子：3×14 珊瑚短竖条 + 珊瑚色加粗（01）。各套 theme 可以覆盖 build.leadin 换成自己的标记"""
    nw="white-space:nowrap;" if len(re.sub(r"\s","",raw))<=LEADIN_MAX else ""
    return (f'<span style="{S["leadin"]}{nw}"><span style="display:inline-block;width:3px;height:14px;background-color:{A};border-radius:2px;margin-right:6px;vertical-align:-2px;"></span>{inner}</span>')
def inline(t,cfg,para=False):
    links=[]
    def keep(m):
        links.append(link_html(m[1],m[2])); CHK["links"].append((m[1],m[2])); return f"\x00{len(links)-1}\x00"
    t=re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",keep,t)
    codes=[]
    def kc(m):
        x=m[1]; st=S.get("icode","")+("white-space:nowrap;" if len(x)<=28 else "")
        codes.append(f'<code style="{st}">{html.escape(x,quote=False)}</code>'); return f"\x03{len(codes)-1}\x03"
    t=re.sub(r"`([^`\n]+)`",kc,t)  # 行内代码先保护起来，不参与高亮/数据匹配
    cites=[]
    def ck(m):
        cites.append(m[0]); CHK["cite"].append(m[0]); return f"\x02{len(cites)-1}\x02"
    t=re.sub(r"\[[A-Za-z]{0,2}\d+\]",ck,t)  # 正文 [xx] 序号保留，渲染成上标小字（和文末引用表一一对应）
    t=html.escape(t,quote=False)
    if para:
        # 段首加粗引子（**小红书小工具：**…、**B站**给…）：按段内引子排，不当小标题；后面其余的 ** 照旧是普通加粗
        def li(m):
            raw=html.unescape(re.sub(r"\x02\d+\x02","",m[1])); CHK["leadin"].append(raw); return leadin(m[1],raw)
        t=re.sub(r"^\*\*(.+?)\*\*",li,t,count=1)
    t=re.sub(r"\*\*(.+?)\*\*",lambda m:f'<strong style="{S["strong"]}">{m[1]}</strong>',t)
    for s in cfg.get("highlight",[]):
        e=html.escape(s,quote=False)
        if e in t: t=t.replace(e,f'<span style="{S["hl"]}">{e}</span>',1); CHK["hit"].append(("highlight",s))
    for s in cfg.get("marker",[]):
        e=html.escape(s,quote=False)
        if e in t: t=t.replace(e,f'<span style="{S["marker"]}">{e}</span>',1); CHK["hit"].append(("marker",s))
    for j,(pre,s) in enumerate(cfg.get("data",[])):
        # 段内包含锚点即匹配（原来是段首匹配）；每条 data 只用一次，避免别的段落也含锚点时重复放大
        if pre not in CUR[0] or ("data",j) in CHK["hit"]:continue
        e=html.escape(s,quote=False); t0=t
        lb=r"(?<![0-9A-Za-z.>])" if cfg.get("data_cjk") else r"(?<![\w.>])"  # data_cjk:true 时数字前紧挨汉字也能放大（默认关，旧稿输出不变）
        t=re.sub(lb+re.escape(e)+r"(?![^<]*</span>)",f'<span style="{S["data"]}">{e}</span>',t,count=1)
        if t!=t0:CHK["hit"].append(("data",j))
    t=re.sub(r"(【(?:待补|待查)[^】]*】)",lambda m:f'<span style="{S["note"]}">{m[1]}</span>',t)
    t=re.sub(r"\x00(\d+)\x00",lambda m:links[int(m[1])],t)
    # 序号和前面紧挨的那个字（或整个数据高亮）粘在一起不换行，避免 [xx] 单独掉到下一行开头
    cs=lambda m:f'<span style="{S["cite"]}">{html.escape(cites[int(m)])}</span>'
    glue=lambda a,m:f'<span style="white-space:nowrap;">{a}{cs(m)}</span>'
    t=re.sub(r'(<span style="'+re.escape(S["data"])+r'">[^<]*</span>)\x02(\d+)\x02',lambda m:glue(m[1],m[2]),t)
    t=re.sub(r'(&\w+;|[^\s<>\x00-\x02])\x02(\d+)\x02',lambda m:glue(m[1],m[2]),t)
    t=re.sub(r"\x02(\d+)\x02",lambda m:cs(m[1]),t)
    t=re.sub(r"\x03(\d+)\x03",lambda m:codes[int(m[1])],t)
    return t
# ---------- 组件 ----------
BASE=["."]
def imgw(src):
    try:
        from PIL import Image; import os
        return Image.open(os.path.join(BASE[0],src)).size[0]
    except Exception: return None
SHOW_CAP=[True]  # 固定规则：每张图下面输出一句说明（cfg 里 "show_captions": false 可整篇关掉）
CAP_PREFIX=re.compile(r"^\s*[^\s，。：:]{0,8}?(?:来源|出处|via|Source)\s*[：:]\s*",re.I)
def clean_cap(cap):
    """图注只写画面内容；「来源：」「截图来源：」「动图来源：」这类前缀自动去掉，并记进检查"""
    if not cap:return ""
    c=CAP_PREFIX.sub("",cap)
    if c!=cap:CHK["cap_prefix"].append(cap)
    return c
def figure(src,cap,shot=False,width=None):
    """width（2026-10-15k 起，可选）：竖图/小图缩宽居中显示。整数 = 显示宽度 px（推荐，如 208 ≈ 正文栏 346px 的 60%）：
    同时写 width 属性、data-w（= 显示宽度，微信可能把 data-w 当宽度）和 style 的 width + max-width:100%；
    字符串 "60%" = 占正文栏的百分比（data-w 按 346px 栏宽折算）。缩宽的图一律不加边框，只有 4px 圆角，居中"""
    cap=clean_cap(cap)
    c=f'<p style="{S["cap"]}">{html.escape(cap)}</p>' if cap and SHOW_CAP[0] else ""
    if width:
        if isinstance(width,str) and width.strip().endswith("%"):
            pc=float(width.strip()[:-1]); px=round(346*pc/100); st=f"display:block;width:{pc:g}%;max-width:{pc:g}%;height:auto;margin:0 auto;border-radius:4px;"
        else:
            px=int(width); st=f"display:block;width:{px}px;max-width:100%;height:auto;margin:0 auto;border-radius:4px;"
        CHK.setdefault("narrow",[]).append((src,width))
        return f'<section style="{S["fig"]}"><span leaf=""><img src="{src}" data-w="{px}" width="{px}" style="{st}" alt=""></span>{c}</section>'
    w=imgw(src); dw=f' data-w="{w}"' if w else ""
    return f'<section style="{S["fig"]}"><span leaf=""><img src="{src}"{dw} style="{S["shot" if shot else "img"]}" alt=""></span>{c}</section>'
def grid(items,cols=2,gap=6):
    """图片宫格（2026-10-15 起，gif_grid 字段）：table 实现（不用 flex/grid），默认 2 列；格子之间用 td 内边距留 gap px 小间距。
    每格一张纯图（不加边框、窗口、相框），下面一行图注（只写名称，390px 下单格内一行）；图片 max-width:100% 自适应，data-w 写原图宽度"""
    rows=[items[k:k+cols] for k in range(0,len(items),cols)];h=gap//2;tr=""
    for ri,r in enumerate(rows):
        td=""
        for j in range(cols):
            pl=0 if j==0 else h; pr=0 if j==cols-1 else h; pb=0 if ri==len(rows)-1 else gap
            st=f"width:{100//cols}%;vertical-align:top;padding:0 {pr}px {pb}px {pl}px;border:0;"
            if j>=len(r):td+=f'<td style="{st}"></td>';continue
            src,cap=r[j][0],clean_cap(r[j][1] if len(r[j])>1 else "")
            w=imgw(src);dw=f' data-w="{w}"' if w else ""
            c=f'<p style="{S["cap"]}">{html.escape(cap)}</p>' if cap and SHOW_CAP[0] else ""
            td+=f'<td style="{st}"><span leaf=""><img src="{src}"{dw} style="{S["img"]}" alt=""></span>{c}</td>'
        tr+=f"<tr>{td}</tr>"
    return f'<section style="{S["fig"]}"><table style="width:100%;table-layout:fixed;border-collapse:collapse;margin:0;"><tbody>{tr}</tbody></table></section>'
def divider():
    d=lambda c,s:f'<span style="display:inline-block;width:{s}px;height:{s}px;border-radius:50%;background:{c};margin:0 5px;vertical-align:middle;"></span>'
    return f'<section style="text-align:center;margin:30px 0 8px;line-height:1;">{d("#ddd",5)}{d(A,7)}{d("#ddd",5)}</section>'
def chapter(title,cfg):
    _,ft=fit(cfg,"h:"+re.sub(r"\s","",re.sub(r"^[一二三四五六七八九十]+、","",title))[:12])
    m=re.match(r"([一二三四五六七八九十]+)、(.*)",title)
    if not m:
        return f'<section style="margin:34px 0 16px;"><span style="font-size:18px;font-weight:bold;color:#111;border-bottom:3px solid {A};padding-bottom:3px;{ft}">{inline(title,cfg)}</span></section>'
    n=CN.index(m[1][-1])+1+(9 if len(m[1])>1 else 0)
    return (f'<section style="margin:36px 0 18px;">'
      f'<p style="margin:0;font-size:44px;line-height:1;font-weight:bold;color:{A};letter-spacing:1px;">{n:02d}<span style="font-size:22px;color:#222;font-weight:normal;margin-left:8px;vertical-align:middle;">—</span></p>'
      f'<p style="margin:8px 0 0;font-size:18px;line-height:1.5;font-weight:bold;color:#111;{ft}">{inline(m[2],cfg)}</p></section>')
def fit(cfg,key):
    """[orphan] 自动微调：layout-map.json 的 card_fit[key] = {"box": 卡片外框追加样式, "text": 文字追加样式}"""
    f=cfg.get("card_fit",{}).get(key,{});return f.get("box",""),f.get("text","")
def lead_card(paras,cfg):
    fb,ft=fit(cfg,"lead")
    body="".join(f'<p style="margin:0 0 8px;{ft}">{(CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in paras)
    return (f'<section style="margin:4px 0 24px;padding:16px 16px 10px;border:1.5px solid #222;border-radius:10px 4px 12px 4px;box-shadow:4px 4px 0 {AL};{fb}">'
      f'<p style="margin:0 0 8px;font-size:12px;letter-spacing:2px;color:{A};font-weight:bold;">导语 · LEAD</p>'
      f'<section style="font-size:15px;line-height:1.8;color:#333;">{body}</section></section>')
def quote_card(text,cfg):
    fb,ft=fit(cfg,re.sub(r"\s","",text)[:12])
    return (f'<section style="margin:26px 0;padding:22px 20px 18px;background:#fff;border:1.5px solid #222;border-radius:4px 14px 4px 14px;text-align:center;{fb}">'
      f'<p style="margin:0;font-size:36px;line-height:1;height:22px;overflow:visible;color:{A};">“</p>'
      f'<p style="margin:10px 0 0;font-size:17px;line-height:1.75;font-weight:bold;color:#111;{ft}">{inline(text,cfg)}</p>'
      f'<p style="margin:12px 0 0;text-align:center;line-height:1;"><span style="display:inline-block;padding:0 14px;border-bottom:3px solid {A};"></span></p></section>')
def points_card(lines,cfg,title=""):
    fb,ft=fit(cfg,re.sub(r"\s","",lines[0])[:12])
    rows="".join(f'<tr><td style="width:1%;vertical-align:top;padding:2px 10px 10px 0;border:0;"><span style="display:inline-block;width:22px;height:22px;line-height:22px;border-radius:50%;background:{A};color:#fff;font-size:12px;font-weight:bold;text-align:center;">{i}</span></td><td style="vertical-align:top;padding:0 0 10px;border:0;font-size:15px;line-height:1.8;{ft}">{(CUR.__setitem__(0,l),inline(l,cfg))[1]}</td></tr>' for i,l in enumerate(lines,1))
    t=f'<p style="margin:0 0 10px;font-size:14px;font-weight:bold;color:#111;">{html.escape(title)}</p>' if title else ""
    return f'<section style="margin:6px 0 22px;padding:14px 14px 4px;background:{BG};border-radius:8px;border-top:3px solid {A};{fb}">{t}<table style="width:100%;border-collapse:collapse;margin:0;"><tbody>{rows}</tbody></table></section>'
def compare_card(L,R,cfg):
    col=lambda d,dark:(f'<td style="width:48%;vertical-align:top;padding:12px;border:0;border-radius:8px;{"background-color:"+A+";color:#fff;" if dark else "background-color:"+BG+";color:#333;"}">'
        f'<p style="margin:0 0 6px;font-size:15px;font-weight:bold;">{html.escape(d["title"])}</p>'
        +"".join(f'<p style="margin:0 0 6px;font-size:13px;line-height:1.65;">{inline(x,cfg)}</p>' for x in d["items"])+'</td>')
    return (f'<section style="margin:6px 0 22px;"><table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>{col(L,False)}'
      f'<td style="width:4%;padding:0;border:0;"></td>{col(R,True)}</tr></tbody></table></section>')
# ---------- 代码窗（2026-10-15，四套共用的行渲染；外观各套自己定） ----------
CMD_RE=re.compile(r"^\s*(?:\$ |> |npx |npm |pnpm |yarn |pip3? |python3? |node |git |curl |wget |brew |apt(?:-get)? |sudo |cd |mkdir |docker |cargo |go |uv |export )")
def is_code_line(x):
    """命令/代码行：以常见命令开头，或整行没有汉字（说明文字有汉字，正常折行）"""
    return bool(x.strip()) and (bool(CMD_RE.match(x)) or not re.search(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]",x))
def code_wrap(x):
    """命令行折行点（2026-10-15i）：只在空格和逗号后面。每段（空格/逗号之间）包 white-space:nowrap 的 span，
    这样浏览器不会在 - / . 这类符号后面自己断开；逗号后面插 <wbr> 允许在这里折；空格原样保留（pre-wrap 下就是折行点）"""
    out=[]
    for tok in re.split(r"(\s+)",x):
        if not tok or tok.isspace():out.append(html.escape(tok));continue
        out.append("<wbr>".join(f'<span style="white-space:nowrap;">{html.escape(p)}</span>' for p in re.findall(r"[^,]+,?|,",tok)))
    return "".join(out)
def code_lines(lines,cmd_st,txt_st,step_st=None,gap="6px"):
    """代码窗正文：命令行一行一个 <p>，white-space:pre-wrap，在空格（或逗号后）折行，绝不在单词中间断开（2026-10-15i 起，不再用 overflow-x 横向滑动），文字包 <code>，
    阅读端（微信、浏览器）对 code 默认用等宽字体，不用写 font-family；说明文字（含汉字）正常折行；「一、」「1.」开头的说明当步骤标题。
    行样式记进 CHK["code_styles"]，publish 的 [codebreak] 按这些样式在 390px 下逐字检查"""
    # 2026-10-15i：命令行改 white-space:pre-wrap，在空格处自动折行，不再依赖 overflow-x（微信可能剔除 overflow-x，撑宽版面）；
    # word-break:normal + overflow-wrap:normal：只在空格（或逗号后）折行，绝不在单词中间断开；单个词比可见区还宽时 [codebreak] 报警
    out=[];pre="white-space:pre-wrap;word-break:normal;overflow-wrap:normal;"
    for x in lines:
        if not x.strip():out.append(f'<p style="margin:0;height:{gap};line-height:{gap};font-size:1px;"><br></p>');continue
        if is_code_line(x):
            st=cmd_st+pre;CHK["code_styles"].append(st)
            out.append(f'<p style="{st}"><code style="font-size:inherit;color:inherit;letter-spacing:0px;">{code_wrap(x)}</code></p>')
        else:
            st=(step_st if step_st and re.match(r"^\s*(?:[一二三四五六七八九十]+、|\d+[.、])",x) else txt_st)+"word-break:normal;overflow-wrap:break-word;"
            CHK["code_styles"].append(st);out.append(f'<p style="{st}">{html.escape(x)}</p>')
    return "".join(out)
def code_label(lines):
    return "bash" if any(CMD_RE.match(x) for x in lines) else "code"
TERM_DOTS="".join(f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:{c};margin-right:6px;vertical-align:middle;"></span>' for c in("#FF5F57","#FEBC2E","#28C840"))
def code_card(lines,cap=""):
    """代码窗（2026-10-15h 起四套统一，照搬 02-window-terminal）：窗口外框 + 深色终端。
    标题栏 #1E293B：左边三色圆点 + 灰色 bash/code，不放「复制」按钮/标签，也不放「· 左右滑动」提示（微信里点了没反应）；
    终端底 #0F172A：命令亮蓝 #7DD3FC 13px 一行一条，white-space:pre-wrap 在空格处折行（2026-10-15i 起不用 overflow-x），包 <code> 走等宽，不在单词中间断开；
    中文说明灰色 #94A3B8 正常折行，「一、」步骤浅色 #F1F5F9 加粗。图注用本套 S["cap"]。不用 break-all"""
    cap=clean_cap(cap)
    c=f'<p style="{S["cap"]}">{html.escape(cap)}</p>' if cap and SHOW_CAP[0] else ""
    lab=f'<span style="display:inline-block;margin-left:4px;font-size:12px;color:#94A3B8;vertical-align:middle;letter-spacing:1px;">{code_label(lines)}</span>'
    bar=f'<p style="margin:0;padding:9px 12px;line-height:1;background-color:#1E293B;border-bottom:1px solid #1E293B;white-space:nowrap;">{TERM_DOTS}{lab}</p>'
    body=code_lines(lines,"margin:0;font-size:13px;line-height:1.75;color:#7DD3FC;","margin:0;font-size:13px;line-height:1.7;color:#94A3B8;","margin:0;font-size:13px;line-height:1.7;color:#F1F5F9;font-weight:bold;")
    return (f'<section style="margin:8px 0 22px;"><section style="border:1px solid #1E293B;border-radius:10px;overflow:hidden;background-color:#0F172A;">{bar}'
      f'<section style="padding:12px 14px;">{body}</section></section>{c}</section>')
def sub_heading(text,cfg):
    """章节内小标题（### 标题，或单独一行的 **标题**）：16px 加粗 + 左侧 4×16 珊瑚竖条；比章节头（44px 大序号 + 18px）低一级，比正文高一级"""
    _,ft=fit(cfg,"h:"+re.sub(r"\s","",text)[:12])
    return (f'<section style="margin:26px 0 12px;"><p style="{S["sub"]}{ft}"><span style="display:inline-block;width:4px;height:16px;background-color:{A};border-radius:2px;margin-right:8px;vertical-align:-2px;"></span>{inline(text,cfg)}</p></section>')
def meta_line(sep=" · "):
    """开头区元信息：日期（layout-map 的 date，可不写）+ 阅读时长（按字数自动算）"""
    a=[x for x in (META.get("date"),f'阅读约 {META["mins"]} 分钟' if META.get("mins") else "") if x]
    return sep.join(a)
def meta_bits():
    """开头区元信息（都可以省略）：日期用 layout-map 的 date（没有就不显示），阅读时长按字数自动算，章节数自动数"""
    return [x for x in (META.get("date",""),f'阅读约 {META["mins"]} 分钟' if META.get("mins") else "",f'共 {META["chapters"]} 节' if META.get("chapters") else "") if x]
def opening(lead,cfg):
    """01 开头区（2026-10-15 二改：成品不放标题和副标题）。参考 gzh-design-skill references/theme-moyu-green.md 组件 2 封面 cover-breaking
    的「顶部标签 + 信息条」和 references/theme-red-white.md 组件 2 开头引言卡的大引号。
    01 的卡片语言：1.5px 黑边、不对称圆角、珊瑚浅色硬阴影；上面是珊瑚实底标签 + 日期/阅读时长/节数，下面是珊瑚大引号 + 16px 加粗导语。不用 flex/渐变。"""
    fb,ft=fit(cfg,"lead")
    tag=html.escape(META.get("tag","<栏目名>")); ml=html.escape(" · ".join(meta_bits()))
    head=(f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
      f'<td style="padding:0;border:0;vertical-align:middle;white-space:nowrap;"><span style="display:inline-block;padding:3px 10px;border-radius:4px 10px 4px 10px;background-color:{A};font-size:12px;line-height:1.4;font-weight:bold;color:#fff;letter-spacing:2px;">{tag}</span></td>'
      f'<td style="padding:0 0 0 8px;border:0;vertical-align:middle;text-align:right;font-size:11px;line-height:1.5;color:{G};">{ml}</td></tr></tbody></table>')
    ld=""
    if lead:
        body="".join(f'<p style="margin:0;{ft}">{(CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in lead)
        ld=(f'<section style="padding:6px 0 0;{fb}">'
          f'<p style="margin:0;font-size:40px;line-height:1;height:26px;overflow:visible;color:{A};font-weight:bold;">“</p>'
          f'<section style="font-size:16px;line-height:1.8;color:#222;font-weight:bold;">{body}</section></section>')
    foot=(f'<p style="margin:12px 0 0;line-height:1;"><span style="display:inline-block;width:36px;border-bottom:3px solid {A};"></span>'
      f'<span style="display:inline-block;width:10px;border-bottom:3px solid #F9B4AA;margin-left:4px;"></span>'
      f'<span style="margin-left:10px;font-size:11px;letter-spacing:2px;color:{A};font-weight:bold;vertical-align:middle;">导语 · LEAD</span></p>')
    return (f'<section style="margin:14px 4px 26px 0;padding:16px 18px 16px;border:1.5px solid #222;border-radius:12px 4px 14px 4px;box-shadow:5px 5px 0 {AL};background-color:#fff;">'
      f'{head}<section style="margin:14px 0 0;padding:10px 0 0;border-top:1.5px dashed #222;">{ld}{foot}</section></section>')
URL_BREAK=re.compile(r"([/.\-?&=])")
def url_html(u):
    """长链接只在 / . - ? & = 后面断行：在这些符号后面插 <wbr>（vass、gzh 均通过）；不用 word-break:break-all。
    // 这类连续符号中间不插；单段太长时由单元格的 overflow-wrap:break-word 兜底。"""
    parts=URL_BREAK.split(u); out=""
    for i,x in enumerate(parts):
        out+=html.escape(x)
        if i%2==1 and i+1<len(parts) and parts[i+1] and not URL_BREAK.fullmatch(parts[i+1][:1]):out+="<wbr>"
    return out
def ref_block(title,rows,cfg):
    """文末引用表：只有「编号 | 链接」两列；编号列 white-space:nowrap + 固定最小宽度；链接是纯文字（公众号外链不可点），只在 / . - ? & = 后面断行"""
    h=chapter(title,cfg) if title else ""
    tr="".join(f'<tr><td style="{S["ref_num"]}">{html.escape(n)}</td><td style="{S["ref_url"]}">{url_html(u)}</td></tr>' for n,u in rows)
    t=(f'<table style="{S["ref_table"]}"><thead><tr><th style="{S["ref_th"]}width:44px;min-width:44px;white-space:nowrap;">编号</th><th style="{S["ref_th"]}">链接</th></tr></thead>'
      f'<tbody>{tr}</tbody></table>')
    return h+(f'<section style="{S["ref_wrap"]}">{t}</section>' if S.get("ref_wrap") else t)  # 母版可用 ref_wrap 给表格加外框
def signature(cfg):
    """文末签名卡（所有母版共用，theme 不准覆盖）。头像可选：signature.avatar 指向输出目录下用户自己的头像图；缺省或文件不存在时不放头像。
    name/main/sub 缺省为占位符，请在 layout-map.json 的 signature 里填写。"""
    sig=cfg.get("signature",{}) if isinstance(cfg.get("signature"),dict) else {}
    av=sig.get("avatar")
    if av and not os.path.exists(os.path.join(BASE[0],av)): av=None
    dw=' data-w="64"'  # data-w 与显示宽度一致（微信可能把 data-w 当宽度）
    name=html.escape(sig.get("name","<你的名字>")); main=html.escape(sig.get("main","<一句话 slogan>")); sub=html.escape(sig.get("sub","<关注引导语>"))
    avtd=(f'<td width="74" style="width:74px;vertical-align:middle;padding:0 10px 0 0;border:0;"><span leaf=""><img src="{av}"{dw} width="64" style="display:block;width:64px;max-width:64px;height:auto;margin:0 auto;" alt=""></span></td>' if av else "")
    return (f'<section style="margin:36px 0 12px;padding:14px 12px;border:1.5px dashed #cfcfcf;border-radius:14px;background-color:#fff;box-sizing:border-box;">'
      f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
      f'{avtd}'
      f'<td style="vertical-align:middle;padding:0;border:0;">'
      f'<p style="margin:0;font-size:20px;line-height:1.4;font-weight:bold;color:#111;">{name}<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background-color:{A};margin-left:8px;vertical-align:top;margin-top:4px;"></span></p>'
      f'<p style="margin:6px 0 0;font-size:16px;line-height:1.6;font-weight:bold;color:#111;"><span style="border-bottom:3px solid {A};padding-bottom:1px;">{main}</span></p>'
      f'<p style="margin:8px 0 0;font-size:13px;line-height:1.6;color:{G};">{sub}</p>'
      f'</td></tr></tbody></table></section>')
# ---------- 主流程 ----------
def _cc(lines,cap=""):
    """调用本套 code_card，并把成品 HTML 记进 CHK["code_html"]，publish 的 [codecopy] 检查里面不能有「复制」"""
    h=code_card(lines,cap); CHK["code_html"].append(h); return h
REF_HEAD=re.compile(r"^#{1,3}\s*(引用|参考|来源|出处|资料)")
def build(md,cfg):
    for k in CHK:CHK[k]=[]
    SHOW_CAP[0]=bool(cfg.get("show_captions",True))
    out=[];lines=[l.rstrip() for l in md.splitlines()];i=0
    after=cfg.get("insert_after",{});shots=cfg.get("shots",{})
    qc=cfg.get("quote_card",[]);lead=cfg.get("lead",0);pc=cfg.get("points_card",{});cc=cfg.get("compare_after",{})
    first_hr=True;paras_seen=0
    # 排版层挪引用序号（layout-map 的 cite_move：[{"cite":"[7]","after":"原句片段"}]）：去掉第一处，插到 after 片段后面（句末标点之前）
    for mv in cfg.get("cite_move",[]):
        c,a=mv["cite"],mv["after"]; txt="\n".join(lines)
        if txt.count(c)<1 or a not in txt:CHK["cite_move"].append(f"✗ {c} → {a[:16]}…：找不到");continue
        txt=txt.replace(c,"",1).replace(a,a+c,1); lines=txt.split("\n"); CHK["cite_move"].append(f"{c} → 「…{a[-14:]}」后")
    body_md="\n".join(x for x in lines if not x.startswith(("|","【","副标题：")))
    n=len(re.findall(r"[\u4e00-\u9fff]",body_md))+len(re.findall(r"[A-Za-z0-9]+",body_md))  # 阅读时长：汉字 + 英文/数字串，按 450 字/分钟
    META.clear(); META.update(tag=cfg.get("tag","<栏目名>"),date=cfg.get("date",""),mins=max(1,round(n/450)),
      chapters=len([x for x in lines if re.match(r"^## [一二三四五六七八九十]+、",x)]))
    pend=None  # 标题、副标题、导语攒齐后一起交给 opening() 出开头区
    def flush():
        nonlocal pend
        if pend is not None:
            out.append(opening(pend["l"],cfg))
            if cfg.get("hero"):out.append(figure(cfg["hero"],cfg.get("hero_cap","")))
            pend=None
    ref_title=""
    used_src=set()  # 同一张图只插一次（稿件标记和 layout-map 的 gif_grid/insert_after 撞了只留第一份）
    draft_src={("img/"+x.split("/")[-1]) for x in re.findall(r"【(?:截图|GIF|动图)：((?:shots|gifs)/[^，】]+)",md)}
    draft_src|={shots[k].get("src") for k in shots if k in md}
    while i<len(lines):
        l=lines[i];i+=1;CUR[0]=l.lstrip("> ")
        if not l.strip():continue
        if pend is not None and not (l.startswith("副标题：") or (lead and l=="---" and first_hr)):flush()
        if any(l.startswith(s) for s in cfg.get("skip_prefix",[])):
            while i<len(lines) and lines[i].startswith(">"):i+=1
            continue
        if any(l.startswith(s) for s in cfg.get("skip_line",[])):continue
        m=re.match(r"【(?:截图|GIF|动图)：(\d)\s*[×xX]\s*(\d)\s*组合[^】]*】$",l)
        if not m and re.match(r"【(?:截图|GIF|动图)：并排[^】]*】$",l):
            # 并排标记（2026-10-15l）：【GIF：并排放两张】= 后面紧跟的 N 个图片标记排成 1×N（一行 N 列，列数 = 张数）
            n=0
            while i+n<len(lines) and re.match(r"【(?:截图|GIF|动图)：(?:shots|gifs)/",lines[i+n]):n+=1
            m=re.match(r"(\d)\D(\d)",f"1x{max(n,1)}")
        if m:
            # 宫格标记（2026-10-15）：【GIF：2×2 组合，…】后面紧跟的图片标记排成宫格，图注用 shots 字段（只写名称）
            items=[]
            while i<len(lines):
                mm=re.match(r"【(?:截图|GIF|动图)：((?:shots|gifs)/[^，】]+)，?(.*)】$",lines[i])
                if not mm:break
                i+=1;info=shots.get(mm[1],{});src=info.get("src","img/"+mm[1].split("/")[-1])
                if src in used_src:CHK["dup"].append(src);continue
                used_src.add(src);items.append([src,info.get("cap","")])
            if items:out.append(grid(items,int(m[2]),6));CHK["grid"].append(len(items))
            continue
        m=re.match(r"【(?:截图|GIF|动图)：((?:shots|gifs)/[^，】]+)，?(.*)】$",l)
        if m:
            info=shots.get(m[1],{});src=info.get("src","img/"+m[1].split("/")[-1])
            if src in used_src:CHK["dup"].append(src);continue
            used_src.add(src);out.append(figure(src,info.get("cap",""),True));continue
        m=re.match(r"【代码(?:卡片|块|窗)：([^，】]+)，?(.*)】$",l)  # 【代码块：说明】标记只用来定位，不进成品
        if m or l.startswith("```"):
            cap=cfg.get("code_cards",{}).get(m[1].strip(),"") if m else ""
            if m:
                while i<len(lines) and not lines[i].strip():i+=1
                if i<len(lines) and lines[i].startswith("```"):i+=1
                else: continue
            body=[]
            while i<len(lines) and not lines[i].startswith("```"):body.append(lines[i]);i+=1
            i+=1; out.append(_cc(body,cap)); continue
        if l.startswith("# "):
            # 固定规则（2026-10-15）：成品不放标题（用户在公众号编辑器里填）；副标题不进正文，publish 单独写 summary.txt
            CHK["title"]=l[2:].strip(); pend={"l":[]};continue
        if l.startswith("副标题："):
            CHK["subtitle"]=l[4:].strip(); continue
        if lead and l=="---" and first_hr:
            first_hr=False;buf=[]
            while i<len(lines) and len(buf)<lead:
                if lines[i].strip():buf.append(lines[i].strip())
                i+=1
            if pend is not None:pend["l"]=buf;flush()
            else:out.append(lead_card(buf,cfg))
            continue
        if REF_HEAD.match(l):ref_title=l.lstrip("# ").strip();continue
        if l.startswith("### "):out.append(sub_heading(l[4:].strip(),cfg));continue
        if re.fullmatch(r"\*\*[^*]{1,24}\*\*",l.strip()):out.append(sub_heading(l.strip()[2:-2],cfg));continue  # 单独一行的 **加粗** 也是小标题
        if l.startswith("## "):out.append(chapter(l[3:],cfg))
        elif l=="---":out.append(divider())
        elif l.startswith(">"):
            q=[l.lstrip("> ")]
            while i<len(lines) and lines[i].startswith(">"):q.append(lines[i].lstrip("> "));i+=1
            out.append(f'<blockquote style="{S["quote"]}">'+"<br>".join((CUR.__setitem__(0,x),inline(x,cfg))[1] for x in q)+'</blockquote>')
        elif l.startswith("|"):
            rows=[l]
            while i<len(lines) and lines[i].startswith("|"):rows.append(lines[i]);i+=1
            cells=[[c.strip() for c in r.strip("|").split("|")] for r in rows if not re.match(r"^\|[-| :]+\|$",r)]
            if any(k in rows[0] for k in cfg.get("skip_table",[])):continue
            if ref_title or re.search(r"编号|链接|来源|出处",rows[0]) or any(re.match(r"^\[?M?\d+\]?$",r[0]) and re.search(r"https?://","".join(r)) for r in cells[1:]):
                # 引用表：编号 | 链接 两列（2026-10-15 起输出，取代句尾链接）
                body=cells[1:] if re.search(r"编号|链接",rows[0]) else cells
                if len(cells[0])!=2:CHK["ref_bad"].append(f"列数 {len(cells[0])}（只能是 编号 | 链接 两列）：{rows[0][:40]}")
                refs=[]
                for r in body:
                    num=r[0].strip(); url=(r[1] if len(r)>1 else "").strip()
                    mm=re.match(r"^\[?([A-Za-z]{0,2}\d+)\]?$",num)
                    if not mm or not re.match(r"^https?://\S+$",url):CHK["ref_bad"].append(f"格式不对：{'|'.join(r)[:60]}");continue
                    refs.append((f"[{mm[1]}]",url))
                CHK["refs"]+=refs; CHK["ref_table"].append(ref_title or "（无标题）")
                out.append(ref_block(ref_title,refs,cfg)); ref_title=""; continue
            h="".join(f'<th style="{S["th"]}'+('white-space:nowrap;width:1%;' if c.strip()=='编号' else '')+f'">{inline(c,cfg)}</th>' for c in cells[0])
            b="".join("<tr>"+"".join(f'<td style="{S["td"]}'+('white-space:nowrap;width:1%;' if j==0 and re.match(r'^M\d+$',c.strip()) else '')+f'">{inline(c,cfg)}</td>' for j,c in enumerate(r))+"</tr>" for r in cells[1:])
            out.append(f'<table style="{S["table"]}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>')
        elif any(l.startswith(k) for k in pc):
            k=next(k for k in pc if l.startswith(k));buf=[l]
            while i<len(lines) and len(buf)<pc[k]["n"]:
                if lines[i].strip():buf.append(lines[i].strip())
                i+=1
            out.append(points_card(buf,cfg,pc[k].get("title","")))
        elif any(l.startswith(k) for k in qc):out.append(quote_card(l,cfg))
        elif CMD_RE.match(l) and not re.search(r"[\u4e00-\u9fff]",l):out.append(_cc([l]))  # 单独成段的命令自动排成代码窗
        else:out.append(f'<p style="{S["p"]}">{inline(l,cfg,True)}</p>')
        for k,v in after.items():
            # 值：[src, 图注] 或 [src, 图注, {"width": 208}]（2026-10-15k：可选第三项，竖图缩宽）
            src,cap=v[0],v[1]; opt=v[2] if len(v)>2 and isinstance(v[2],dict) else {}
            if l.startswith(k):
                CHK["hit"].append(("insert_after",k))
                # 稿件里已有这张图的标记时以稿件为准（2026-10-15l），map 的 insert_after 让位，避免单张先占位、宫格少一张
                if src in used_src or src in draft_src:CHK["dup"].append(src)
                else:used_src.add(src);out.append(figure(src,cap,False,opt.get("width")))
        for k,v in cc.items():
            if l.startswith(k):out.append(compare_card(v["left"],v["right"],cfg))
        for k,v in cfg.get("gif_grid",{}).items():
            if l.startswith(k):
                its=[x for x in v["items"] if x[0] not in draft_src and x[0] not in used_src]
                CHK["dup"]+=[x[0] for x in v["items"] if x not in its]
                if its:used_src.update(x[0] for x in its);out.append(grid(its,v.get("cols",2),v.get("gap",6)));CHK["grid"].append(len(its))
    flush()
    if cfg.get("signature") is not False:out.append(signature(cfg))
    # 匹配不上的 highlight / marker / data 记进 CHK["miss"]，publish 打印报警（成品不受影响）
    for k in ("highlight","marker"):
        CHK["miss"]+=[(k,x) for x in cfg.get(k,[]) if (k,x) not in CHK["hit"]]
    # insert_after 的锚点（段落/标题开头）在稿里找不到时，那张图会悄悄不出现（2026-10-15j：第二章改标题差点丢 fig1），一起报 [miss]
    CHK["miss"]+=[("insert_after",f"{k} → {v[0]}") for k,v in after.items() if ("insert_after",k) not in CHK["hit"]]
    CHK["miss"]+=[("data",f"{a} → {b}") for j,(a,b) in enumerate(cfg.get("data",[])) if ("data",j) not in CHK["hit"]]
    return leafify(f'<section style="{S["wrap"]}">'+"\n".join(out)+'<p style="margin:0;height:20px;"><br></p></section>')
def leafify(h):
    """gzh-design-skill：所有文字节点用 <span leaf=""> 包裹（图片已单独包 leaf，里面没有文字）"""
    parts=re.split(r"(<[^>]+>)",h)
    return "".join(p if p.startswith("<") or not p.strip() else f'<span leaf="">{p}</span>' for p in parts)
def doc(frag,title="article"):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title></head><body style="margin:0;background:#fff;">{frag}</body></html>'
if __name__=="__main__":
    a=[x for x in sys.argv[1:] if x!="x"]
    cfg=json.load(open(a[2],encoding="utf-8")) if len(a)>2 else {}
    import os; BASE[0]=os.path.dirname(os.path.abspath(a[1]))
    open(a[1],"w",encoding="utf-8").write(doc(build(open(a[0],encoding="utf-8").read(),cfg)))
