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
"""04-timeline-ticket：参考 gzh-design-skill
- references/theme-moyu-ticket.md（票据/门票隐喻、硬阴影卡片、撕票虚线）
- archive/themes-v1/theme-data-infographic.md（数据信息图，gallery-v1/datainfo.html：数据胶囊、圆形节点）
自己的设计：票根开头区（全程路线）、时间线站点式章节、竖线时间轴要点、SMIL 跳动三点分隔；素材截图直接放（不加相框）。"""
A="#0D9488"; Y="#F59E0B"; H="#1F2937"; T="#374151"; G="#9CA3AF"; LT="#CCFBF1"
C=dict(A=A,H=H,T=T,G=G,S={
 "h1":f"font-size:22px;line-height:1.45;font-weight:bold;color:{H};margin:24px 0 8px;",
 "subtitle":f"font-size:14px;color:#6B7280;margin:0 0 20px;",
 "data":f"background-color:{A};color:#fff;font-weight:bold;font-size:15px;padding:1px 6px;border-radius:4px;margin:0 1px;white-space:nowrap;",
 "quote":f"margin:0 0 20px;padding:12px 14px;background:#F0FDFA;border-radius:8px;color:#475569;font-size:14px;line-height:1.75;",
 "img":"display:block;max-width:100%;height:auto;margin:0 auto;border-radius:6px;",
 "shot":"display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid #E5E7EB;border-radius:6px;box-sizing:border-box;",  # 素材截图直接放，不加拍立得框
 "cite":f"font-size:11px;line-height:1;color:{A};vertical-align:super;padding:0 1px;white-space:nowrap;font-weight:bold;",
 "ref_wrap":"margin:0 5px 24px 0;border:2px solid #1F2937;border-radius:8px;overflow:hidden;box-shadow:4px 4px 0 #CCFBF1;",
 "ref_table":"width:100%;table-layout:auto;border-collapse:collapse;font-size:12px;line-height:1.6;margin:0;",
 "ref_th":f"background:{LT};border:0;border-bottom:2px dashed #99F6E4;padding:7px 10px;text-align:left;font-weight:bold;color:{H};letter-spacing:1px;",
 "ref_num":f"width:44px;min-width:44px;white-space:nowrap;padding:7px 10px;border:0;border-bottom:1px dashed #CCFBF1;vertical-align:top;color:{A};font-weight:bold;",
 "ref_url":"padding:7px 10px 7px 0;border:0;border-bottom:1px dashed #CCFBF1;vertical-align:top;color:#6B7280;word-break:normal;overflow-wrap:break-word;",
 "th":f"background:{LT};border:1px solid #99F6E4;padding:6px;text-align:left;font-weight:bold;color:{H};",
 "td":"border:1px solid #CCFBF1;padding:6px;vertical-align:top;word-break:break-all;"})
ST={"quote":f"margin:0;font-size:17px;line-height:1.75;font-weight:bold;color:{H};",
 "lead":"font-size:16px;line-height:1.8;color:#1F2937;font-weight:bold;",
 "head":f"margin:0;font-size:19px;line-height:1.45;font-weight:bold;color:{H};",
 "head2":f"margin:0;font-size:17px;line-height:1.5;font-weight:bold;color:{H};padding:2px 0 2px 12px;border-left:4px solid {Y};",
 "cap":f"margin:8px 0 0;font-size:12px;line-height:1.6;color:#6B7280;text-align:center;",
 "hl":f"background-color:{LT};color:#134E4A;padding:1px 2px;",
 "marker":f"border-bottom:3px solid #FCD34D;font-weight:bold;color:{H};"}
