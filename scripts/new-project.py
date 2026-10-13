#!/usr/bin/env python3
"""在所有 bot 目录下创建同名项目文件夹并初始化 handoff.json。
Create the same project folder under every bot directory and initialise handoff.json.

用法 / usage: python3 scripts/new-project.py 2026-10-20-my-topic
"""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "templates" / "project"
FLOW = {"01-news": "02-ideation", "02-ideation": "00-chief-of-staff", "03-research": "04-copywriter",
        "04-copywriter": "05-visual", "05-visual": "06-layout", "06-layout": "07-reviewer",
        "07-reviewer": "00-chief-of-staff", "00-chief-of-staff": "user"}

def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", sys.argv[1]):
        sys.exit("usage: new-project.py YYYY-MM-DD-slug  (lowercase, digits, hyphens)")
    slug = sys.argv[1]
    today = datetime.date.today().isoformat()
    roles = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and re.fullmatch(r"\d{2}-[a-z-]+", p.name))
    for role in roles:
        d = ROOT / role / "projects" / slug
        if d.exists():
            print(f"skip (exists): {d.relative_to(ROOT)}")
            continue
        d.mkdir(parents=True)
        h = json.loads((TPL / "handoff.json").read_text(encoding="utf-8"))
        h.update(project=slug, **{"from": role}, to=FLOW.get(role, "00-chief-of-staff"), updated=today)
        (d / "handoff.json").write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        readme = (TPL / "README.md").read_text(encoding="utf-8")
        (d / "README.md").write_text(readme.replace("{{slug}}", slug).replace("{{role}}", role), encoding="utf-8")
        print(f"created: {d.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
