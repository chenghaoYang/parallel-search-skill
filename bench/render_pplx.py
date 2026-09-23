"""给 pplx-web 的 JSON 对象生成引用列表，由 run_arm.py 使用。"""


def citations_md(data, snippets=True):
    lines = []
    for i, c in enumerate(data.get("citations") or [], start=1):
        title = (c.get("title") or "").strip()
        url = (c.get("url") or "").strip()
        line = f"{i}. [{title}]({url})"
        if snippets:
            line += " — " + " ".join((c.get("snippet") or "").split())
        lines.append(line)
    return "\n".join(lines)
