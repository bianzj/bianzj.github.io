# 卞尊健 Zunjian Bian

科研个人主页，计划发布于 https://bianzj.github.io/ 。支持中英文切换、研究进展与代表论文分方向展示，以及打印简历。论文默认折叠，点击展开；打印时自动展开全部论文。每个方向采用左侧机理示意、右侧成果图的布局，图片点击可查看原图；辐射建模的右侧可切换植被和地形验证。三组示意图和成果图使用用户提供的原图，保留色标、坐标和图内标注，图片位于 `assets/research/`。纯静态页面，无第三方字体、分析跟踪或前端构建依赖。

## 更新内容

编辑 `profile.json`，然后运行：

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器打开 http://127.0.0.1:8765 。修改样式请编辑 `assets/site.css`，交互逻辑位于 `assets/site.js`。

## 发布

仓库名称为 `bianzj.github.io`，账号为 `bianzj`。将主页文件推送到 `main`，在仓库 Settings → Pages 中，选择 Deploy from a branch → main → /(root)。页面无需 Jekyll 或 GitHub Actions 自定义工作流。

已登录 GitHub CLI 时，可在本目录运行：

```sh
gh repo create bianzj/bianzj.github.io --public --source=. --remote=origin --push
gh api --method POST repos/bianzj/bianzj.github.io/pages -f 'source[branch]=main' -f 'source[path]=/'
```

首次发布前应先确认仓库不存在，避免覆盖已有个人网站。

## 内容来源

- 用户在本次对话中确认的研究定位：TIRT 为辐射传输机理模型；LS4T 为温度产品算法；STREAM 对应遥感数字孪生研究与应用；STREAM Studio 为软件入口，计划加入 TIRT 和 LS4T。
- 实验室个人主页：https://www.slrss.cn/kydw/fyjyfjs/202502/t20250218_402577.html
- 2026 年院所会议通知中的单位和职称：https://www.aircas.cas.cn/tzgg/202608/t20260805_8259259.html
- 本地中英文简历：教育经历及学术背景。仅抽取公开学术信息，未上传原始简历。
- 论文以用户指定的“文章专著/全文”目录为主要来源，逐篇核对作者、题名与 DOI，并用 Crossref 补齐正式发表年份、卷期与页码。当前收录 25 篇本人参与的论文，按辐射建模、温度反演、数字孪生分组，每组先展示问题与研究进展，再列可折叠的代表性论文；数字孪生分类包含场景仿真、能量平衡耦合和图像生成等相关基础方法。机理示意图和成果图以用户提供的“峨眉山”PPT和七张图片为准；另从已有研究汇报提取两张植被与地形极坐标原图，分别保留原色标，不据此进行跨图定量比较。
- 头像来自上述实验室公开个人主页。

本站展示代表论文，并非完整论文列表。论文总量“SCI 论文40余篇”据用户资料中的 `身份/简历/简介.docx`，本页代表性论文选列25篇；授权发明专利按用户指定“材料/专利”目录的证书号去重，共9项，其中第一发明人5项，最新一项授权于2026-02-24。不收录出生日期、手机号码、政治面貌或家庭信息。没有将计划中的软件集成写成已经发布的功能。
