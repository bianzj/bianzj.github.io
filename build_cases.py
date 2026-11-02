"""Render the static STREAM Studio software cases page using the site's shared helpers."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build_cases(profile, bi, text, heading, research_image):
    content = json.loads((ROOT / 'stream_cases.json').read_text())
    cards, sections = [], []
    for i, case in enumerate(content['cases'], 1):
        number = case.get('number', f'{i:03}')
        cards.append(f'''<a class="case-card" href="#{case['id']}"><span class="case-number">{escape(number)}</span><h2>{bi(case['title'])}</h2><p>{bi(case['tag'])}</p><span class="case-arrow" aria-hidden="true">↗</span></a>''')
        steps = ''.join(f'<div><dt>{bi(step["label"])}</dt><dd>{bi(step["text"])}</dd></div>' for step in case['steps'])
        figure = f'''<figure class="case-figure">{research_image(case['image'],case['caption']['zh'],case['caption']['en'])}<figcaption>{bi(case['caption'])}</figcaption></figure>'''
        if case.get('secondary_image'):
            figure += f'''<figure class="case-figure secondary-figure">{research_image(case['secondary_image'],case['secondary_caption']['zh'],case['secondary_caption']['en'])}<figcaption>{bi(case['secondary_caption'])}</figcaption></figure>'''
        for item in case.get('additional_images', []):
            figure += f'''<figure class="case-figure secondary-figure">{research_image(item['image'],item['caption']['zh'],item['caption']['en'])}<figcaption>{bi(item['caption'])}</figcaption></figure>'''
        related = f'<a class="case-paper" href="https://doi.org/{case["doi"]}">{text("相关论文","Related paper")} ↗</a>' if case.get('doi') else ''
        for paper in case.get('references', []):
            related += f'<p class="case-reference">{escape(paper["citation"])}<br><a class="case-paper" href="https://doi.org/{escape(paper["doi"], quote=True)}">DOI: {escape(paper["doi"])}</a></p>'
        if case.get('reference_note'):
            related += f'<p class="case-reference">{bi(case["reference_note"])}</p>'
        download = ''
        if case.get('document'):
            download = f'<p class="case-download"><a class="button" href="{escape(case["document"], quote=True)}" download>{text("下载案例库 Word","Download case library (Word)")} ↓</a></p>'
        sections.append(f'''<section class="section case-section" id="{case['id']}">{heading(number,case['title']['zh'],case['title']['en'])}<p class="case-summary">{bi(case['summary'])}</p>{download}<div class="case-layout"><div class="case-copy"><dl>{steps}</dl>{related}</div><div class="case-images">{figure}</div></div></section>''')
    case_content = (f'<nav class="case-index" id="cases" aria-label="Case studies">{"".join(cards)}</nav>' + ''.join(sections)) if cards else f'<section class="case-placeholder" id="cases"><p>{text("案例内容待补充。","Case studies will be added here.")}</p></section>'
    page = f''' <!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>STREAM Studio 软件案例 | 卞尊健</title><meta name="description" content="STREAM Studio 软件使用案例与操作示例。">
<meta name="theme-color" content="#285e4e"><link rel="canonical" href="https://bianzj.github.io/stream.html">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/cases.css"><script defer src="assets/site.js"></script></head>
<body class="cases-page" data-title-zh="STREAM Studio 软件案例 | 卞尊健" data-title-en="STREAM Studio case studies | Zunjian Bian">
<a class="skip" href="#main">{text('跳到正文','Skip to content')}</a>
<header class="header"><div class="wrap nav"><a class="brand" href="stream.html">STREAM Studio<span>CASES</span></a><nav class="nav-links" aria-label="Main navigation"><a href="index.html">{text('个人主页','Profile')}</a><a class="desktop-link" href="https://github.com/bianzj/streamstudio">GitHub ↗</a><button type="button" class="language" id="language-toggle" aria-label="Switch to English">EN</button></nav></div></header>
<main id="main" class="wrap"><section class="case-hero"><span class="eyebrow">SOFTWARE CASE STUDIES</span><h1>{bi(content['title'])}</h1><p>{bi(content['intro'])}</p></section>
{case_content}
</main><footer class="footer wrap"><span>© 2026 Zunjian Bian · STREAM Studio</span><span><a href="index.html">{text('返回个人主页','Back to profile')}</a> · <a href="mailto:{profile['email']}">{text('交流与合作','Contact')}</a></span></footer></body></html>'''
    (ROOT / 'stream.html').write_text(page, encoding='utf-8')
