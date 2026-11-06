"""Build a venue-neutral LaTeX manuscript from the reviewed Markdown source."""

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "MANUSCRIPT.md"
OUTPUT = HERE / "manuscript.tex"

CITE_KEYS = {
    1: "el2026physics",
    2: "guo2024survey",
    3: "li2023camel",
    4: "wu2024autogen",
    5: "du2024debate",
    6: "liang2024divergent",
    7: "zhang2024social",
    8: "li2024sparse",
    9: "wang2024bounds",
    10: "chuang2024opinion",
    11: "choi2025conformity",
    12: "ashery2025conventions",
    13: "zomer2026collective",
    14: "ko2026social",
    15: "oh2026belief",
    16: "amayuelas2024attack",
    17: "kraidia2026persuasion",
    18: "south2025delegation",
    19: "garzon2026credentials",
    20: "douceur2002sybil",
    21: "jung2012security",
    22: "nist2008hmac",
    23: "castro1999pbft",
    24: "debenedetti2024agentdojo",
    25: "zhang2025asb",
    26: "zhan2024injecagent",
}


def stash(value, store):
    key = f"ZZTOKEN{len(store)}ZZ"
    store[key] = value
    return key


def convert_inline(text):
    store = {}

    def cite_range(match):
        start, end = map(int, match.groups())
        keys = ",".join(CITE_KEYS[i] for i in range(start, end + 1))
        return stash(f"\\cite{{{keys}}}", store)

    def cite_single(match):
        numbers = [int(value) for value in re.findall(r"\d+", match.group(1))]
        keys = ",".join(CITE_KEYS[i] for i in numbers)
        return stash(f"\\cite{{{keys}}}", store)

    text = re.sub(r"\[(\d+)\]\s*[–-]\s*\[(\d+)\]", cite_range, text)
    text = re.sub(r"\[([0-9, ]+)\]", cite_single, text)
    text = re.sub(r"\\\(.*?\\\)", lambda m: stash(m.group(0), store), text)
    def inline_code(match):
        value = match.group(1)
        if "/" in value:
            return stash("\\nolinkurl{" + value.replace("%", "\\%") + "}", store)
        return stash("\\texttt{" + escape_tex(value) + "}", store)

    text = re.sub(r"`([^`]+)`", inline_code, text)
    text = re.sub(
        r"\*\*([^*]+)\*\*",
        lambda m: stash("\\textbf{" + convert_inline(m.group(1)) + "}", store),
        text,
    )
    text = re.sub(
        r"\*([^*]+)\*",
        lambda m: stash("\\textit{" + convert_inline(m.group(1)) + "}", store),
        text,
    )
    text = escape_tex(text)
    for key, value in store.items():
        text = text.replace(key, value)
    return text


def escape_tex(text):
    replacements = {
        "\\": "ZZBACKSLASHZZ",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text.replace("ZZBACKSLASHZZ", r"\textbackslash{}")


def table_to_tex(rows, caption):
    cells = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows]
    cells = [row for row in cells if not all(re.fullmatch(r":?-+:?", cell) for cell in row)]
    width = len(cells[0])
    alignment = "l" + "r" * (width - 1)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{" + convert_inline(caption) + "}",
        r"\scriptsize",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{" + alignment + "}",
        r"\toprule",
        " & ".join(convert_inline(cell) for cell in cells[0]) + r" \\",
        r"\midrule",
    ]
    for row in cells[1:]:
        lines.append(" & ".join(convert_inline(cell) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{table}", r"\FloatBarrier"])
    return lines


def heading_title(raw):
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", raw).strip()


def convert():
    lines = SOURCE.read_text().splitlines()
    out = []
    in_equation = False
    pending_table_caption = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "## References":
            break
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("**Author:**") or line.startswith("**Affiliation:**") or line.startswith("**Corresponding author:**"):
            i += 1
            continue
        if line == "## Abstract":
            out.append(r"\begin{abstract}")
            i += 1
            continue
        if line == "## \u6458要":
            out.extend([r"\end{abstract}", r"\section*{摘要}"])
            i += 1
            continue
        if line.startswith("## "):
            out.append(r"\section{" + convert_inline(heading_title(line[3:])) + "}")
            i += 1
            continue
        if line.startswith("### "):
            out.append(r"\subsection{" + convert_inline(heading_title(line[4:])) + "}")
            i += 1
            continue
        if line.startswith("**Table ") and line.endswith("**"):
            pending_table_caption = re.sub(r"^Table \d+\.\s*", "", line[2:-2])
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.extend(table_to_tex(rows, pending_table_caption or "Study table"))
            pending_table_caption = None
            continue
        if line.startswith("!["):
            match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            caption = match.group(1) if match else "Study figure"
            path = match.group(2) if match else ""
            if i + 2 < len(lines) and lines[i + 2].startswith("**Figure "):
                caption_line = lines[i + 2].replace("**", "")
                caption = re.sub(r"^Figure \d+\.\s*", "", caption_line)
                i += 2
            out.extend(
                [
                    r"\begin{figure}[htbp]",
                    r"\centering",
                    r"\includegraphics[width=\textwidth]{" + path + "}",
                    r"\caption{" + convert_inline(caption) + "}",
                    r"\end{figure}",
                    r"\FloatBarrier",
                ]
            )
            i += 1
            continue
        if line.strip() == r"\[":
            in_equation = True
            out.append(line)
            i += 1
            continue
        if in_equation:
            out.append(line)
            if line.strip() == r"\]":
                in_equation = False
            i += 1
            continue
        if line.strip() == "---":
            i += 1
            continue
        if line.strip():
            out.append(convert_inline(line))
        else:
            out.append("")
        i += 1
    return "\n".join(out)


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont{Times New Roman}
\setCJKmainfont{Songti TC}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{float}
\usepackage{placeins}
\usepackage[hidelinks]{hyperref}
\usepackage{microtype}
\setlength{\parindent}{1.5em}
\setlength{\parskip}{0.25em}
\title{Authenticated Relationship Routing Mitigates External-Identity Attacks in LLM-Agent Collectives}
\author{Ben Tseng\\\small Affiliation to be confirmed before submission}
\date{}
\begin{document}
\maketitle
"""

ENDING = r"""
\begingroup
\small
\bibliographystyle{IEEEtran}
\bibliography{references}
\endgroup
\end{document}
"""


if __name__ == "__main__":
    OUTPUT.write_text(PREAMBLE + convert() + ENDING)
    print(f"wrote {OUTPUT}")
