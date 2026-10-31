# 卞尊健 Zunjian Bian

科研个人主页，计划发布于 https://bianzj.github.io/ 。支持中英文切换、论文分类及打印简历。纯静态页面，无第三方字体、分析跟踪或前端构建依赖。

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
- 论文题名与 DOI 由 Crossref 元数据核对。
- 头像来自上述实验室公开个人主页。

本站展示代表论文，并非完整论文列表。不使用旧简历中的累计论文或专利数量；不收录出生日期、手机号码、政治面貌或家庭信息。没有将计划中的软件集成写成已经发布的功能。
