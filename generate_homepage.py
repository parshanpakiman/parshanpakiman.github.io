#!/usr/bin/env python3

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "index.html"
CONTENT_PATH = ROOT / "data" / "homepage_research.txt"

START_MARKER = "      <!-- HOMEPAGE_RESEARCH_START -->"
END_MARKER = "      <!-- HOMEPAGE_RESEARCH_END -->"


def main() -> None:
    index_html = INDEX_PATH.read_text(encoding="utf-8")
    paragraphs = [
        paragraph.strip()
        for paragraph in CONTENT_PATH.read_text(encoding="utf-8").split("\n\n")
        if paragraph.strip()
    ]

    rendered_paragraphs = [
        (
            '      <p style="line-height: 1.5em; margin-left: 0px; margin-top: 0px; text-indent: 0px;">\n'
            f"        {escape(paragraph)}\n"
            "      </p>"
        )
        for paragraph in paragraphs
    ]

    research_html = (
        '      <h3 style="margin-top:10px;">Research</h3>\n'
        + "\n      <br/>\n".join(rendered_paragraphs)
    )

    start = index_html.find(START_MARKER)
    end = index_html.find(END_MARKER)

    if start == -1 or end == -1 or end <= start:
        raise RuntimeError("Homepage research markers were not found in index.html")

    start_content = start + len(START_MARKER)
    updated_index = (
        index_html[:start_content]
        + "\n"
        + research_html
        + "\n"
        + index_html[end:]
    )

    INDEX_PATH.write_text(updated_index, encoding="utf-8")
    print(f"Updated {INDEX_PATH.name} from {CONTENT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
