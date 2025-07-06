## Willian7004的博客

这是我把博客正式迁到web的项目，只保留原博客项目的部分内容，具体包含[New Blog](https://willian7004-new-blog.streamlit.app/)的动态文章（在本项目为置顶文章）以及从[Media Blog](https://willian7004-media-blog.streamlit.app/)选取背景（横屏背景使用Hidream i1 full生成，竖屏背景使用Cosmos Predict2生成），以上两个项目部署在[Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)，后续也会保留。

在本页面点击右上角"相册模式"按钮可进入背景浏览模式，通过滑块选择具体的背景，背景根据横竖屏自动切换，点击另外两个卡片在新标签页打开对应页面。竖屏使用侧边栏可能默认折叠，要在展开后选择文章。

资源方面，为了方便编辑，本项目使用markdown编写文章，存储在articles文件夹，其中置顶文章在pinned文件夹。网页存储在pages文件夹，暂时只使用单文件。背景存储在backgrounds文件夹。由于跨仓库请求有速率限制，选择在本仓库files文件夹存储文章。

程序方面，index.html、articles.html和pages.html分别对应首页、文章和网页页面，css文件位于styles文件夹，js文件位于scripts文件夹。引入了marked.min.js用于markdown解析，也放到scripts文件夹。

在html内容以外，本项目包含两个python程序。generate.py用于在添加或移除文章/网页后生成列表。add_media.py用于把名称对应的文件夹的媒体内容添加到markdown文件，使用内嵌html页面实现响应式设计，适用于把媒体文件放到文章末尾的需求，其它布局不使用同名文件夹并手动添加。

本项目使用Deepseek R1 0528编写，手动修改了不少css。在功能上，如果要实现更复杂的功能，还是要等下一代模型。

更多项目见[博客项目中的相应文件](https://github.com/Willian7004/new-blog/blob/main/dynamic/%E6%88%91%E7%9A%84%E7%BC%96%E7%A8%8B%E6%8A%80%E6%9C%AF%E6%A0%88.md)。

如需查看源码请前往[本项目地址](https://github.com/Willian7004/Willian7004.github.io)，生成网页的提示词在对应的html文件顶部。
