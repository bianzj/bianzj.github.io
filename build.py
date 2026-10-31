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

def research_image(filename, zh, en):
    from struct import unpack
    path = 'assets/research/' + filename
    width, height = unpack('>II', (ROOT / path).read_bytes()[16:24])
    return f'<a class="research-image-link" href="{path}" target="_blank" rel="noopener" aria-label="{esc(en)}"><img src="{path}" alt="{esc(zh + " / " + en)}" width="{width}" height="{height}" loading="lazy"></a>'

def image_gallery(prefix, items, label):
    tabs, panels = [], []
    for i, (key, zh, en, filename, caption_zh, caption_en) in enumerate(items):
        tab_id, panel_id = f'tab-{prefix}-{key}', f'result-{prefix}-{key}'
        tabs.append(f'<button type="button" role="tab" id="{tab_id}" aria-controls="{panel_id}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">{text(zh,en)}</button>')
        panels.append(f'<div class="result-panel" id="{panel_id}" role="tabpanel" aria-labelledby="{tab_id}">{research_image(filename,caption_zh,caption_en)}<p class="image-caption">{text(caption_zh,caption_en)}</p></div>')
    return f'<div class="result-gallery" data-gallery><div class="result-tabs" role="tablist" aria-label="{esc(label)}">{"".join(tabs)}</div>{"".join(panels)}</div>'

