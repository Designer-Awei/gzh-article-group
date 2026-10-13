#!/usr/bin/env python3
"""排版母版 v2.1（gzh-design-skill + 微信内容结构规范兼容）：python3 build.py 稿件.md out.html layout-map.json"""
import os, re, sys, json, html
A="#F26B5B"; AL="#FDE9E6"; T="#2b2b2b"; G="#888"; LN="#eee"; BG="#f7f7f7"
FONT=None  # 微信规范第3节：不设置 font-family，使用公众号默认字体栈
S={
 "wrap":f"padding:8px 22px;box-sizing:border-box;color:{T};font-size:15px;line-height:1.8;letter-spacing:0.5px;word-break:break-word;background:#fff;",
 "h1":"font-size:22px;line-height:1.45;font-weight:bold;color:#111;margin:24px 0 8px;",
 "subtitle":f"font-size:14px;color:{G};margin:0 0 18px;",
 "p":"margin:0 0 18px;text-align:left;",
 "strong":"font-weight:bold;color:#111;",
 # 重点句：强调色底纹 / 马克笔下划线（底部 40% 半透明色带）
 "hl":f"background:{AL};color:#111;padding:1px 2px;border-radius:2px;",
 "marker":f"background-color:rgba(242,107,91,0.16);border-bottom:2px solid #F26B5B;color:#111;font-weight:bold;padding:0 1px;",
 "data":f"color:{A};font-weight:bold;font-size:17px;padding:0 1px;",
 "cite":f"font-size:11px;color:{A};vertical-align:super;",
 "note":"background:#fff4d6;color:#8a5a00;padding:0 3px;font-size:14px;",
 "quote":f"margin:0 0 20px;padding:12px 14px;background:{BG};border-left:3px solid {A};color:#555;font-size:14px;line-height:1.75;",
 "img":"display:block;max-width:100%;height:auto;margin:0 auto;border-radius:4px;",
 "shot":f"display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid {LN};border-radius:4px;box-sizing:border-box;",
 "fig":"margin:8px 0 22px;",
 "cap":f"margin:6px 0 0;font-size:12px;line-height:1.6;color:{G};text-align:center;",
 "table":"width:100%;table-layout:auto;border-collapse:collapse;font-size:12px;line-height:1.6;margin:0 0 20px;",
 "th":f"background:{AL};border:1px solid {LN};padding:6px;text-align:left;font-weight:bold;color:#111;",
 "td":f"border:1px solid {LN};padding:6px;vertical-align:top;word-break:break-all;",
}
CUR=[""]
CN="一二三四五六七八九十"
def inline(t,cfg):
    t=html.escape(t,quote=False)
    t=re.sub(r"\*\*(.+?)\*\*",lambda m:f'<strong style="{S["strong"]}">{m[1]}</strong>',t)
    for s in cfg.get("highlight",[]):
        e=html.escape(s,quote=False)
        if e in t: t=t.replace(e,f'<span style="{S["hl"]}">{e}</span>',1)
    for s in cfg.get("marker",[]):
        e=html.escape(s,quote=False)
        if e in t: t=t.replace(e,f'<span style="{S["marker"]}">{e}</span>',1)
    for pre,s in cfg.get("data",[]):
        if not CUR[0].startswith(pre):continue
        e=html.escape(s,quote=False)
        t=re.sub(r"(?<![\w.>])"+re.escape(e)+r"(?![^<]*</span>)",f'<span style="{S["data"]}">{e}</span>',t,count=1)
    t=re.sub(r"(【(?:待补|待查)[^】]*】)",lambda m:f'<span style="{S["note"]}">{m[1]}</span>',t)
    t=re.sub(r"((?:\[M\d+\])+)",lambda m:f'<span style="{S["cite"]}">{m[1]}</span>',t)
    return t
# ---------- 组件 ----------
BASE=["."]
def imgw(src):
    try:
        from PIL import Image; import os
        return Image.open(os.path.join(BASE[0],src)).size[0]
    except Exception: return None
def figure(src,cap,shot=False):
    c=f'<p style="{S["cap"]}">{html.escape(cap)}</p>' if cap else ""
    w=imgw(src); dw=f' data-w="{w}"' if w else ""
    return f'<section style="{S["fig"]}"><span leaf=""><img src="{src}"{dw} style="{S["shot" if shot else "img"]}" alt=""></span>{c}</section>'
def divider():
    d=lambda c,s:f'<span style="display:inline-block;width:{s}px;height:{s}px;border-radius:50%;background:{c};margin:0 5px;vertical-align:middle;"></span>'
    return f'<section style="text-align:center;margin:30px 0 8px;line-height:1;">{d("#ddd",5)}{d(A,7)}{d("#ddd",5)}</section>'
def chapter(title,cfg):
    m=re.match(r"([一二三四五六七八九十]+)、(.*)",title)
    if not m:
        return f'<section style="margin:34px 0 16px;"><span style="font-size:18px;font-weight:bold;color:#111;border-bottom:3px solid {A};padding-bottom:3px;">{inline(title,cfg)}</span></section>'
    n=CN.index(m[1][-1])+1+(9 if len(m[1])>1 else 0)
    return (f'<section style="margin:36px 0 18px;">'
      f'<p style="margin:0;font-size:44px;line-height:1;font-weight:bold;color:{A};letter-spacing:1px;">{n:02d}<span style="font-size:22px;color:#222;font-weight:normal;margin-left:8px;vertical-align:middle;">—</span></p>'
      f'<p style="margin:8px 0 0;font-size:18px;line-height:1.5;font-weight:bold;color:#111;">{inline(m[2],cfg)}</p></section>')
