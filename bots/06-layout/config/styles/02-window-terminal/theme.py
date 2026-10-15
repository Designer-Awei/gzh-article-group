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
"""02-window-terminal：参考 gzh-design-skill
- archive/themes-v1/theme-terminal.md（终端风，gallery-v1/rich_terminal.html、heikeji.html）
- references/common-components.md 组件 1a 深色代码块（三色圆点标题栏）
- references/theme-moyu-green.md 的 #FDE68A 黄色高亮（审核官建议）
自己的设计：苹果窗口卡片只承载正文组件（导语/金句/要点/对比/代码），素材截图直接放；终端窗口开头区；命令行提示符式章节，SMIL 进度线分隔。"""
A="#2563EB"; H="#0F172A"; T="#334155"; G="#94A3B8"; LN="#E2E8F0"; BAR="#F1F5F9"
C=dict(A=A,H=H,T=T,G=G,S={
 "h1":f"font-size:22px;line-height:1.45;font-weight:bold;color:{H};margin:24px 0 10px;",
 "subtitle":f"font-size:14px;color:#64748B;margin:0 0 20px;padding-left:10px;border-left:3px solid {A};",
 "data":f"color:{A};font-weight:bold;font-size:17px;padding:0 1px;white-space:nowrap;",
 "quote":f"margin:0 0 20px;padding:12px 14px;background:#F8FAFC;border-left:3px solid {G};color:#475569;font-size:14px;line-height:1.75;",
 "img":"display:block;max-width:100%;height:auto;margin:0 auto;border-radius:6px;",
 "shot":f"display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid {LN};border-radius:6px;box-sizing:border-box;",  # 素材截图直接放，不套窗口
 "cite":"font-size:11px;line-height:1;color:#3B82F6;vertical-align:super;padding:0 1px;white-space:nowrap;",
 "ref_th":f"background:{BAR};border:0;border-bottom:1px solid {LN};padding:6px 8px;text-align:left;font-weight:bold;color:{H};",
 "ref_num":f"width:44px;min-width:44px;white-space:nowrap;padding:6px 8px;border:0;border-bottom:1px solid {LN};vertical-align:top;color:{A};font-weight:bold;",
 "ref_url":"padding:6px 8px;border:0;border-bottom:1px solid #E2E8F0;vertical-align:top;color:#64748B;word-break:normal;overflow-wrap:break-word;",
 "th":f"background:{BAR};border:1px solid {LN};padding:6px;text-align:left;font-weight:bold;color:{H};",
 "td":f"border:1px solid {LN};padding:6px;vertical-align:top;word-break:break-all;"})
ST={"quote":f"margin:0;font-size:17px;line-height:1.75;font-weight:bold;color:{H};",
 "lead":"font-size:16px;line-height:1.8;color:#F1F5F9;font-weight:bold;",
 "head":f"margin:0;font-size:19px;line-height:1.5;font-weight:bold;color:{H};",
 "head2":f"margin:0;font-size:17px;line-height:1.5;font-weight:bold;color:{H};",
 "cap":f"margin:8px 0 0;font-size:12px;line-height:1.6;color:{G};text-align:center;",
 "hl":"background-color:#FDE68A;color:#1F2937;padding:1px 2px;",
 "marker":f"border-bottom:2px solid {A};font-weight:bold;color:{H};"}
