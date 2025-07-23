## Willian7004的博客

#### 功能

这是我把博客正式迁到web的项目，只保留原博客项目的部分内容，具体包含[New Blog](https://willian7004-new-blog.streamlit.app/)的动态文章（在本项目为置顶文章）以及从[Media Blog](https://willian7004-media-blog.streamlit.app/)选取的背景（横屏背景使用Hidream i1 full生成，竖屏背景使用Cosmos Predict2生成），以上两个项目部署在[Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)，后续也会保留。

本项目迭代到2.0版本，首页卡片使用2*2布局以避免不同列高度不一致（竖屏设备使用纵向布局）。其它页面使用带高斯模糊的侧边栏与正文iframe分屏显示的形式从而平衡外观、可读性和空间利用率表现。侧边栏有折叠、大小调整和选中项高亮和在新标签页打开相应页面的功能。

“文章”

#### 目录结构

本项目index.html包含首页内容，content.html为展示页。

资源方面，为了方便编辑，本项目使用markdown编写文章，存储在articles文件夹。使用单文件的网页存储在pages文件夹。projects文件夹存储多文件的网页。cards.json存储首页卡片内容。背景存储在backgrounds文件夹。由于跨仓库请求有速率限制，选择在本仓库files文件夹存储媒体文件。

在html内容以外，本项目包含两个python程序。generate.py用于在添加或移除文章/网页后生成列表。add_media.py用于把名称对应的文件夹的媒体内容添加到markdown文件，使用内嵌html页面实现响应式设计，适用于把媒体文件放到文章末尾的需求，其它布局不使用同名文件夹并手动添加。

另外，创建了libs文件夹保存库文件以避免重复加载。

本项目当前版本前期使用Kimi K2编写，后面使用

更多项目见[本项目中的相应文件](https://github.com/Willian7004/Willian7004.github.io/blob/main/articles/pinned/%E6%88%91%E7%9A%84%E7%BC%96%E7%A8%8B%E6%8A%80%E6%9C%AF%E6%A0%88.md)。

如需查看源码请前往[本项目地址](https://github.com/Willian7004/Willian7004.github.io)，生成网页的提示词在对应的html文件顶部。
