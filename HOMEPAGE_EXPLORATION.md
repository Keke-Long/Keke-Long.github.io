# 首页设计探索版备份

这是用户要求单独保存的首页探索版，不替换当前已定稿版本，也不自动纳入 2027 年 1 月的上线计划。

- 本分支：`homepage-exploration`
- 当前定稿分支：`redesign-2027`
- 现有公开网站：`main`
- 独立预览：https://keke-long-home-exploration.keke-long-re-5174.chatgpt.site
- 当前定稿预览：https://keke-long-lab-2027.keke-long-re-5174.chatgpt.site

## 文件

- `home-design.css`：仅用于探索版首页的样式。
- `site/build_home_exploration.py`：首页布局变换，保留全部可见文字、关键词、研究图片和链接。
- `site/build.py`：生成全部页面后，自动应用上述首页设计。
- `site/content.json`：沿用定稿版本的内容。
- `index.html` 与 `dist/index.html`：已生成的探索版首页。
- 所有图片、其他页面及资源均随分支保存。

运行 `python site/build.py` 即可重新生成本分支预览。用静态服务器提供 `dist/` 即可浏览完整网站。不要仅通过双击 HTML 文件预览，因为链接使用站点根路径。

`.openai/hosting.json` 指向独立首页探索 Site，不指向已定稿 Site。预览访问权限没有改变。本次仅备份 GitHub 源码，没有重新部署或覆盖任一网页。

此备份源自独立预览的 a11bfdcf2dad83a7fd9f8e99a3239afcf3b09e25，基于定稿 a0e0264288d56b2386335667ca9d296b4b3c3f3b。生成的整个 dist/ 应与独立预览逐文件一致。