ST["sub"]=f"margin:0;font-size:16px;line-height:1.6;font-weight:bold;color:{H};"  # 章节内小标题（### 或整行 **加粗**，2026-10-15）
PROFILE=_prof(ST)
DOTS=''.join(f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:{c};margin-right:6px;vertical-align:middle;"></span>' for c in("#FF5F57","#FEBC2E","#28C840"))
def win(body,label="",fb="",pad="14px 16px",dark=False):
    bar_bg="#1E293B" if dark else BAR; bd="#1E293B" if dark else LN
    lab=f'<span style="display:inline-block;margin-left:4px;font-size:12px;color:{"#94A3B8" if dark else "#64748B"};vertical-align:middle;letter-spacing:1px;">{label}</span>' if label else ""
    return (f'<section style="margin:6px 0 24px;border:1px solid {bd};border-radius:10px;overflow:hidden;background-color:{"#0F172A" if dark else "#fff"};">'
      f'<p style="margin:0;padding:9px 12px;line-height:1;background-color:{bar_bg};border-bottom:1px solid {bd};">{DOTS}{lab}</p>'
      f'<section style="padding:{pad};{fb}">{body}</section></section>')  # card_fit 的 box 样式加在内容区（orphan.js 调的就是这一层）
def apply(b):
    _base(b,C,ST); inline=b.inline; fit=b.fit; S=b.S
    def opening(lead,cfg):
        """开头区（2026-10-15 二改：不放标题/副标题）：深色终端窗口。参考 archive/themes-v1/theme-terminal.md 组件 2 开头引言卡（三色圆点标题栏 + 命令提示符 + 引言）。
        标题栏 → 两枚标签（蓝底账号标签 + 描边的阅读时长/节数/日期）→ ❯ cat lead.md → 16px 浅色导语 → 底部状态栏 + SMIL 闪烁光标。
        深色底上的引用序号单独放大到 13px、换成亮青 #67E8F9。"""
        fb,ft=fit(cfg,"lead"); bits=b.meta_bits()
        tag=html.escape(b.META.get("tag","<栏目名>"))
        chip=lambda x,on:f'<span style="display:inline-block;margin:0 6px 6px 0;padding:2px 8px;border-radius:4px;font-size:11px;line-height:1.5;letter-spacing:1px;{"background-color:"+A+";color:#fff;font-weight:bold;" if on else "border:1px solid #334155;color:#94A3B8;"}">{html.escape(x)}</span>'
        chips=f'<p style="margin:0 0 8px;line-height:1;">{chip(tag,True)}'+"".join(chip(x,False) for x in bits)+'</p>'
        pr=lambda cmd:f'<p style="margin:0 0 8px;font-size:12px;line-height:1.4;color:#64748B;letter-spacing:0.5px;"><span style="color:#28C840;font-weight:bold;">❯</span><span style="margin-left:6px;color:#7DD3FC;">{cmd}</span></p>'
        ld=""
        if lead:
            cd="font-size:13px;line-height:1;color:#67E8F9;font-weight:bold;vertical-align:super;padding:0 1px;white-space:nowrap;"
            body="".join(f'<p style="margin:0;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in lead).replace(S["cite"],cd)
            ld=f'{pr("cat lead.md")}<section style="margin:0;padding:0 0 2px;{fb}"><section style="{ST["lead"]}">{body}</section></section>'
        cur=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 14" style="display:inline-block;width:7px;height:12px;vertical-align:middle;margin-left:6px;">'
             '<rect x="0" y="0" width="8" height="14" fill="#28C840"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"></animate></rect></svg>')
        return (f'<section style="margin:14px 0 26px;border:1px solid #1E293B;border-radius:12px;overflow:hidden;background-color:{H};">'
          f'<p style="margin:0;padding:10px 12px;line-height:1;background-color:#1E293B;">{DOTS}<span style="display:inline-block;margin-left:4px;font-size:12px;color:#94A3B8;vertical-align:middle;letter-spacing:1px;">~/column — zsh</span></p>'
          f'<section style="padding:16px 18px 16px;">{chips}{ld}</section>'
          f'<p style="margin:0;padding:8px 18px;font-size:11px;line-height:1.4;color:#94A3B8;background-color:#1E293B;"><span style="color:#28C840;">●</span> ready{cur}</p></section>')
    def divider():
        return _svg('<line x1="0" y1="6" x2="300" y2="6" stroke="#E2E8F0" stroke-width="2" stroke-linecap="round"></line>'
          f'<line x1="0" y1="6" x2="300" y2="6" stroke="{A}" stroke-width="2" stroke-linecap="round" stroke-dasharray="48 252"><animate attributeName="stroke-dashoffset" values="300;0" dur="3.2s" repeatCount="indefinite"></animate></line>'
          f'<circle cx="300" cy="6" r="3" fill="{A}"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"></animate></circle>',"0 0 304 12","56%")
    def chapter(title,cfg):
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",re.sub(r"^[一二三四五六七八九十]+、","",title))[:12])
        m=re.match(r"([一二三四五六七八九十]+)、(.*)",title)
        if not m:
            return f'<section style="margin:30px 0 14px;"><p style="{ST["head2"]}{ft}"><span style="color:{A};margin-right:6px;">#</span>{inline(title,cfg)}</p></section>'
        n=b.CN.index(m[1][-1])+1+(9 if len(m[1])>1 else 0)
        return (f'<section style="margin:36px 0 18px;">'
          f'<p style="margin:0 0 6px;font-size:13px;line-height:1.4;color:{G};letter-spacing:1px;"><span style="color:#28C840;font-weight:bold;">❯</span><span style="margin-left:6px;color:{A};font-weight:bold;">cd</span><span style="margin-left:6px;">part-{n:02d}</span><span style="display:inline-block;width:7px;height:13px;background-color:{A};margin-left:4px;vertical-align:middle;"></span></p>'
          f'<p style="{ST["head"]}{ft}">{inline(m[2],cfg)}</p>'
          f'<p style="margin:8px 0 0;line-height:1;"><span style="display:inline-block;width:36px;border-bottom:3px solid {H};"></span></p></section>')
    def lead_card(paras,cfg):
        fb,ft=fit(cfg,"lead")
        body="".join(f'<p style="margin:0 0 8px;{ft}">{(b.CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in paras)
        return win(f'<section style="font-size:15px;line-height:1.8;color:#334155;">{body}</section>',"导读",fb,"14px 16px 6px")  # 没有标题时的备用导语卡
    def quote_card(text,cfg):
        fb,ft=fit(cfg,re.sub(r"\s","",text)[:12])
        return win(f'<p style="{ST["quote"]}{ft}">{inline(text,cfg)}</p>',"划重点",fb,"16px 18px")
    def points_card(lines,cfg,title=""):
        fb,ft=fit(cfg,re.sub(r"\s","",lines[0])[:12])
        rows="".join(f'<tr><td style="width:1%;vertical-align:top;padding:3px 10px 12px 0;border:0;white-space:nowrap;"><span style="display:inline-block;padding:0 6px;line-height:20px;border:1px solid {A};border-radius:4px;color:{A};font-size:12px;font-weight:bold;">STEP {i}</span></td><td style="vertical-align:top;padding:0 0 12px;border:0;font-size:15px;line-height:1.8;{ft}">{(b.CUR.__setitem__(0,l),inline(l,cfg))[1]}</td></tr>' for i,l in enumerate(lines,1))
        t=f'<p style="margin:0 0 10px;font-size:14px;font-weight:bold;color:{H};">{html.escape(title)}</p>' if title else ""
        return win(f'{t}<table style="width:100%;border-collapse:collapse;margin:0;"><tbody>{rows}</tbody></table>',"",fb,"14px 14px 2px")
    def compare_card(L,R,cfg):
        col=lambda d,ok:(f'<td style="width:48%;vertical-align:top;padding:0;border:0;">'
          +win(f'<p style="margin:0 0 6px;font-size:15px;font-weight:bold;color:{A if ok else "#64748B"};">{html.escape(d["title"])}</p>'+"".join(f'<p style="margin:0 0 4px;font-size:13px;line-height:1.65;">{inline(x,cfg)}</p>' for x in d["items"]),"","","10px 12px 6px").replace("margin:6px 0 24px;","margin:0;")+'</td>')
        return (f'<section style="margin:6px 0 22px;"><table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>{col(L,False)}'
          f'<td style="width:4%;border:0;padding:0;"></td>{col(R,True)}</tr></tbody></table></section>')
    # code_card：2026-10-15h 起四套统一用 master/build.py 的终端代码窗（照搬原 02 的窗口外框 + 深色终端，去掉「复制」和「左右滑动」），本套不再覆盖
    def sub_heading(text,cfg):
        """章节内小标题：灰色「./」路径前缀 + 16px 加粗；章节头是「❯ cd part-01」+ 19px 标题 + 粗短线，小标题明显低一级"""
        _,ft=fit(cfg,"h:"+re.sub(r"\s","",text)[:12])
        return (f'<section style="margin:26px 0 12px;"><p style="{ST["sub"]}{ft}"><span style="color:{A};font-size:14px;font-weight:bold;margin-right:6px;">./</span>{inline(text,cfg)}</p></section>')
    for k,v in dict(opening=opening,divider=divider,chapter=chapter,lead_card=lead_card,quote_card=quote_card,points_card=points_card,compare_card=compare_card,sub_heading=sub_heading).items():setattr(b,k,v)
    # 段首加粗引子（**xx：**正文，2026-10-15g）：蓝色「./」前缀 + 蓝色加粗（同小标题的「./」）；还是正文段落，不是小标题
    S["leadin"]=f"font-weight:bold;color:{A};"
    def leadin(inner,raw):
        nw="white-space:nowrap;" if len(re.sub(r"\s","",raw))<=b.LEADIN_MAX else ""
        return f'<span style="{S["leadin"]}{nw}"><span style="color:{A};font-size:13px;font-weight:bold;margin-right:4px;">./</span>{inner}</span>'
    b.leadin=leadin
