# 卞尊健 Zunjian Bian

科研个人主页：https://bianzj.github.io/ 。支持中英文切换、研究进展分方向展示，以及打印简历。首页个人简介后展示成果统计与科研项目概况；代表性论文与授权发明专利集中放在研究方向后的独立板块，可分别折叠，打印时自动展开。每个方向采用左侧机理示意、右侧成果图的布局，图片点击可查看原图；辐射建模左侧可切换植被结构和复杂场景示意，右侧可切换植被和地形验证；温度反演左侧可切换方法示意与热成像，右侧可切换温度产品和精度验证；数字孪生左侧可切换耦合示意与 Landsat 空间对比，右侧可切换 StreamSensor 系统和分地类精度。桌面端采用等宽双栏和统一图框，平板与手机端上下排列，原图保持比例并可点击查看。三组示意图和成果图使用用户提供的原图，保留色标、坐标和图内标注，图片位于 `assets/research/`。纯静态页面，无第三方字体、分析跟踪或前端构建依赖。

## STREAM Studio 软件案例页

独立页面 `stream.html` 展示 STREAM Studio 软件案例。案例001为“STREAM案例 | 作物光热转换的物理桥梁”，展示玉米场景1—4、中央九株的温度/PAR/H/LE、光热垂直剖面及Vcmax响应，包含五张实际模拟图、JAG与RSE论文链接及案例库Word下载。该案例为数值模拟，尚非逐日连续全生长季计算，也未进行独立观测验证。主页导航、简介按钮和科研软件板块均提供跳转入口；两页共享中英文选择。页面配置位于 `stream_cases.json`，由 `build_cases.py` 生成，运行 `python3 build.py` 会同时更新两个页面。

案例图片位于 `assets/research/maize/`，文档位于 `assets/documents/streamstudio-case-library.docx`。当前收录001—005；在 `stream_cases.json` 中维护编号、双语说明、图片、论文及文档链接。

案例002为“STREAM案例 | 穿透树冠，从上到下读懂雨林的光与热”，展示七类植被的三维雨林、四波段方向反射率、垂直光热剖面与0—24点叶温。图片位于 `assets/research/rainforest/`，直达链接：https://bianzj.github.io/stream.html#rainforest-light-heat 。Word案例库已包含001和002。案例002为理想化场景与合成气象，尚无独立观测验证，全天叶温试验未开启流体。

案例003为城市街区浅色屋面与增加绿化，采用2026-11-05 v2修订的五张图及当前PDF，入口为 `stream.html#urban-cooling`。案例004为延庆山地光热与风场，包含真实地形、中心2×2km的原生流体空气温度和风场、坡向热响应，以及最后的站点足迹图，入口为 `stream.html#yanqing-terrain-wind`。两例均保留结果适用范围，未完成独立观测验证。工程与输入链接指向StreamStudio仓库，网站自身只托管图文展示和报告，不托管完整历史计算输出。

顶部提供四例图文入口、GitHub程序与工程、百度网盘及提取码；Word总册已更新，城市案例请以单独的v2 PDF为准。

## 更新内容

编辑 `profile.json`，然后运行：

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器打开 http://127.0.0.1:8765 。修改样式请编辑 `assets/site.css`，交互逻辑位于 `assets/site.js`。

## 发布与长期维护

- 主页：https://bianzj.github.io/
- STREAM Studio 软件案例：https://bianzj.github.io/stream.html
- 源码仓库：https://github.com/bianzj/bianzj.github.io
- 网站设置：https://github.com/bianzj/bianzj.github.io/settings/pages

网站由 GitHub Pages 托管，使用 `main` 分支根目录发布。访问网站不依赖本地电脑或本地预览服务。页面为静态 HTML/CSS/JavaScript，没有服务器进程、数据库或前端依赖需要常驻运行。保留仓库名称和 Pages 配置，可沿用上述地址；每次推送 `main` 后会自动重新部署。

日常修改个人资料使用 `profile.json`；软件案例配置使用 `stream_cases.json`。编辑后运行 `python3 build.py`，本地预览确认，再提交并推送：

```sh
python3 build.py
git diff --check
git add profile.json stream_cases.json build.py build_cases.py index.html stream.html assets README.md
git commit -m "Update website content"
git push origin main
```

换电脑时，可从 GitHub 克隆仓库继续维护：

```sh
git clone https://github.com/bianzj/bianzj.github.io.git
cd bianzj.github.io
python3 build.py
```

仓库保留修改历史。通过 Pages 设置和仓库 Actions 查看部署状态；需要恢复旧内容时，可撤销对应提交后推送。

## 内容来源

- 用户在本次对话中确认的研究定位：TIRT 为辐射传输机理模型；LS4T 为温度产品算法；STREAM 对应遥感数字孪生研究与应用；STREAM Studio 为软件入口，计划加入 TIRT 和 LS4T。
- 实验室个人主页：https://www.slrss.cn/kydw/fyjyfjs/202502/t20250218_402577.html
- 2026 年院所会议通知中的单位和职称：https://www.aircas.cas.cn/tzgg/202608/t20260805_8259259.html
- 本地中英文简历：教育经历及学术背景。仅抽取公开学术信息，未上传原始简历。
- 论文以用户指定的“文章专著/全文”目录为主要来源，逐篇核对作者、题名与 DOI，并用 Crossref 补齐正式发表年份、卷期与页码。已核对的25篇论文条目集中列在独立成果板块，不再附在各研究方向之后；数字孪生分类包含场景仿真、能量平衡耦合和图像生成等相关基础方法。机理示意图和成果图以用户提供的“峨眉山”PPT和本次提供的图片为准；地形场景仅保留山谷、山脊、山峰的模型误差与地形组合图。
- 头像来自上述实验室公开个人主页。

成果统计和项目概况以用户于2026-10-31在本次对话中确认的信息为准：SCI论文48篇，第一/通讯作者22篇，中国科学院一区/TOP刊物17篇，专著1部，谷歌学术引用1400余次；主持国家自然科学基金2项、省部级项目3项，参与国家自然科学基金委重点项目2项、国家重点研发项目2项及高分辨率对地观测重大专项等。授权发明专利按用户指定“材料/专利”目录的证书号去重，共9项，其中第一发明人5项，与用户更新一致。不收录出生日期、手机号码、政治面貌或家庭信息。没有将计划中的软件集成写成已经发布的功能。


案例目录按一行一个案例展示小图、编号、短标题和说明，桌面与手机均可点击整行跳转。新增005“光伏草场热环境”，使用三张已有推广图及3页PDF，分别说明基础1 m网格与0.25 m空间补算；没有进行新的模型计算。更新配置后运行 `python -X utf8 build.py`。
