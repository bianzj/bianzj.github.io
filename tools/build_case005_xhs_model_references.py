"""Rebuild only the publication cards and citations; retain existing numerical plots."""
from pathlib import Path
import hashlib, html, json, re, shutil, zipfile
import pymupdf
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

SITE=Path(__file__).resolve().parents[1]
CASE=Path('D:/cases/StreamStudio/案例库/005_光伏草场热环境')
PACK=Path('D:/releases/streamstudio/promotion/20261107-xiaohongshu/005-photovoltaic')
SOCIAL=SITE/'assets/social/case005-xiaohongshu'
ASSETS=CASE/'publication/promotion/assets'
RENDER=PACK/'render';RENDER.mkdir(parents=True,exist_ok=True)
INK,MUTED,BLUE,GREEN='#19364b','#637887','#245e8a','#267861'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
papers=[
 dict(citation='Fan, T., Bian, Z., et al. (2025). STREAM: a system for tracing radiative transfer and energy balance in heterogeneous surfaces. International Journal of Applied Earth Observation and Geoinformation, 142, 104763.',doi='10.1016/j.jag.2025.104763',short='Fan, T., Bian, Z., et al. (2025). STREAM: a system for tracing radiative transfer and energy balance in heterogeneous surfaces. <b>JAG, 142, 104763.</b>'),
 dict(citation='Zhong, S., Bian, Z., et al. (2026). A global system for monitoring radiative transfer and directional temperatures over heterogeneous surfaces. Remote Sensing of Environment, 346, 115635.',doi='10.1016/j.rse.2026.115635',short='Zhong, S., Bian, Z., et al. (2026). A global system for monitoring radiative transfer and directional temperatures over heterogeneous surfaces. <b>RSE, 346, 115635.</b>')]

