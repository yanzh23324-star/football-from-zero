# 第一脚 · 从零开始踢足球

## 👉 [打开网站](https://yanzh23324-star.github.io/football-from-zero/)

中文足球入门手册，面向第一次接触足球、刚开始参加约球的人。无需登录。

**这是独立多页面网站**，不是单页长文章。首页 → 六大板块 → 每课一个独立网址；共24篇首版课程，另有课程搜索、入门路线、学习记录和来源库。

- 认识足球：目标、场地标线、重开、越位、犯规。
- 赛制与规则：五/七/八/十一人对比、futsal与普通五人、约球规则。
- 第一次上场：装备与第一次约球。
- 基础技术：停、传、带、射与接球前观察。
- 跑位与配合：接应、传后移动、宽度纵深、保护、转换和位置。
- 训练与复盘：独练、双人练习和赛后复盘。

## 实现与费用

纯静态 HTML/CSS/JavaScript，Python 标准库生成页面，GitHub Pages + 标准 GitHub Actions runner 发布，不租服务器、不用付费 API。多页面不会按页计费，仍遵守 GitHub Pages 的体积、带宽和使用政策。

收藏、已读记录和复盘仅存于当前浏览器 `localStorage`，不会上传。不同设备和不同浏览器不自动同步；提供导出笔记功能。

## 维护和扩充

- `content/lessons.json`：所有课程与参考来源。
- `scripts/build.py`：生成器，输出35个初版 HTML 页面及公共资源。
- `assets/style.css`、`assets/app.js`：视觉与交互。
- `scripts/check.py`：核对所有内部链接、锚点、课程ID、来源及测验数据。
- `.github/workflows/deploy.yml`：每次默认分支更新时构建、检查并发布。
- `site/`：构建结果，未提交到 Git，避免生成文件和内容源不一致。

新增选题时在制作对话中提出，先研究和核验再编辑 `content/lessons.json`，提交后自动生成独立课程、加入目录/搜索/板块页。可以在新对话附上此仓库链接继续维护。课程不由定时抓取自动发布。

添加课程对象需含：`id`、`title`、`category`、`lead`、`sections`（title/text）、`takeaway`、`practice`、`quiz`（question/options/answer/explanation）、`sources`（title/url）。category 为 start/formats/matchday/skills/tactics/practice，id 使用唯一英文短横线形式。answer 是从0开始的选项序号。

## 本地运行

Python 3.9+：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory site
```

打开 http://localhost:8000/ 。点击板块和课程会打开新的 HTML 页面，每页从顶部开始，支持浏览器前进/后退与直接收藏。

## 编辑原则

独立学习资料站，非FIFA、IFAB或足协官方网站。正文为原创中文整理，优先依据 IFAB、FIFA Training Centre、England Football Learning 等官方规则与教学来源；每课列出原始链接，核验日期2026-10-27。练习和球场图是本站入门改编，不等于来源中的原始训练处方。

区分赛制和实际活动规程：人数包含门将，七/八人不假定全球统一规则，正式 futsal 不等于所有五人活动；战术图只演示可能选择，具体分工需与队友协调。已读记录不是能力评价。新增题目经研究、核验后编辑发布，不把自媒体搜索结果直接当课程。