def research_figure(category):
    captions = {
        'modeling': ('植被结构与复杂场景建模', 'Modeling vegetation structure and complex scenes', 'modeling-schematic.png', 'TIRT 模型验证', 'TIRT model evaluation'),
        'retrieval': ('多信息协同组分温度反演', 'Component temperature retrieval with combined information', 'retrieval-schematic.png', '组分温度产品与验证', 'Component temperature products and evaluation'),
        'twins': ('过程耦合与地表温度空间模拟', 'Process coupling and spatial simulation of land surface temperature', 'twins-schematic.png', 'StreamSensor 卫星论证系统', 'StreamSensor satellite mission assessment system'),
    }
    zh, en, image_file, result_zh, result_en = captions[category]
    schematic = research_image(image_file, zh, en)
    if category == 'modeling':
        schematic = image_gallery('modeling-method', [
            ('vegetation','植被结构','Vegetation','modeling-vegetation-schematic.png','植被聚集、分层与辐射贡献解析表达','Vegetation clumping, stratification and analytical radiation contributions'),
            ('terrain','复杂场景','Complex scenes','modeling-schematic.png','复杂场景的地形与森林尺度嵌套分解','Scale decomposition of terrain and forest in complex scenes'),
        ], 'Radiative transfer modeling methods')
        result = f'''<div class="result-gallery" data-gallery>
<div class="result-tabs" role="tablist" aria-label="Model evaluation">
<button type="button" role="tab" id="tab-vegetation" aria-controls="result-vegetation" aria-selected="true" tabindex="0">{text('植被场景','Vegetation')}</button>
<button type="button" role="tab" id="tab-terrain" aria-controls="result-terrain" aria-selected="false" tabindex="-1">{text('地形场景','Terrain')}</button></div>
<div class="result-panel" id="result-vegetation" role="tabpanel" aria-labelledby="tab-vegetation">{research_image('modeling-validation.png','无人机测量、新模型与 MGP 模型对比','Comparison of UAV measurements, the new model and MGP')}<p class="image-caption">{text('无人机测量与模型模拟的方向性及误差对比','Directional patterns and errors: UAV measurements and model simulations')}</p></div>
<div class="result-panel" id="result-terrain" role="tabpanel" aria-labelledby="tab-terrain">
{research_image('modeling-terrain-validation.png','山谷、山脊和山峰场景的模型误差对比','Model errors over valley, ridge and peak scenes')}
<p class="image-caption">{text('山谷、山脊、山峰场景的方向温度模拟误差对比','Directional temperature simulation errors over valley, ridge and peak scenes')}</p></div></div>'''
    elif category == 'retrieval':
        schematic = image_gallery('retrieval-method', [
            ('overview','方法示意','Method','retrieval-schematic.png','热点效应、多像元信息与温差约束','Hotspot effects, multipixel information and temperature difference constraints'),
            ('thermal','热成像','Thermal image','retrieval-thermal-observation.png','地表热成像与热辐射角度变化示例','Surface thermal imagery and angular variations in thermal radiation'),
        ], 'Retrieval methods and observations')
        result = image_gallery('retrieval-result', [
            ('products','温度产品','Products','retrieval-products.png','AATSR、SLSTR、MSG 全球与区域组分温度产品','Global and regional component temperature products from AATSR, SLSTR and MSG'),
            ('validation','精度验证','Evaluation','retrieval-component-validation.png','土壤与植被组分温度验证及与平均温度的对比','Evaluation of soil and vegetation component temperatures and comparison with mean temperatures'),
        ], 'Temperature products and evaluation')
    else:
        result_zh, result_en = 'StreamSensor 系统与模拟验证', 'StreamSensor system and simulation evaluation'
        schematic = image_gallery('twins-method', [
            ('process','耦合示意','Coupled processes','twins-schematic.png','地表—大气—轨道—传感器耦合示意','Coupled surface, atmosphere, orbit and sensor processes'),
            ('landsat','空间对比','Spatial comparison','twins-landsat-comparison.png','Landsat 与 STREAM 地表温度空间对比','Spatial comparison of Landsat and STREAM land surface temperatures'),
        ], 'Digital twin processes and spatial simulation')
        result = image_gallery('twins-result', [
            ('system','卫星论证','Mission assessment','streamsensor-system.png','StreamSensor 卫星轨道、观测几何与成像模拟界面','StreamSensor satellite orbit, observation geometry and imaging simulation interface'),
            ('landcover','分地类验证','Land cover','twins-landcover-evaluation.png','不同地类下 STREAM、ERA5 与 GLDAS 的 Bias 和 RMSE 对比','Bias and RMSE of STREAM, ERA5 and GLDAS across land cover types'),
        ], 'Digital twin system and evaluation')
    left_label = text('机理与模拟','Model & simulation') if category == 'twins' else text('机理示意','Method schematic')
    return f'''<div class="research-visuals"><figure class="research-visual schematic"><figcaption>{left_label}<span>{text(zh,en)}</span></figcaption><div class="visual-image">{schematic}</div></figure><figure class="research-visual result"><figcaption>{text('研究成果','Research results')}<span>{text(result_zh,result_en)}</span></figcaption><div class="visual-image">{result}</div></figure><p class="image-hint">{text('点击图片查看原图','Select an image to view the original')}</p></div>'''

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
    figure = research_figure(category)
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
patents = data['achievements']['patents']
patent_count = len(patents)
first_inventor_count = sum(p['inventor_rank'] == 1 for p in patents)
paper_count = len(data['publications'])
achievement_text = {
    'zh': f'围绕辐射建模、温度反演与数字孪生，在 Remote Sensing of Environment、ISPRS Journal of Photogrammetry and Remote Sensing、IEEE Transactions on Geoscience and Remote Sensing 等期刊发表 SCI 学术论文 {data["achievements"]["sci_papers"]["zh"]}篇；获授权国家发明专利 {patent_count} 项，其中第一发明人 {first_inventor_count} 项。本页按三个研究方向选列代表性论文 {paper_count} 篇。',
    'en': f'Published {data["achievements"]["sci_papers"]["en"]} SCI-indexed papers on radiative transfer modeling, temperature retrieval and digital twins, including work in Remote Sensing of Environment, ISPRS Journal of Photogrammetry and Remote Sensing, and IEEE Transactions on Geoscience and Remote Sensing. Named as an inventor on {patent_count} granted Chinese invention patents, including {first_inventor_count} as first inventor. This page presents {paper_count} selected publications across the three research areas.'
}

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
<aside class="achievement-overview" id="achievements" aria-labelledby="achievements-title"><h3 id="achievements-title">{text('论文与专利成果','Publications & patents')}</h3><p>{bi(achievement_text)}</p><div class="achievement-numbers"><div><strong>{bi(data['achievements']['sci_papers'])}</strong><span>{text('SCI 学术论文','SCI-indexed papers')}</span></div><div><strong>{patent_count}</strong><span>{text('授权发明专利','Granted invention patents')}</span></div><div><strong>{first_inventor_count}</strong><span>{text('第一发明人专利','Patents as first inventor')}</span></div></div></aside>
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
