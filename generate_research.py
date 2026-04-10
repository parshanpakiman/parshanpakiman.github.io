#!/usr/bin/env python3

from __future__ import annotations

import csv
import html
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "papers.csv"
OUTPUT_PATH = ROOT / "research.html"


def escape(value: str) -> str:
    return html.escape(value or "", quote=True)


def build_link(url: str, icon_class: str, label: str) -> str:
    if not url:
        return f'<span id="inactiveLink" class="fa {icon_class}" aria-hidden="true"></span>'

    return (
        f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{escape(label)}"><i id="activeLink" class="fa {icon_class}" '
        f'aria-hidden="true"></i></a>'
    )


def build_paper(paper: dict[str, str]) -> str:
    status_prefix = paper.get("status_prefix", "").strip()
    venue = paper.get("venue", "").strip()

    status_line = escape(status_prefix)
    if venue:
        status_line = (
            f'{status_line} <span class="journal-text-format">{escape(venue)}</span>'
        )

    title = paper.get("title", "").strip()
    authors = paper.get("authors", "").strip()

    paper_link = build_link(paper.get("paper_url", "").strip(), "fa-link", f"{title} paper link")
    code_link = build_link(paper.get("code_url", "").strip(), "fa-file-code-o", f"{title} code link")

    return f"""      <div class="container">
        <div id="paperInfo">
          <div id="number"><div class="container"><span>&#8226;</span></div></div>
          <div id="paperTitle">
            <div class="title-paper-text-format">{escape(title)}</div>
            <span class="author-text-format">{escape(authors)}</span><br>
            <div class="status-text-format">{status_line}</div>
          </div>
          <div class="relatedLinks">
            <div id="links">
              {paper_link}
              {code_link}
            </div>
          </div>
        </div>
      </div>"""


def load_papers() -> OrderedDict[str, list[dict[str, str]]]:
    sections: OrderedDict[str, list[dict[str, str]]] = OrderedDict()

    with CSV_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            section = (row.get("section") or "Papers").strip()
            sections.setdefault(section, []).append(row)

    for papers in sections.values():
        papers.sort(key=lambda item: int((item.get("order") or "0").strip() or "0"))

    return sections


def build_html() -> str:
    sections = load_papers()

    section_blocks = []
    for title, papers in sections.items():
        section_header = f"""      <div class="container">
        <div id="customized_title">{escape(title)} <hr></div>
      </div>"""
        paper_blocks = "\n".join(build_paper(paper) for paper in papers)
        section_blocks.append(f"{section_header}\n{paper_blocks}")

    sections_html = "\n\n".join(section_blocks)

    return f"""<!DOCTYPE HTML>
<html>

<head>
  <title>Research</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Research papers and projects by Parshan Pakiman." />
  <meta name="keywords" content="Parshan Pakiman research papers operations management" />
  <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
  <link rel="stylesheet" type="text/css" href="style/style.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo"></div>
    </div>

    <div id="menubar">
      <div id="firstLastName">
        <ul id="menu">
          <li><a href="vita.html">Vita</a></li>
          <li><a href="teaching.html">Teaching</a></li>
          <li class="selected"><a href="research.html">Research</a></li>
          <li><a href="index.html">Home</a></li>
        </ul>
      </div>
    </div>

    <div id="site_content">
{sections_html}
      <hr class="section-divider" style="margin-top: 18px;" />
    </div>
  </div>

  <script src="style/scripts.js" defer></script>
</body>

</html>
"""


def main() -> None:
    OUTPUT_PATH.write_text(build_html(), encoding="utf-8")
    print(f"Updated {OUTPUT_PATH.name} from {CSV_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