ST["sub"]=f"margin:0;font-size:16px;line-height:1.6;font-weight:bold;color:{H};"  # 章节内小标题（### 或整行 **加粗**，2026-10-15）
PROFILE=_prof(ST)
def apply(b):
    _base(b,C,ST); inline=b.inline; fit=b.fit; S=b.S
    def opening(lead,cfg):
        """开头区（2026-10-15 二改：不放标题/副标题）：大票根。参考 references/theme-moyu-ticket.md 组件 2 票据封面 ticket-cover（彩色头条 + 正票 + ✂ 撕口 + 票根），flex 全换成 table。
        头条「STOP 00 · 出发」+ 右侧 NO.月日（没有日期就写 ADMIT ONE）→ 正票：「导语」标签 + 16px 加粗导语 → ✂ 撕口 → 票根：全程路线（每个编号章节一站，自动数）+ 全程 N 站 · 日期 · 阅读约 N 分钟。"""
        fb,ft=fit(cfg,"lead"); N=b.META.get("chapters",0)
        d=b.META.get("date",""); no=("NO."+d.replace(".","").replace("-","")[-4:]) if d else "ADMIT ONE"
        head=(f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="padding:9px 16px;border:0;background-color:{A};font-size:11px;line-height:1.4;font-weight:bold;color:#fff;letter-spacing:3px;white-space:nowrap;">STOP 00 · 出发</td>'
          f'<td style="padding:9px 16px;border:0;background-color:{A};text-align:right;font-size:11px;line-height:1.4;color:#CCFBF1;letter-spacing:2px;white-space:nowrap;">{html.escape(no)}</td></tr></tbody></table>')
        ld=""
        if lead:
            body="".join(f'<p style="margin:0;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in lead)
            ld=(f'<section style="padding:14px 16px 14px;{fb}">'
              f'<p style="margin:0 0 8px;font-size:11px;line-height:1.2;font-weight:bold;color:{Y};letter-spacing:3px;">{html.escape(b.META.get("tag","<栏目名>"))} · 导语</p>'
              f'<section style="{ST["lead"]}">{body}</section></section>')
        tear=(f'<table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="padding:0 0 0 8px;border:0;vertical-align:middle;"><section style="margin:0;height:0;line-height:0;font-size:0;overflow:hidden;border-top:2px dashed #CBD5E1;"><br></section></td>'
          f'<td style="width:1%;padding:0 6px;border:0;vertical-align:middle;font-size:12px;line-height:1;color:#94A3B8;white-space:nowrap;">✂</td>'
          f'<td style="padding:0 8px 0 0;border:0;vertical-align:middle;"><section style="margin:0;height:0;line-height:0;font-size:0;overflow:hidden;border-top:2px dashed #CBD5E1;"><br></section></td></tr></tbody></table>')
        dot=lambda i:f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:{A if i%2 else Y};vertical-align:middle;"></span>'
        seg='<span style="display:inline-block;width:26px;border-top:2px dashed #99F6E4;vertical-align:middle;margin:0 3px;"></span>'
        info="  ·  ".join([f"全程 {N} 站"]*(N>0)+[x for x in b.meta_bits() if not x.startswith("共 ")])
        route=(f'<p style="margin:0 0 6px;line-height:1;white-space:nowrap;">'+seg.join(dot(i) for i in range(1,N+1))+'</p>') if N else ""
        stub=f'<section style="padding:10px 16px 12px;background-color:#F0FDFA;">{route}<p style="margin:0;font-size:11px;line-height:1.5;color:#6B7280;letter-spacing:1px;">{html.escape(info)}</p></section>'
        return (f'<section style="margin:14px 5px 28px 0;border:2px solid {H};border-radius:10px;overflow:hidden;background-color:#fff;box-shadow:5px 5px 0 {A};">'
          f'{head}{ld}{tear}{stub}</section>')
    def divider():
        dots="".join(f'<circle cx="{x}" cy="12" r="5" fill="{c}"><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="1.2s" begin="{d}s" repeatCount="indefinite"></animateTransform></circle>' for x,c,d in((40,A,0),(60,Y,0.2),(80,A,0.4)))
        return _svg(f'<line x1="0" y1="12" x2="24" y2="12" stroke="#D1D5DB" stroke-width="1" stroke-dasharray="3 3"></line><line x1="96" y1="12" x2="120" y2="12" stroke="#D1D5DB" stroke-width="1" stroke-dasharray="3 3"></line>{dots}',"0 0 120 20","34%","28px 0 12px")
    def chapter(title,cfg):
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",re.sub(r"^[一二三四五六七八九十]+、","",title))[:12])
        m=re.match(r"([一二三四五六七八九十]+)、(.*)",title)
        if not m:
            return f'<section style="margin:30px 0 14px;"><p style="{ST["head2"]}{ft}">{inline(title,cfg)}</p></section>'
        n=b.CN.index(m[1][-1])+1+(9 if len(m[1])>1 else 0)
        # 时间线站点：圆形节点 + 外圈 + 站名
        return (f'<section style="margin:36px 0 18px;"><table style="width:100%;border-collapse:collapse;margin:0;"><tbody><tr>'
          f'<td style="width:1%;vertical-align:middle;padding:0 12px 0 4px;border:0;white-space:nowrap;"><span style="display:inline-block;width:34px;height:34px;line-height:34px;border-radius:50%;background-color:{A};color:#fff;font-size:15px;font-weight:bold;text-align:center;box-shadow:0 0 0 5px {LT};">{n:02d}</span></td>'
          f'<td style="vertical-align:middle;padding:0;border:0;"><p style="margin:0 0 2px;font-size:11px;line-height:1.2;font-weight:bold;color:{Y};letter-spacing:3px;white-space:nowrap;">STOP {n:02d}</p><p style="{ST["head"]}{ft}">{inline(m[2],cfg)}</p></td>'
          f'</tr></tbody></table><p style="margin:10px 0 0 21px;line-height:1;"><span style="display:inline-block;height:14px;border-left:2px dashed #99F6E4;"></span></p></section>')
    def lead_card(paras,cfg):  # 没有标题时的备用便签导语
        fb,ft=fit(cfg,"lead")
        body="".join(f'<p style="margin:0 0 8px;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in paras)
        pin='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="display:inline-block;width:16px;height:16px;vertical-align:middle;margin-right:6px;"><circle cx="12" cy="9" r="6" fill="#EF4444"></circle><line x1="12" y1="15" x2="12" y2="23" stroke="#6B7280" stroke-width="2" stroke-linecap="round"></line></svg>'
        return (f'<section style="margin:6px 0 26px;padding:12px 16px 6px;background-color:#FEF3C7;box-shadow:4px 4px 0 #FCD34D;{fb}">'
          f'<p style="margin:0 0 8px;font-size:12px;line-height:1;font-weight:bold;color:#B45309;letter-spacing:2px;">{pin}便签</p>'
          f'<section style="{ST["lead"]}">{body}</section></section>')
    def quote_card(text,cfg):
        fb,ft=fit(cfg,re.sub(r"\s","",text)[:12])
        return (f'<section style="margin:28px 4px 30px 0;border:2px solid {H};border-radius:8px;background-color:#fff;box-shadow:5px 5px 0 {A};">'
          f'<p style="margin:0;padding:8px 16px;font-size:12px;line-height:1.2;font-weight:bold;color:{A};letter-spacing:3px;border-bottom:2px dashed #CBD5E1;">ADMIT ONE · 划重点</p>'
          f'<section style="padding:14px 18px 16px;{fb}"><p style="{ST["quote"]}{ft}">{inline(text,cfg)}</p></section></section>')
    def points_card(lines,cfg,title=""):
        fb,ft=fit(cfg,re.sub(r"\s","",lines[0])[:12])
        rows="".join(f'<tr><td style="width:1%;vertical-align:top;padding:6px 12px 0 0;border:0;border-right:2px solid {LT};white-space:nowrap;"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background-color:{A if i%2 else Y};margin-right:-19px;"></span></td><td style="vertical-align:top;padding:0 0 14px 18px;border:0;font-size:15px;line-height:1.8;{ft}"><span style="display:block;font-size:11px;line-height:1.4;font-weight:bold;color:{G};letter-spacing:2px;">STEP {i:02d}</span>{(b.CUR.__setitem__(0,l),inline(l,cfg))[1]}</td></tr>' for i,l in enumerate(lines,1))
        t=f'<p style="margin:0 0 10px;font-size:14px;font-weight:bold;color:{H};">{html.escape(title)}</p>' if title else ""
        return f'<section style="margin:6px 0 22px;padding:4px 0 0 4px;{fb}">{t}<table style="width:100%;border-collapse:collapse;margin:0;"><tbody>{rows}</tbody></table></section>'
    def compare_card(L,R,cfg):
        col=lambda d,ok:(f'<td style="width:48%;vertical-align:top;padding:12px;border:2px solid {H};border-radius:8px;background-color:{"#F0FDFA" if ok else "#fff"};">'
            f'<p style="margin:0 0 6px;font-size:15px;font-weight:bold;color:{A if ok else H};">{html.escape(d["title"])}</p>'
            +"".join(f'<p style="margin:0 0 4px;font-size:13px;line-height:1.65;">{inline(x,cfg)}</p>' for x in d["items"])+'</td>')
        return (f'<section style="margin:6px 0 22px;"><table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>{col(L,False)}'
          f'<td style="width:4%;padding:0;border:0;"></td>{col(R,True)}</tr></tbody></table></section>')
    # code_card：2026-10-15h 起四套统一用 master/build.py 的终端代码窗（照搬原 02 的窗口外框 + 深色终端，去掉「复制」和「左右滑动」），本套不再覆盖
    def sub_heading(text,cfg):
        """章节内小标题：「途经点」——10px 青色空心圆环 + 16px 加粗；章节头是 34px 实心站点圆 + STOP + 19px 标题，小标题像站点之间的小站，低一级"""
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",text)[:12])
        return (f'<section style="margin:26px 0 12px;"><p style="{ST["sub"]}{ft}"><span style="display:inline-block;width:6px;height:6px;border:2px solid {A};border-radius:50%;margin-right:10px;vertical-align:2px;"></span>{inline(text,cfg)}</p></section>')
    for k,v in dict(opening=opening,divider=divider,chapter=chapter,lead_card=lead_card,quote_card=quote_card,points_card=points_card,compare_card=compare_card,sub_heading=sub_heading).items():setattr(b,k,v)
    # 段首加粗引子（**xx：**正文，2026-10-15g）：青色空心小圆环 + 青色加粗（同小标题的「途经点」圆环，缩小一号）；还是正文段落，不是小标题
    S["leadin"]=f"font-weight:bold;color:{A};"
    def leadin(inner,raw):
        nw="white-space:nowrap;" if len(re.sub(r"\s","",raw))<=b.LEADIN_MAX else ""
        return f'<span style="{S["leadin"]}{nw}"><span style="display:inline-block;width:5px;height:5px;border:2px solid {A};border-radius:50%;margin-right:7px;vertical-align:2px;"></span>{inner}</span>'
    b.leadin=leadin
