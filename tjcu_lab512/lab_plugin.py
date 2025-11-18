import os
import re
from datetime import datetime
from mkdocs.plugins import BasePlugin
# from mkdocs.exceptions import PluginError


class Lab512Plugin(BasePlugin):
    def on_startup(self, **kwargs):
        lab_path = '.lab'

        # create .lab file
        if not os.path.exists(lab_path):
            with open(lab_path, 'w', encoding='utf-8') as f:
                f.write('contributor_name = ""\n')

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        match = re.match(r'---lab\s*\n(.*?)\n---\s*\n(.*)', markdown, re.DOTALL)
        if not match:
            return markdown

        meta_block, content = match.groups()

        # read contributor_name
        contributor_name = ""
        if os.path.exists('.lab'):
            with open('.lab', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('contributor_name'):
                        contributor_name = line.split('=', 1)[1].strip().strip('"')

        # 解析 meta 块
        meta = {}
        for line in meta_block.splitlines():
            line = line.strip()
            if ':' not in line:
                continue
            key, value = line.split(':', 1)
            meta[key.strip().lower()] = value.strip()

        date = meta.get('date', '')
        author = meta.get('author', '')
        category = meta.get('category', '')
        tags = meta.get('tags', '')

        if not author:
            author = contributor_name
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # HTML
        html_parts = []
        if date:
            html_parts.append(f"<strong>📅 发布日期:</strong> {date}")
        if author:
            html_parts.append(f"<strong>👤 作者:</strong> {author}")
        if category:
            html_parts.append(f"<strong>📁 分类:</strong> {category}")
        if tags:
            html_parts.append(f"<strong>🏷️ 标签:</strong> {tags}")

        html = f"""
<div class="article-meta" style="background: #f0f8ff; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 20px; border-radius: 4px;">
  <p style="margin: 0; color: #666; font-size: 0.9em;">
    {" &nbsp;|&nbsp; ".join(html_parts)}
  </p>
</div>
        """.strip()

        return html + '\n\n' + content
