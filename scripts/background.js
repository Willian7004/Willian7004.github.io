// 初始化背景
function initBackground() {
    const bgContainer = document.getElementById('background-container');
    let currentOrientation = getOrientation();

    function updateBackground() {
        const orientation = getOrientation();
        if (orientation !== currentOrientation) {
            currentOrientation = orientation;
            setRandomBackground();
        }
    }

    window.addEventListener('resize', updateBackground);
    setRandomBackground();
}

function getOrientation() {
    return window.innerWidth > window.innerHeight ? 'horizontal' : 'vertical';
}

function setRandomBackground() {
    const orientation = getOrientation();
    const bgCount = orientation === 'horizontal' ? 93 : 90; // 根据实际文件数量调整
    const randomNum = Math.floor(Math.random() * bgCount) + 1;
    const bgPath = `backgrounds/${orientation}/${randomNum}.jpg`;
    
    document.getElementById('background-container').style.backgroundImage = 
        `url('${bgPath}')`;
}

// 初始化
document.addEventListener('DOMContentLoaded', initBackground);
