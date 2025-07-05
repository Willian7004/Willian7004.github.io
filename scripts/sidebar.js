class Sidebar {
    constructor(type) {
        this.type = type; // 'articles' 或 'pages'
        this.sidebar = document.getElementById('sidebar');
        this.sidebarContent = document.querySelector('.sidebar-content');
        this.toggleButton = document.querySelector('.toggle-button');
        this.mainContent = document.querySelector('.main-content');
        this.data = null;
        
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.renderSidebar();
        this.setupEvents();
        
        // 移动端默认折叠侧边栏
        if (window.innerWidth <= 767) {
            this.sidebar.classList.add('collapsed');
        }
    }
    
    async loadData() {
        const response = await fetch('./data/structure.json'); // 显式使用相对路径
        this.data = await response.json();
    }
    
    renderSidebar() {
        this.sidebarContent.innerHTML = '';
        
        let groups;
        if (this.type === 'articles') {
            // 确保pinned在最前，其他分类按年月倒序
            const articles = {...this.data.articles};
            const pinned = articles.pinned ? [['pinned', articles.pinned]] : [];
            delete articles.pinned;
            
            // 其他分类按键名倒序排列（新的年月在前）
            const other = Object.entries(articles)
                .sort(([a], [b]) => b.localeCompare(a));
            
            groups = pinned.concat(other);
        } else {
            groups = Object.entries(this.data.pages);
        }
        
        groups.forEach(([groupName, files]) => {
            const groupElement = document.createElement('div');
            groupElement.innerHTML = `
                <div class="group-title">${groupName}</div>
            `;
            
                files.forEach(file => {
                    const fileElement = document.createElement('div');
                    fileElement.className = 'file-item';
                    fileElement.dataset.path = file.path;
                    // 去掉文件扩展名显示
                    const fileNameWithoutExt = file.name.replace(/\.[^/.]+$/, "");
                    fileElement.textContent = fileNameWithoutExt;
                    groupElement.appendChild(fileElement);
                });
            
            this.sidebarContent.appendChild(groupElement);
        });
    }
    
    setupEvents() {
        // 切换侧边栏折叠状态
        this.toggleButton.addEventListener('click', () => {
            this.sidebar.classList.toggle('collapsed');
        });
        
        // 文件选择
        this.sidebarContent.addEventListener('click', (e) => {
            if (e.target.classList.contains('file-item')) {
                const filePath = e.target.dataset.path;
                this.showFileContent(filePath);
            }
        });
    }
    
    showFileContent(filePath) {
        if (this.type === 'articles') {
            // 文章页面显示Markdown内容
            fetch(filePath)
                .then(response => response.text())
                .then(text => {
                    document.querySelector('.article-content').innerHTML = `
                        <div class="markdown-content">
                            ${marked.parse(text)}
                        </div>
                    `;
                });
        } else {
            // 网页页面显示iframe
            document.querySelector('.page-frame').src = filePath;
        }
    }
}

// 根据当前页面初始化侧边栏
document.addEventListener('DOMContentLoaded', () => {
    const pageType = document.title.includes('文章') ? 'articles' : 'pages';
    new Sidebar(pageType);
});