def lead_card(paras,cfg):
    body="".join(f'<p style="margin:0 0 8px;">{(CUR.__setitem__(0,p),inline(p,cfg))[1]}</p>' for p in paras)
    return (f'<section style="margin:4px 0 24px;padding:16px 16px 10px;border:1.5px solid #222;border-radius:10px 4px 12px 4px;box-shadow:4px 4px 0 {AL};">'
      f'<p style="margin:0 0 8px;font-size:12px;letter-spacing:2px;color:{A};font-weight:bold;">导语 · LEAD</p>'
      f'<section style="font-size:15px;line-height:1.8;color:#333;">{body}</section></section>')
def quote_card(text,cfg):
    return (f'<section style="margin:26px 0;padding:22px 20px 18px;background:#fff;border:1.5px solid #222;border-radius:4px 14px 4px 14px;text-align:center;">'
      f'<p style="margin:0;font-size:36px;line-height:1;height:22px;overflow:visible;color:{A};">“</p>'
      f'<p style="margin:10px 0 0;font-size:17px;line-height:1.75;font-weight:bold;color:#111;">{inline(text,cfg)}</p>'
      f'<p style="margin:12px 0 0;text-align:center;line-height:1;"><span style="display:inline-block;padding:0 14px;border-bottom:3px solid {A};"></span></p></section>')
def points_card(lines,cfg,title=""):
    rows="".join(f'<tr><td style="width:1%;vertical-align:top;padding:2px 10px 10px 0;border:0;"><span style="display:inline-block;width:22px;height:22px;line-height:22px;border-radius:50%;background:{A};color:#fff;font-size:12px;font-weight:bold;text-align:center;">{i}</span></td><td style="vertical-align:top;padding:0 0 10px;border:0;font-size:15px;line-height:1.8;">{(CUR.__setitem__(0,l),inline(l,cfg))[1]}</td></tr>' for i,l in enumerate(lines,1))
    t=f'<p style="margin:0 0 10px;font-size:14px;font-weight:bold;color:#111;">{html.escape(title)}</p>' if title else ""
    return f'<section style="margin:6px 0 22px;padding:14px 14px 4px;background:{BG};border-radius:8px;border-top:3px solid {A};">{t}<table style="width:100%;border-collapse:collapse;margin:0;"><tbody>{rows}</tbody></table></section>'
def compare_card(L,R,cfg):
    col=lambda d,dark:(f'<td style="width:46%;vertical-align:top;padding:12px;border:0;border-radius:8px;{"background-color:"+A+";color:#fff;" if dark else "background-color:"+BG+";color:#333;"}">'
        f'<p style="margin:0 0 6px;font-size:15px;font-weight:bold;">{html.escape(d["title"])}</p>'
        +"".join(f'<p style="margin:0 0 6px;font-size:13px;line-height:1.65;">{inline(x,cfg)}</p>' for x in d["items"])+'</td>')
    return (f'<section style="margin:6px 0 22px;"><table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>{col(L,False)}'
      f'<td style="width:8%;vertical-align:middle;text-align:center;padding:0;border:0;font-size:13px;font-weight:bold;font-style:italic;color:#222;">vs</td>{col(R,True)}</tr></tbody></table></section>')
def signature(cfg):
    sig=cfg.get("signature",{})
    av=sig.get("avatar")  # 头像可选：来自 ip-spec.md 或用户提供；缺省或文件不存在时不放头像
    if av and not os.path.exists(os.path.join(BASE[0],av)): av=None
    w=imgw(av) if av else None; dw=f' data-w="{w}"' if w else ""
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
def build(md,cfg):
    out=[];lines=[l.rstrip() for l in md.splitlines()];i=0
    after=cfg.get("insert_after",{});shots=cfg.get("shots",{})
    qc=cfg.get("quote_card",[]);lead=cfg.get("lead",0);pc=cfg.get("points_card",{});cc=cfg.get("compare_after",{})
    first_hr=True;paras_seen=0
    while i<len(lines):
        l=lines[i];i+=1;CUR[0]=l.lstrip("> ")
        if not l.strip():continue
        if any(l.startswith(s) for s in cfg.get("skip_prefix",[])):
            while i<len(lines) and lines[i].startswith(">"):i+=1
            continue
        if any(l.startswith(s) for s in cfg.get("skip_line",[])):continue
        m=re.match(r"【截图：(shots/[\w.]+)，?(.*)】$",l)
        if m:
            info=shots.get(m[1],{});out.append(figure(info.get("src","img/"+m[1].split("/")[-1]),info.get("cap",""),True));continue
        if l.startswith("# "):
            out.append(f'<h1 style="{S["h1"]}">{inline(l[2:],cfg)}</h1>')
            if cfg.get("hero"):out.append(figure(cfg["hero"],cfg.get("hero_cap","")))
            continue
        if l.startswith("副标题："):out.append(f'<p style="{S["subtitle"]}">{inline(l[4:],cfg)}</p>');continue
        if lead and l=="---" and first_hr:
            first_hr=False;buf=[]
            while i<len(lines) and len(buf)<lead:
                if lines[i].strip():buf.append(lines[i].strip())
                i+=1
            out.append(lead_card(buf,cfg));continue
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
        else:out.append(f'<p style="{S["p"]}">{inline(l,cfg)}</p>')
        for k,(src,cap) in after.items():
            if l.startswith(k):out.append(figure(src,cap))
        for k,v in cc.items():
            if l.startswith(k):out.append(compare_card(v["left"],v["right"],cfg))
    if cfg.get("signature") is not False:out.append(signature(cfg))
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
