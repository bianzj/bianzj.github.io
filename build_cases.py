"""Render the static STREAM case studies page using the site's shared helpers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build_cases(profile, bi, text, heading, research_image):
    content = json.loads((ROOT / 'stream_cases.json').read_text())
    cards, sections = [], []
    for i, case in enumerate(content['cases'], 1):
        cards.append(f'''<a class="case-card" href="#{case['id']}"><span class="case-number">0{i}</span><h2>{bi(case['title'])}</h2><p>{bi(case['tag'])}</p><span class="case-arrow" aria-hidden="true">↗</span></a>''')
        steps = ''.join(f'<div><dt>{bi(step["label"])}</dt><dd>{bi(step["text"])}</dd></div>' for step in case['steps'])
        figure = f'''<figure class="case-figure">{research_image(case['image'],case['caption']['zh'],case['caption']['en'])}<figcaption>{bi(case['caption'])}</figcaption></figure>'''
        if case.get('secondary_image'):
            figure += f'''<figure class="case-figure secondary-figure">{research_image(case['secondary_image'],case['secondary_caption']['zh'],case['secondary_caption']['en'])}<figcaption>{bi(case['secondary_caption'])}</figcaption></figure>'''
        related = f'<a class="case-paper" href="https://doi.org/{case["doi"]}">{text("相关论文","Related paper")} ↗</a>' if case.get('doi') else ''
        sections.append(f'''<section class="section case-section" id="{case['id']}">{heading(f'0{i}',case['title']['zh'],case['title']['en'])}<p class="case-summary">{bi(case['summary'])}</p><div class="case-layout"><div class="case-copy"><dl>{steps}</dl>{related}</div><div class="case-images">{figure}</div></div></section>''')
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>STREAM 案例 | 卞尊健</title><meta name="description" content="STREAM 遥感数字孪生应用案例：地表温度空间模拟、多地类精度验证与 StreamSensor 卫星论证。">
<meta name="theme-color" content="#285e4e"><link rel="canonical" href="https://bianzj.github.io/stream.html">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/cases.css"><script defer src="assets/site.js"></script></head>
<body class="cases-page" data-title-zh="STREAM 案例 | 卞尊健" data-title-en="STREAM case studies | Zunjian Bian">
<a class="skip" href="#main">{text('跳到正文','Skip to content')}</a>
<header class="header"><div class="wrap nav"><a class="brand" href="stream.html">STREAM<span>CASE STUDIES</span></a><nav class="nav-links" aria-label="Main navigation"><a href="index.html">{text('个人主页','Profile')}</a><a class="desktop-link" href="#cases">{text('案例目录','Cases')}</a><a class="desktop-link" href="https://github.com/bianzj/streamstudio">GitHub ↗</a><button type="button" class="language" id="language-toggle" aria-label="Switch to English">EN</button></nav></div></header>
<main id="main" class="wrap"><section class="case-hero"><span class="eyebrow">REMOTE SENSING DIGITAL TWINS</span><h1>{bi(content['title'])}</h1><p>{bi(content['intro'])}</p><div class="actions"><a class="button primary" href="#cases">{text('浏览案例','Explore cases')} ↓</a><a class="button" href="index.html#research-twins">{text('研究背景','Research background')} ↗</a></div></section>
<nav class="case-index" id="cases" aria-label="Case studies">{''.join(cards)}</nav>
{''.join(sections)}
<section class="case-access"><div><span class="eyebrow">STREAM STUDIO</span><h2>{text('获取软件与使用文档','Software & documentation')}</h2><p>{text('通过 STREAM Studio 项目仓库了解软件功能、安装方式和使用文档。','Visit the STREAM Studio repository for software features, installation instructions and documentation.')}</p></div><a class="button primary" href="https://github.com/bianzj/streamstudio">{text('访问软件仓库','Explore the repository')} ↗</a></section>
<p class="case-original-note">{text('点击案例图片可查看原图。','Select a case image to view the original.')}</p>
</main><footer class="footer wrap"><span>© 2026 Zunjian Bian · STREAM</span><span><a href="index.html">{text('返回个人主页','Back to profile')}</a> · <a href="mailto:{profile['email']}">{text('交流与合作','Contact')}</a></span></footer></body></html>'''
    (ROOT / 'stream.html').write_text(page, encoding='utf-8')
