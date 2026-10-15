#!/usr/bin/env python3
"""本母版一条命令出全套。用法同 master/publish.py：
python3 <本目录>/publish.py <输出目录> <稿件.md> [素材目录] [--no-sync]
做法：载入 master/build.py，套上本目录 theme.py（样式和组件），再执行 master/publish.py 的流程。
每次运行先由 master/orphan.js 生成本目录的 orphan.js，把 PROFILE 设成 theme.PROFILE（本母版的识别样式），所以 master 的检查改了会自动同步。
文末签名卡沿用 01（不覆盖 build.signature）。master 和 01 的文件都不改。"""
import sys,os,json
here=os.path.dirname(os.path.abspath(__file__)); master=os.path.abspath(os.path.join(here,"..","..","master"))
sys.path.insert(0,master); sys.path.insert(0,here)
import build, theme; theme.apply(build)
o=open(os.path.join(master,"orphan.js"),encoding="utf-8").read()
assert "const PROFILE=null;" in o
open(os.path.join(here,"orphan.js"),"w",encoding="utf-8").write(o.replace("const PROFILE=null;","const PROFILE="+json.dumps(theme.PROFILE,ensure_ascii=False)+";",1))
src=open(os.path.join(master,"publish.py"),encoding="utf-8").read()
sys.argv[0]=os.path.abspath(__file__)
exec(compile(src,os.path.join(here,"publish.py"),"exec"),{"__name__":"__main__","__file__":os.path.abspath(__file__)})
