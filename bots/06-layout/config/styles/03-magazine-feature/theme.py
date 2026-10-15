import re, html
def _prof(ST):
    z=lambda v:v.replace(" ","").rstrip(";")
    P={k:z(ST[k]) for k in ("quote","lead","cap","hl","marker")}
    P["head"]=[z(ST["head"]),z(ST["head2"])]+([z(ST["sub"])] if "sub" in ST else [])
    return P
def _svg(inner,vb,w="60%",m="28px 0 12px"):
    """SMIL 动效 SVG：内联、无 id/class/defs/use/href/style 动画/script；只用白名单属性（stroke-dashoffset、transform、opacity）"""
    return (f'<section style="text-align:center;line-height:0;margin:{m};">'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" style="display:inline-block;width:{w};max-width:100%;height:auto;vertical-align:top;">{inner}</svg></section>')
def _base(b,C,ST):
    S=b.S
    S.update({
     "wrap":f"padding:8px 22px;box-sizing:border-box;color:{C['T']};font-size:15px;line-height:1.8;letter-spacing:0.5px;word-break:break-word;background:#fff;",
     "p":"margin:0 0 18px;text-align:left;",
     "strong":f"font-weight:bold;color:{C['H']};",
     "hl":ST["hl"],"marker":ST["marker"],"cap":ST["cap"],
     "link":f"color:{C['A']};text-decoration:underline;",
     "linkurl":f"font-size:12px;color:{C['G']};",
    })
    S.update(C.get("S",{}))
"""03-magazine-feature：参考 gzh-design-skill
- archive/themes-v1/theme-editorial-feature.md（杂志特稿，gallery-v1/magfeature.html）
- references/theme-red-white.md（编号章节、引言卡、细线分隔的编辑风）
自己的设计：无框「编者按」导语、CHAPTER 字母栏 + 细笔画大号数字（模拟衬线标题的杂志感，不用 font-family）、无框大引号拉引语、细线数字目录式要点、SMIL 旋转菱形分隔。"""
A="#E11D48"; H="#111111"; T="#3F3F46"; G="#A1A1AA"; HAIR="#E4E4E7"
C=dict(A=A,H=H,T=T,G=G,S={
 "h1":f"font-size:25px;line-height:1.4;font-weight:bold;color:{H};margin:20px 0 10px;padding-top:14px;border-top:4px solid {H};letter-spacing:1px;",
 "subtitle":f"font-size:15px;line-height:1.7;color:#71717A;margin:0 0 22px;padding-bottom:14px;border-bottom:1px solid {HAIR};",
 "data":f"color:{A};font-weight:bold;font-size:19px;padding:0 1px;white-space:nowrap;",
 "quote":f"margin:0 0 20px;padding:2px 0 2px 14px;border-left:2px solid {H};color:#52525B;font-size:14px;line-height:1.8;",
 "img":"display:block;max-width:100%;height:auto;margin:0 auto;",
 "shot":f"display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid {HAIR};box-sizing:border-box;",
 "cite":f"font-size:11px;line-height:1;color:{A};vertical-align:super;padding:0 1px;white-space:nowrap;",
 "ref_table":"width:100%;table-layout:auto;border-collapse:collapse;font-size:12px;line-height:1.6;margin:0 0 20px;border-top:2px solid #111111;",
 "ref_th":f"background:#fff;border:0;border-bottom:1px solid {H};padding:7px 8px 7px 0;text-align:left;font-weight:bold;color:{H};letter-spacing:2px;",
 "ref_num":f"width:44px;min-width:44px;white-space:nowrap;padding:7px 8px 7px 0;border:0;border-bottom:1px solid {HAIR};vertical-align:top;color:{A};font-weight:bold;",
 "ref_url":"padding:7px 0;border:0;border-bottom:1px solid #E4E4E7;vertical-align:top;color:#71717A;word-break:normal;overflow-wrap:break-word;",
 "th":f"background:#FAFAFA;border-bottom:2px solid {H};border-top:0;border-left:0;border-right:0;padding:6px;text-align:left;font-weight:bold;color:{H};",
 "td":f"border-bottom:1px solid {HAIR};border-top:0;border-left:0;border-right:0;padding:6px;vertical-align:top;word-break:break-all;"})
ST={"quote":f"margin:0;font-size:20px;line-height:1.65;font-weight:bold;color:{H};letter-spacing:1px;",
 "lead":"font-size:20px;line-height:1.7;color:#111111;font-weight:bold;letter-spacing:1px;",
 "head":f"margin:0;font-size:21px;line-height:1.45;font-weight:bold;color:{H};letter-spacing:1px;",
 "head2":f"margin:0;font-size:17px;line-height:1.5;font-weight:bold;color:{H};letter-spacing:1px;",
 "cap":f"margin:8px 0 0;font-size:12px;line-height:1.6;color:{G};text-align:left;",
 "hl":"background-color:#FFE4E6;color:#881337;padding:1px 2px;",
 "marker":f"border-bottom:1px solid {A};font-weight:bold;color:{A};"}
ST["sub"]=f"margin:0;font-size:16px;line-height:1.6;font-weight:bold;color:{H};letter-spacing:1px;"  # 章节内小标题（### 或整行 **加粗**，2026-10-15）
PROFILE=_prof(ST)
def apply(b):
    _base(b,C,ST); inline=b.inline; fit=b.fit; S=b.S
    def opening(lead,cfg):
        """开头区（2026-10-15 二改：不放标题/副标题）：杂志刊头。参考 archive/themes-v1/theme-editorial-feature.md 组件 2/3（报头感、栏目线）
        和 references/theme-olive-journal.md 组件 4–6（刊头标签条、期号条）。
        双线刊头 + 「FEATURE · 特稿」+ 日期（可省略）→ 编者按标签 → 20px 加粗导语当作特稿的引题（standfirst）→ 署名栏：文 / <你的名字> ｜ 阅读约 N 分钟 · N CHAPTERS。"""
        fb,ft=fit(cfg,"lead"); nm=html.escape(cfg.get("signature",{}).get("name","<你的名字>") if isinstance(cfg.get("signature"),dict) else "<你的名字>")
        d=html.escape(b.META.get("date",""))
        mast=(f'<section style="margin:0;height:2px;line-height:0;font-size:0;overflow:hidden;border-top:4px solid {H};border-bottom:1px solid {H};"><br></section>'
          f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="padding:8px 0;border:0;border-bottom:1px solid {HAIR};vertical-align:middle;font-size:11px;line-height:1.4;font-weight:bold;color:{A};letter-spacing:4px;white-space:nowrap;">FEATURE · 特稿</td>'
          f'<td style="padding:8px 0;border:0;border-bottom:1px solid {HAIR};vertical-align:middle;text-align:right;font-size:11px;line-height:1.4;color:{G};letter-spacing:1px;white-space:nowrap;">{d}</td></tr></tbody></table>')
        ld=""
        if lead:
            body="".join(f'<p style="margin:0;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in lead)
            ld=(f'<section style="margin:20px 0 18px;padding:0;{fb}">'
              f'<p style="margin:0 0 12px;font-size:12px;line-height:1;font-weight:bold;color:{A};letter-spacing:4px;">编者按<span style="display:inline-block;width:40px;border-bottom:1px solid {A};margin-left:10px;vertical-align:middle;"></span></p>'
              f'<section style="{ST["lead"]}">{body}</section></section>')
        rt=" · ".join(x for x in (f'阅读约 {b.META["mins"]} 分钟' if b.META.get("mins") else "",f'{b.META["chapters"]} CHAPTERS' if b.META.get("chapters") else "") if x)
        by=(f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="padding:8px 0;border:0;border-top:1px solid {H};border-bottom:1px solid {HAIR};font-size:12px;line-height:1.4;color:{H};font-weight:bold;letter-spacing:1px;white-space:nowrap;">文 / {nm}</td>'
          f'<td style="padding:8px 0;border:0;border-top:1px solid {H};border-bottom:1px solid {HAIR};text-align:right;font-size:11px;line-height:1.4;color:{G};letter-spacing:1px;white-space:nowrap;">{html.escape(rt)}</td></tr></tbody></table>')
        return f'<section style="margin:10px 0 26px;">{mast}{ld}{by}</section>'
    def divider():
        return _svg(f'<line x1="0" y1="10" x2="128" y2="10" stroke="{H}" stroke-width="1"></line><line x1="172" y1="10" x2="300" y2="10" stroke="{H}" stroke-width="1"></line>'
          f'<rect x="144" y="4" width="12" height="12" fill="{A}" transform="rotate(45 150 10)"><animateTransform attributeName="transform" type="rotate" values="45 150 10;225 150 10;45 150 10" dur="6s" repeatCount="indefinite"></animateTransform></rect>',"0 0 300 20","62%","30px 0 14px")
    def chapter(title,cfg):
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",re.sub(r"^[一二三四五六七八九十]+、","",title))[:12])
        m=re.match(r"([一二三四五六七八九十]+)、(.*)",title)
        if not m:
            return f'<section style="margin:32px 0 14px;"><p style="margin:0 0 6px;line-height:1;"><span style="display:inline-block;width:24px;border-bottom:2px solid {A};"></span></p><p style="{ST["head2"]}{ft}">{inline(title,cfg)}</p></section>'
        n=b.CN.index(m[1][-1])+1+(9 if len(m[1])>1 else 0)
        return (f'<section style="margin:40px 0 20px;padding-top:12px;border-top:1px solid {H};">'
          f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="width:1%;vertical-align:top;padding:0 14px 0 0;border:0;white-space:nowrap;"><p style="margin:0;font-size:52px;line-height:1;font-weight:200;color:{A};white-space:nowrap;letter-spacing:-1px;">{n:02d}</p></td>'
          f'<td style="vertical-align:top;padding:2px 0 0;border:0;"><p style="margin:0 0 6px;font-size:11px;line-height:1.2;color:{G};letter-spacing:4px;white-space:nowrap;">CHAPTER {n:02d}</p><p style="{ST["head"]}{ft}">{inline(m[2],cfg)}</p></td>'
          f'</tr></tbody></table></section>')
    def lead_card(paras,cfg):  # 没有标题时的备用导语
        fb,ft=fit(cfg,"lead")
        body="".join(f'<p style="margin:0 0 10px;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in paras)
        return (f'<section style="margin:4px 0 26px;padding:0 0 6px;{fb}">'
          f'<p style="margin:0 0 10px;font-size:12px;line-height:1;font-weight:bold;color:{A};letter-spacing:4px;">编者按<span style="display:inline-block;width:40px;border-bottom:1px solid {A};margin-left:10px;vertical-align:middle;"></span></p>'
          f'<section style="{ST["lead"]}">{body}</section></section>')
    def quote_card(text,cfg):
        fb,ft=fit(cfg,re.sub(r"\s","",text)[:12])
        return (f'<section style="margin:30px 0;padding:0 8px 14px;border-bottom:1px solid {H};{fb}">'
          f'<p style="margin:0 0 6px;font-size:60px;line-height:1;font-weight:bold;color:{A};">“</p>'
          f'<p style="{ST["quote"]}{ft}">{inline(text,cfg)}</p></section>')
    def points_card(lines,cfg,title=""):
        fb,ft=fit(cfg,re.sub(r"\s","",lines[0])[:12])
        rows="".join(f'<tr><td style="width:1%;vertical-align:top;padding:10px 14px 10px 0;border:0;border-top:1px solid {HAIR};white-space:nowrap;"><span style="font-size:26px;line-height:1;font-weight:200;color:{A};">{i:02d}</span></td><td style="vertical-align:top;padding:10px 0;border:0;font-size:15px;line-height:1.8;border-top:1px solid {HAIR};{ft}">{(b.CUR.__setitem__(0,l),inline(l,cfg))[1]}</td></tr>' for i,l in enumerate(lines,1))
        t=f'<p style="margin:0 0 4px;font-size:12px;font-weight:bold;color:{H};letter-spacing:3px;">{html.escape(title)}</p>' if title else ""
        return f'<section style="margin:6px 0 24px;padding:0;border-bottom:1px solid {HAIR};{fb}">{t}<table style="width:100%;border-collapse:collapse;margin:0;"><tbody>{rows}</tbody></table></section>'
    def compare_card(L,R,cfg):
        col=lambda d,ok:(f'<td style="width:48%;vertical-align:top;padding:10px 0 4px;border:0;border-top:{"3px solid "+A if ok else "3px solid "+H};">'
            f'<p style="margin:0 0 6px;font-size:16px;font-weight:bold;color:{A if ok else H};">{html.escape(d["title"])}</p>'
            +"".join(f'<p style="margin:0 0 4px;font-size:13px;line-height:1.65;">{inline(x,cfg)}</p>' for x in d["items"])+'</td>')
        return (f'<section style="margin:6px 0 22px;"><table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>{col(L,False)}'
          f'<td style="width:4%;border:0;padding:0;"></td>{col(R,True)}</tr></tbody></table></section>')
    # code_card：2026-10-15h 起四套统一用 master/build.py 的终端代码窗（照搬原 02 的窗口外框 + 深色终端，去掉「复制」和「左右滑动」），本套不再覆盖
    def sub_heading(text,cfg):
        """章节内小标题：8px 玫红实心小方块 + 16px 加粗（字距 1px）；章节头是 52px 细体数字 + CHAPTER + 21px 标题，小标题明显低一级"""
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",text)[:12])
        return (f'<section style="margin:28px 0 12px;"><p style="{ST["sub"]}{ft}"><span style="display:inline-block;width:8px;height:8px;background-color:{A};margin-right:10px;vertical-align:2px;"></span>{inline(text,cfg)}</p></section>')
    for k,v in dict(opening=opening,divider=divider,chapter=chapter,lead_card=lead_card,quote_card=quote_card,points_card=points_card,compare_card=compare_card,sub_heading=sub_heading).items():setattr(b,k,v)
    # 段首加粗引子（**xx：**正文，2026-10-15g）：6px 玫红实心小方块 + 玫红加粗（同小标题的 8px 方块，缩小一号）；还是正文段落，不是小标题
    S["leadin"]=f"font-weight:bold;color:{A};"
    def leadin(inner,raw):
        nw="white-space:nowrap;" if len(re.sub(r"\s","",raw))<=b.LEADIN_MAX else ""
        return f'<span style="{S["leadin"]}{nw}"><span style="display:inline-block;width:6px;height:6px;background-color:{A};margin-right:7px;vertical-align:2px;"></span>{inner}</span>'
    b.leadin=leadin
