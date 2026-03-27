#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export sqlite article data into a GitHub Pages friendly static site."""

import sqlite3
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "zhuanlan.db"
SITE_DIRS = [ROOT, ROOT / "docs"]

STYLE = """
:root {
  --bg: #f5f7fb;
  --text: #17202a;
  --muted: #5f6b7a;
  --card: #ffffff;
  --line: #e6eaf0;
  --accent: #2176ff;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}

.container {
  width: min(1080px, calc(100% - 2rem));
  margin: 0 auto;
}

.hero {
  padding: 3rem 0 2rem;
}

.hero h1 {
  margin: 0;
  font-size: clamp(1.6rem, 2.8vw, 2.4rem);
  letter-spacing: 0.2px;
}

.hero p {
  color: var(--muted);
  margin: .9rem 0 0;
}

.meta {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  margin-top: 1rem;
  padding: .25rem .65rem;
  border-radius: 999px;
  background: #e9f1ff;
  color: #0f4aa8;
  font-size: .88rem;
}

.month {
  margin: 2rem 0 0;
}

.month h2 {
  margin: 0 0 1rem;
  font-size: 1.2rem;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
}

.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 22px rgba(32, 54, 86, 0.07);
}

.card img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  display: block;
  background: #dce5f2;
}

.content {
  padding: .9rem .95rem 1rem;
}

.title {
  margin: 0;
  font-size: 1rem;
}

.title a {
  text-decoration: none;
  color: var(--text);
}

.title a:hover {
  color: var(--accent);
}

.info {
  color: var(--muted);
  margin-top: .45rem;
  font-size: .87rem;
}

footer {
  border-top: 1px solid var(--line);
  margin-top: 2.6rem;
  padding: 1rem 0 2rem;
  color: var(--muted);
  font-size: .9rem;
}
""".strip()


def format_date(yyyymmdd: str) -> str:
  dt = datetime.strptime(yyyymmdd, "%Y%m%d")
  return dt.strftime("%Y-%m-%d")


def fetch_articles():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  try:
    cur = conn.execute(
      """
      SELECT title, titleImage, date, likesCount, commentsCount, url
      FROM wujun
      ORDER BY date DESC, id DESC
      """
    )
    return list(cur.fetchall())
  finally:
    conn.close()


def group_by_month(rows):
  grouped = OrderedDict()
  for row in rows:
    month_key = f"{row['date'][:4]}-{row['date'][4:6]}"
    grouped.setdefault(month_key, []).append(row)
  return grouped


def build_html(rows):
  grouped = group_by_month(rows)

  sections = []
  for month, articles in grouped.items():
    cards = []
    for item in articles:
      title = escape(item["title"])
      url = escape(item["url"])
      image = escape(item["titleImage"])
      date = format_date(item["date"])
      likes = int(item["likesCount"])
      comments = int(item["commentsCount"])
      cards.append(
        f"""
        <article class=\"card\">
          <img src=\"{image}\" alt=\"{title}\" loading=\"lazy\" />
          <div class=\"content\">
            <h3 class=\"title\"><a href=\"{url}\" target=\"_blank\" rel=\"noopener noreferrer\">{title}</a></h3>
            <div class=\"info\">{date} · 👍 {likes} · 💬 {comments}</div>
          </div>
        </article>
        """.strip()
      )

    sections.append(
      f"""
      <section class=\"month\">
        <h2>{month}</h2>
        <div class=\"grid\">
          {''.join(cards)}
        </div>
      </section>
      """.strip()
    )

  count = len(rows)
  today = datetime.utcnow().strftime("%Y-%m-%d")

  return f"""<!doctype html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>吴军《发明365》静态归档</title>
    <meta name=\"description\" content=\"由 sqlite 数据导出的吴军《发明365》静态博客归档\" />
    <link rel=\"stylesheet\" href=\"./style.css\" />
  </head>
  <body>
    <header class=\"hero\">
      <div class=\"container\">
        <h1>吴军《文明之光》之《发明365》</h1>
        <p>从原站点 sqlite 数据直接导出的静态页面，可直接部署到 GitHub Pages。</p>
        <div class=\"meta\">共 {count} 篇 · 最后生成于 {today}</div>
      </div>
    </header>

    <main class=\"container\">
      {''.join(sections)}
    </main>

    <footer>
      <div class=\"container\">数据源：仓库内 zhuanlan.db（wujun 表）</div>
    </footer>
  </body>
</html>
"""


def main():
  rows = fetch_articles()
  html = build_html(rows)
  css = STYLE + "\n"

  outputs = []
  for site_dir in SITE_DIRS:
    site_dir.mkdir(parents=True, exist_ok=True)
    index_path = site_dir / "index.html"
    style_path = site_dir / "style.css"
    nojekyll_path = site_dir / ".nojekyll"

    index_path.write_text(html, encoding="utf-8")
    style_path.write_text(css, encoding="utf-8")
    nojekyll_path.write_text("", encoding="utf-8")
    outputs.extend([index_path, style_path, nojekyll_path])

  print(f"Generated {len(outputs)} files from {DB_PATH}:")
  for output in outputs:
    print(f"- {output}")


if __name__ == "__main__":
  main()
