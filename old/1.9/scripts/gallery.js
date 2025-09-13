class GalleryMode {
    constructor() {
        this.isActive = false;
        this.currentOrientation = getOrientation();
        this.slider = document.getElementById('bg-slider');
        this.sliderValue = document.getElementById('slider-value');
        this.galleryControls = document.getElementById('gallery-controls');
        this.toggleButton = document.getElementById('gallery-toggle');
        this.cardsContainer = document.querySelector('.cards-container');
        
        // 添加窗口resize监听
        this.resizeHandler = () => this.handleResize();
        window.addEventListener('resize', this.resizeHandler);

        this.init();
    }

    handleResize() {
        const newOrientation = getOrientation();
        if (newOrientation !== this.currentOrientation) {
            this.currentOrientation = newOrientation;
            // 如果处于相册模式则更新滑块设置
            if (this.isActive) {
                const max = this.currentOrientation === 'horizontal' ? 93 : 90;
                this.slider.max = max;
                this.slider.value = Math.min(this.slider.value, max);
                this.updateBackground(this.slider.value);
            }
        }
    }

    init() {
        this.toggleButton.addEventListener('click', () => this.toggleGallery());
        this.slider.addEventListener('input', (e) => this.updateBackground(e.target.value));
    }

    toggleGallery() {
        this.isActive = !this.isActive;
        
        if (this.isActive) {
            // 进入相册模式
            this.cardsContainer.classList.add('hidden');
            this.galleryControls.classList.remove('hidden');
            this.toggleButton.textContent = '退出相册';
            
            // 设置滑块最大值
            const max = this.currentOrientation === 'horizontal' ? 93 : 90;
            this.slider.max = max;
            this.slider.value = 1;
            this.updateBackground(1);
        } else {
            // 退出相册模式
            this.cardsContainer.classList.remove('hidden');
            this.galleryControls.classList.add('hidden');
            this.toggleButton.textContent = '相册模式';
            setRandomBackground(); // 恢复随机背景
        }
    }

    updateBackground(value) {
        this.sliderValue.textContent = value;
        const bgPath = `backgrounds/${this.currentOrientation}/${value}.jpg`;
        document.getElementById('background-container').style.backgroundImage = 
            `url('${bgPath}')`;
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new GalleryMode();
});
