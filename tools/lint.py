"""Mechanical health check for the wiki (the agent does the semantic lint by reading).

    .venv/bin/python tools/lint.py            # report problems
    .venv/bin/python tools/lint.py --catalog  # print "section | [[page]] | summary" lines

Checks: frontmatter fields, broken [[wikilinks]], duplicate file names, orphan pages
(no inbound links), pages missing from index.md, practice-question callouts without
an answer, and raw/ files that no source or code page mentions.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
REQUIRED = ("type", "summary", "unit", "tags", "sources", "updated")
NO_FRONTMATTER = {"index", "log"}
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def main():
    pages = {}
    problems = defaultdict(list)
    for path in sorted(WIKI.rglob("*.md")):
        if path.stem in pages:
            problems["duplicate name"].append(f"{path.relative_to(WIKI)} vs {pages[path.stem].relative_to(WIKI)}")
        pages[path.stem] = path

    inbound = defaultdict(set)
    meta = {}
    for name, path in pages.items():
        text = path.read_text()
        fm = frontmatter(text)
        if name not in NO_FRONTMATTER:
            if fm is None:
                problems["no frontmatter"].append(name)
            else:
                meta[name] = fm
                missing = [f for f in REQUIRED if not fm.get(f)]
                if missing:
                    problems["missing fields"].append(f"{name}: {', '.join(missing)}")
        for target in LINK.findall(strip_code(text)):
            target = target.strip()
            if target in pages:
                if target != name:
                    inbound[target].add(name)
            else:
                problems["broken link"].append(f"{name} -> [[{target}]]")
        for block in re.findall(r"(> \[!question\]-.*?)(?=\n(?!>)|\Z)", text, flags=re.S):
            if "Answer" not in block:
                problems["question without answer"].append(f"{name}: {block.splitlines()[0][:70]}")

    index_text = pages["index"].read_text() if "index" in pages else ""
    index_links = set(LINK.findall(index_text))
    for name in pages:
        if name in NO_FRONTMATTER:
            continue
        if not inbound[name] - {"index"}:
            problems["orphan (only index links here)"].append(name)
        if name not in index_links:
            problems["not in index"].append(name)

    mentioned = "\n".join(p.read_text() for p in pages.values() if p.parent.name in ("sources", "code"))
    for f in sorted(RAW.rglob("*")):
        if f.is_file() and not f.name.startswith((".", "~$")) and "__pycache__" not in f.parts \
                and f.suffix not in (".zip", ".pyc") and f.name not in mentioned:
            problems["raw file never mentioned"].append(str(f.relative_to(RAW)))

    if "--catalog" in sys.argv:
        for name, fm in sorted(meta.items(), key=lambda kv: (pages[kv[0]].parent.name, kv[0])):
            print(f"{pages[name].parent.name} | [[{name}]] | {fm.get('summary', '')}")
        return

    total = sum(len(v) for v in problems.values())
    print(f"{len(pages)} pages, {sum(len(v) for v in inbound.values())} internal links, {total} problems")
    for kind, items in problems.items():
        print(f"\n{kind} ({len(items)})")
        for item in items:
            print(f"  - {item}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
