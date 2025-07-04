## 在Github Pages创建博客的感受

我之前使用Streamlit创建博客并使用Streamlit Community Cloud部署。之前在Github Pages展示网页项目，今天正式引入博客内容。两个方案各有优势。

Streamlit的优势：
1. 总容量限制50g，虽然程序占用一部分，但也可以使用多个仓库进行部署更大的项目。总流量也没有明显限制。
2. 有较完善的外观和响应式设计，能够开箱即用。使用LLM编写也相对简单。
3. 使用Python编写，可以实现一些后端功能。

Github Pages（静态网页）的优势：
1. 可自由选择库文件，外观和功能自由度较高。
2. 静态网页形式资源占用低，加载快，也不受无访问时的运行时间限制。
3. 知名度高，对于分享和SEO等更为友好。

编写网页对LLM要求高一些。我深入使用Deepseek R1 0528后才决定编写这一项目，编写时除了提出修改要求外，还手动修改了不少css。如果要达到更完善的网页创作体验，可能还是要等下一代模型。