def main():
    backup=PACK/'previous-references'
    backup.mkdir(exist_ok=True)
    for name in ['02.png','03.png','02.jpg','03.jpg','caption.txt','manifest.json']:
        p=SOCIAL/name
        if p.exists() and not (backup/name).exists():shutil.copy2(p,backup/name)
    for name in ['stream-case005-xhs.html','stream_cases.json']:
        p=SITE/name
        if not (backup/name).exists():shutil.copy2(p,backup/name)
    protected={p.name:sha(p) for p in ASSETS.iterdir() if p.is_file()}
    first_sha=sha(SOCIAL/'01.png')
    pdfmetrics.registerFont(TTFont('YaHei','C:/Windows/Fonts/msyh.ttc'))
    pdfmetrics.registerFont(TTFont('YaHeiBold','C:/Windows/Fonts/msyhbd.ttc'))
    c=canvas.Canvas(str(RENDER/'reference-cards.pdf'),pagesize=(1080,1440))
    def text(s,x,y,size=28,color=INK,bold=False):
        font='YaHeiBold' if bold else 'YaHei'
        assert pdfmetrics.stringWidth(s,font,size)<=1080-x-55,s
        c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,1440-y-size,s)
    def para(s,x,y,w=950,size=25,color=MUTED):
        p=Paragraph(s,ParagraphStyle('p',fontName='YaHei',fontSize=size,leading=size*1.6,textColor=HexColor(color),wordWrap='CJK'))
        _,h=p.wrap(w,1300);p.drawOn(c,x,1440-y-h);return h
    def line(y):
        c.setFillColor(HexColor('#dce5ea'));c.rect(65,1440-y-1,950,1,fill=1,stroke=0)
    def image(name,x,y,w,h):
        im=ImageReader(str(ASSETS/name));iw,ih=im.getSize();sc=min(w/iw,h/ih)
        c.drawImage(im,x+(w-iw*sc)/2,1440-y-h+(h-ih*sc)/2,width=iw*sc,height=ih*sc,mask='auto')
    def top(tag):
        text('StreamStudio',65,48,25,INK,True);text('案例005 · '+tag,680,52,18,MUTED);line(96)
    def foot(n):
        line(1325)
        if n==3:
            text('代码与程序：github.com/bianzj/streamstudio',65,1341,15,MUTED)
            text('百度网盘：pan.baidu.com/s/1iYGVT5aC67xQ9T5A00A_YA?pwd=uvx2   提取码：uvx2',65,1366,15,MUTED)
        text('理想化数值案例 · 未完成独立实测验证',65,1400,14,MUTED);text(f'{n}/3',970,1400,14,MUTED);c.showPage()
    top('草场对照与日变化');text('同一片草场，',65,145,62,INK,True);text('板下与行间怎样变化？',65,227,62,INK,True)
    image('maps.png',55,333,970,435);text('午间草叶均温变化 −2.32 K',65,785,35,GREEN,True)
    para('0.25 m原生网格独立补算；虚线是板的垂直投影。<br/>每格平均两片原生三角面元，没有空间插值。',65,840,size=23)
    image('diurnal.png',55,945,970,285)
    para('上图是0.25 m午间空间诊断；全天曲线沿用1 m草叶网格。<br/>前24个节点预热。草叶温差不能直接解释为气温变化。[1,2]',65,1245,size=20);foot(2)
    top('热辐射方向性');text('换一个角度看，',65,135,59,INK,True);text('热红外亮温也会变',65,215,59,INK,True)
    para('同一温度场 · 12:00 · 10.5 μm<br/>板面、草叶与土壤的可见比例随方向改变。[1,2]',65,315,size=24)
    image('angular.png',55,402,970,300);text('61个方向，场景亮温极差约 5.65 K',65,718,32,BLUE,True)
    for i,(name,label) in enumerate([('view-60-0.png','北向60°'),('view-0-0.png','天底0°'),('view-60-180.png','南向60°')]):
        image(name,65+i*325,786,300,190);text(label,130+i*325,987,21)
    para('同一22–48°C色标；曲线示南北平面。亮温不同于物理温度；<br/>板发射率固定取0.90，未验证角度依赖发射率。',65,1033,size=18)
    text('模型方法参考文献',65,1102,21,INK,True)
    y=1140
    for i,paper in enumerate(papers,1):
        y+=para(f'[{i}] {paper["short"]}<br/>DOI: {paper["doi"]}',65,y,size=17,color=INK)+6
    assert y<1320,('reference overflow',y)
    foot(3);c.save()
    pdf=pymupdf.open(RENDER/'reference-cards.pdf')
    pdf_text='\n'.join(p.get_text() for p in pdf)
    assert all(p['doi'] in pdf_text for p in papers)
    assert not any(s in pdf_text for s in ['Armstrong','Barron','Faiman','Cao et al.','[1,2,5]','[4]'])
    for i,page in enumerate(pdf,2):
        page.get_pixmap().save(SOCIAL/f'{i:02d}.png')
        with Image.open(SOCIAL/f'{i:02d}.png') as im:
            assert im.size==(1080,1440)
            im.convert('RGB').save(SOCIAL/f'{i:02d}.jpg',quality=96,subsampling=0,optimize=True)
        shutil.copy2(SOCIAL/f'{i:02d}.png',SITE/f'assets/research/photovoltaic/{i:02d}.png')
    caption=(SOCIAL/'caption.txt').read_text(encoding='utf8')
    reftext='参考文献：\n'+'\n'.join(f'[{i}] {p["citation"]} DOI:{p["doi"]}' for i,p in enumerate(papers,1))+'\n\n以上文献介绍模型体系，不代表本光伏案例已完成独立实测验证。'
    caption=re.sub(r'参考文献：.*?(?=\n\n#光伏)',lambda _:reftext,caption,flags=re.S)
    assert len(caption)<1000 and not any(s in caption for s in ['Armstrong','Barron-Gafford','Faiman','Cao et al.'])
    (SOCIAL/'caption.txt').write_text(caption,encoding='utf8')
    page=SITE/'stream-case005-xhs.html';s=page.read_text(encoding='utf8')
    s=re.sub(r'(<textarea[^>]*>).*?(</textarea>)',lambda m:m[1]+html.escape(caption)+m[2],s,flags=re.S)
    s=re.sub(r'文案含参考文献，共\d+字以内。','文案含Fan的JAG、Zhong的RSE两篇模型论文。',s)
    for n in ['02','03']:
        s=re.sub(rf'({n}\.jpg)(?:\?[^"\s<]*)?(?=")',rf'\1?v=fan-zhong',s)
    page.write_text(s,encoding='utf8')
    content=SITE/'stream_cases.json';j=json.loads(content.read_text(encoding='utf8'));case=next(x for x in j['cases'] if x['number']=='005')
    case['references']=[{k:p[k] for k in ['citation','doi']} for p in papers]
    case['reference_note']['zh']='这两篇论文介绍STREAM模型体系，不代表本光伏案例已完成独立实测验证。此处提供图文推广材料；工程输入以相应发布内容为准。'
    case['reference_note']['en']='These papers describe the STREAM model family; they do not independently validate this photovoltaic case. This entry provides promotional figures and text; project inputs depend on the corresponding release.'
    content.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    assert sha(SOCIAL/'01.png')==first_sha
    assert all(sha(ASSETS/name)==h for name,h in protected.items())
    manifest={'format':'1080x1440, 3:4','cards':3,'model_rerun':False,'numerical_plot_assets_unchanged':True,'references':[{k:p[k] for k in ['citation','doi']} for p in papers],'resource_entry':'Third card footer only','files':{p.name:sha(p) for p in SOCIAL.iterdir() if p.suffix in ['.jpg','.png','.txt']}}
    (SOCIAL/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for name in ['01.jpg','02.jpg','03.jpg','caption.txt','manifest.json']:shutil.copy2(SOCIAL/name,PACK/name)
    (PACK/'参考文献.md').write_text('\n\n'.join(f'[{i}] {p["citation"]}\nhttps://doi.org/{p["doi"]}' for i,p in enumerate(papers,1)),encoding='utf8')
    with zipfile.ZipFile(PACK.parent/'光伏案例_小红书发布包.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['01.jpg','02.jpg','03.jpg','caption.txt','manifest.json','参考文献.md']:z.write(PACK/name,name)
    print(json.dumps({'cards':3,'references':2,'caption_characters':len(caption),'plot_assets_unchanged':True,'reference_block_end_y':y},ensure_ascii=False))

if __name__=='__main__':main()
