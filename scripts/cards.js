document.addEventListener('DOMContentLoaded', () => {
    // 加载Markdown内容
    const cards = document.querySelectorAll('.card[data-md]');
    cards.forEach(card => {
        const mdFile = card.dataset.md;
        fetch(mdFile)
            .then(response => response.text())
            .then(text => {
                card.innerHTML = `
                    <div class="markdown-content">
                        ${marked.parse(text)}
                    </div>
                `;
            })
            .catch(() => {
                card.innerHTML = `<div class="loading-indicator">内容加载失败</div>`;
            });
    });

    // 卡片点击处理
    document.querySelector('.article-card').addEventListener('click', () => {
        window.open('articles.html', '_blank');
    });

    document.querySelector('.pages-card').addEventListener('click', () => {
        window.open('pages.html', '_blank');
    });
});
