#!/usr/bin/env python3
"""从 projects/_template/ 创建 projects/<slug>/ 固定结构并初始化 handoff.json。
Create projects/<slug>/ with the fixed layout from projects/_template/.

用法 / usage: python3 scripts/new-project.py 2026-10-20-my-topic
"""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "projects" / "_template"

def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", sys.argv[1]):
        sys.exit("usage: new-project.py YYYY-MM-DD-slug  (lowercase, digits, hyphens)")
    slug = sys.argv[1]
    dst = ROOT / "projects" / slug
    if dst.exists():
        sys.exit(f"exists: projects/{slug}")
    shutil.copytree(TPL, dst)
    for f in ("handoff.json", "README.md"):
        p = dst / f
        p.write_text(p.read_text(encoding="utf-8").replace("{{slug}}", slug), encoding="utf-8")
    json.loads((dst / "handoff.json").read_text(encoding="utf-8"))
    for p in sorted(dst.rglob("*")):
        print(p.relative_to(ROOT))

if __name__ == "__main__":
    main()
