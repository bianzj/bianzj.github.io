#!/usr/bin/env python3
"""Build the bilingual, dependency-free academic homepage from profile.json."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'profile.json').read_text())

def esc(value):
    return html.escape(str(value), quote=True)

def bi(value):
    return f'<span class="zh">{esc(value["zh"])}</span><span class="en" lang="en">{esc(value["en"])}</span>'

def text(zh, en):
    return bi({'zh': zh, 'en': en})

def heading(number, zh, en, note=''):
    return f'<div class="section-head"><div class="section-label"><span class="section-no">{number}</span><h2>{text(zh,en)}</h2></div>{note}</div>'

def timeline(items):
    return '<div class="timeline">' + ''.join(f'<article class="timeline-item"><div class="date">{esc(i["date"])}</div><h3>{bi(i["title"])}</h3><div class="place">{bi(i["place"])}</div></article>' for i in items) + '</div>'

def render_paper(p):
    authors = esc(p['authors']).replace('Bian, Z.', '<strong>Bian, Z.</strong>')
    title = bi({'zh': p['title_zh'], 'en': p['title']}) if p.get('title_zh') else esc(p['title'])
    journal = bi({'zh': p['journal_zh'], 'en': p['journal']}) if p.get('journal_zh') else esc(p['journal'])
    if p.get('authors_zh'):
        authors_zh = esc(p['authors_zh']).replace('卞尊健', '<strong>卞尊健</strong>')
        authors = f'<span class="zh">{authors_zh}</span><span class="en" lang="en">{authors}</span>'
    return f'''<article class="pub" data-category="{esc(p['category'])}"><div class="pub-year">{esc(p['year'])}</div><div><h4><a href="https://doi.org/{esc(p['doi'])}">{title}</a></h4><div class="pub-authors">{authors}</div><div class="pub-journal"><em>{journal}</em> · {esc(p['details'])}</div></div><a class="pub-link" href="https://doi.org/{esc(p['doi'])}" aria-label="DOI: {esc(p['title'])}">↗</a></article>'''

def model_emphasis(value):
    result = bi(value)
    for model in ['TIRT', 'STREAM']:
        result = result.replace(model, f'<em>{model}</em>')
    return result

def modeling_figure():
    labels = {
        'figure_title': ('复杂结构与热辐射“时空角”特征关系示意', 'Complex surface structure and thermal radiation variability'),
        'vegetation': ('植被场景', 'Vegetation'),
        'terrain': ('植被 + 地形', 'Vegetation + terrain'),
        'urban': ('植被 + 城市', 'Vegetation + urban surfaces'),
        'clumping': ('聚集效应 · 分层特征', 'Clumping · Vertical stratification'),
        'terrain_features': ('地形起伏 · 植被分布', 'Terrain relief · Vegetation distribution'),
        'urban_features': ('建筑形态 · 植被配置', 'Building form · Vegetation arrangement'),
        'structure_input': ('复杂结构', 'Complex structure'),
        'radiative_transfer': ('辐射传输', 'Radiative transfer'),
        'radiation_response': ('热辐射响应', 'Thermal radiation response'),
        'time': ('时间', 'Time'), 'time_detail': ('时间变化', 'Temporal variation'),
        'space': ('空间', 'Space'), 'space_detail': ('空间异质性', 'Spatial heterogeneity'),
        'angle': ('角度', 'Angle'), 'angle_detail': ('方向差异', 'Directional variation'),
        'conceptual_note': ('结构与响应关系示意；图中曲线和色块不表示定量模拟结果。', 'Conceptual relationships; curves and color patches do not represent quantitative simulation results.'),
    }
    result = (ROOT / 'templates/modeling-figure.html').read_text()
    for key, (zh, en) in labels.items():
        result = result.replace('{{' + key + '}}', text(zh, en))
    alternatives = {
        'figure_alt': 'Conceptual diagram of complex surface structures, TIRT, and temporal, spatial and angular thermal radiation variations',
        'vegetation_alt': 'Clustered tree crowns with distinct vertical layers',
        'terrain_alt': 'Vegetation distributed across sloping terrain',
        'urban_alt': 'Buildings of different heights interspersed with vegetation',
    }
    for key, value in alternatives.items():
        result = result.replace('{{' + key + '}}', esc(value))
    return result

research_groups = []
for research in data['research']:
    category = research['category']
    category_papers = [p for p in data['publications'] if p['category'] == category]
    question = f'<p class="research-question"><strong>{bi(research["question"])}</strong></p>' if research.get('question') else ''
    if research.get('summary'):
        overview = f'<p class="research-summary">{model_emphasis(research["summary"])}</p>'
    else:
        findings = ''.join(f'<li>{model_emphasis(finding)}</li>' for finding in research['contributions'])
        overview = f'<div class="contribution-box"><ol class="contributions">{findings}</ol></div>'
    figure = modeling_figure() if research.get('figure') == 'modeling' else ''
    research_groups.append(f'''<section class="research-group" id="research-{esc(category)}" aria-labelledby="title-{esc(category)}">
<div class="research-group-heading"><h3 id="title-{esc(category)}">{bi(research['title'])}</h3><a class="method-name" href="{esc(research['url'])}">{esc(research['name'])}</a></div>
{question}
<div class="research-overview">{overview}</div>
{figure}
<details class="paper-details"><summary class="group-paper-heading"><span>{text('代表性论文','Selected publications')}</span><span class="paper-fold-meta"><span class="section-note">{text(f'{len(category_papers)} 篇',f'{len(category_papers)} papers')}</span><span class="fold-label fold-closed">{text('展开','Show')}</span><span class="fold-label fold-open">{text('收起','Hide')}</span><span class="fold-icon" aria-hidden="true"></span></span></summary>
<div class="group-papers">{''.join(render_paper(p) for p in category_papers)}</div>
</details>
</section>''')
projects = ''.join(f'<article class="project"><div class="date">{esc(p["date"])}</div><h3>{bi(p["title"])}</h3><div class="place">{bi(p["funder"])}</div></article>' for p in data['projects'])
honors = ''.join(f'<div class="honor"><time>{esc(p["year"])}</time><span>{bi(p["title"])}</span></div>' for p in data['honors'])
committees = ''.join(f'<article class="project service-item"><h3>{bi(item["title"])}</h3><div class="place">{bi(item["organization"])}</div></article>' for item in data['academic_service']['committees'])
conferences = ''.join(f'<article class="project service-item"><h3>{bi(item["title"])}</h3><div class="place">{bi(item["detail"])}</div></article>' for item in data['academic_service']['conferences'])
research_nav = ''.join(f'<a href="#research-{esc(r["category"])}">{bi(r["title"])}</a>' for r in data['research'])

page = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="卞尊健 Zunjian Bian，中国科学院空天信息创新研究院副研究员。研究方向：辐射建模、温度反演与数字孪生。TIRT · LS4T · STREAM Studio.">
<meta name="theme-color" content="#285e4e">
<meta property="og:type" content="profile">
<meta property="og:title" content="卞尊健 Zunjian Bian | 热红外遥感">
<meta property="og:description" content="Radiative transfer modeling · Temperature retrieval · Digital twins">
<meta property="og:url" content="https://bianzj.github.io/">
<link rel="canonical" href="https://bianzj.github.io/">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="stylesheet" href="assets/site.css">
<script defer src="assets/site.js"></script>
<title>卞尊健 | 热红外遥感</title>
</head>
<body>
<a class="skip" href="#main">{text('跳到正文','Skip to content')}</a>
<header class="header"><div class="wrap nav">
<a class="brand" href="#main">Zunjian Bian<span>ACADEMIC PROFILE</span></a>
<nav class="nav-links" aria-label="Main navigation">
<a href="#research">{text('研究与论文','Research')}</a>
<a href="#cv">{text('简历','CV')}</a>
<a class="desktop-link" href="#service">{text('学术服务','Service')}</a>
<a class="desktop-link" href="#software">{text('软件','Software')}</a>
<button type="button" class="language" id="language-toggle" aria-label="Switch to English">EN</button>
</nav></div></header>
<main id="main" class="wrap">
<section class="hero" aria-labelledby="name">
<div class="hero-copy">
<span class="eyebrow">THERMAL INFRARED REMOTE SENSING</span>
<h1 id="name">{bi(data['name'])}</h1>
<div class="roman">{text('Zunjian Bian','卞尊健')}</div>
<div class="role">{bi(data['role'])}</div>
<div class="affiliation">{bi(data['institution'])}<br>{bi(data['laboratory'])}</div>
<p class="intro">{bi(data['intro'])}</p>
<div class="actions">
<a class="button primary" href="mailto:{esc(data['email'])}">{text('邮件联系','Get in touch')}<span aria-hidden="true">↗</span></a>
<a class="button" href="{esc(data['github'])}">GitHub<span aria-hidden="true">↗</span></a>
<button class="button" type="button" id="print-cv">{text('打印简历','Print CV')}<span aria-hidden="true">↓</span></button>
</div>
<p class="print-only">{esc(data['email'])} · https://bianzj.github.io/ · {esc(data['github'])}</p>
</div>
<figure class="portrait"><div class="portrait-frame"><img src="assets/portrait.jpg" alt="卞尊健 Zunjian Bian" width="420" height="540" fetchpriority="high"></div><figcaption><span>BEIJING, CHINA</span><span>中国科学院 · CAS</span></figcaption></figure>
</section>
<div class="topic-line" aria-label="Research interests"><span>{text('辐射建模','RADIATIVE TRANSFER MODELING')}</span><span>{text('温度反演','TEMPERATURE RETRIEVAL')}</span><span>{text('数字孪生','DIGITAL TWINS')}</span></div>
<section class="section" id="research">
<span id="publications"></span>
{heading('01','研究方向与代表性论文','Research & selected publications')}
<nav class="research-nav" aria-label="Research areas">{research_nav}</nav>
{''.join(research_groups)}
</section>
<section class="section" id="cv">
{heading('02','教育与工作经历','Experience & education')}
<div class="cv-grid"><div><h3 class="subheading">{text('工作经历','Appointments')}</h3>{timeline(data['experience'])}</div><div><h3 class="subheading">{text('教育经历','Education')}</h3>{timeline(data['education'])}</div></div>
</section>
<section class="section" id="projects">
{heading('03','科研项目与荣誉','Projects & recognition')}
<div class="lower-grid"><div><h3 class="subheading">{text('代表项目','Selected projects')}</h3>{projects}</div><div><h3 class="subheading">{text('人才计划与荣誉','Programs & honors')}</h3>{honors}</div></div>
</section>
<section class="section" id="service">
{heading('04','学术服务','Academic service')}
<div class="cv-grid"><div><h3 class="subheading">{text('学术任职','Committee memberships')}</h3>{committees}</div><div><h3 class="subheading">{text('会议组织','Conference organization')}</h3>{conferences}</div></div>
</section>
<section class="section" id="software">
{heading('05','科研软件','Research software')}
<div class="software"><div><span class="eyebrow">MODELS INTO PRACTICE</span><h3>STREAM Studio</h3><p>{text('面向遥感数字孪生与模拟实验的软件工具。访问项目仓库，了解功能、安装方式和使用文档；TIRT 与 LS4T 也可通过各自仓库获取。','Software for remote sensing digital twins and numerical experiments. Visit the repository for features, installation instructions, and documentation. TIRT and LS4T are also available in their respective repositories.')}</p></div><a class="button" href="https://github.com/bianzj/streamstudio">{text('访问软件仓库','Explore the repository')}<span aria-hidden="true">↗</span></a></div>
</section>
<section class="section" id="contact"><div class="contact-grid"><div><span class="eyebrow">CONTACT</span><h2>{text('交流与合作','Let’s connect')}</h2><p>{text('欢迎就热红外遥感、辐射传输、温度产品与遥感数字孪生交流。','For discussions on thermal infrared remote sensing, radiative transfer, temperature products, and remote sensing digital twins.')}</p></div><a class="email" href="mailto:{esc(data['email'])}">{esc(data['email'])}<span aria-hidden="true"> ↗</span></a></div></section>
</main>
<footer class="footer wrap"><span>© 2026 Zunjian Bian · {text('更新于','Updated')} {esc(data['updated'])}</span><span><a href="{esc(data['official_profile'])}">{text('实验室个人主页','Institutional profile')}</a> · <a href="{esc(data['github'])}">GitHub</a></span></footer>
</body></html>
'''
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print(f'Built index.html: {len(data["publications"])} publications, bilingual profile.')
