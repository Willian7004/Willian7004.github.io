'''
写一个python程序，实现以下功能：
1.当前目录下articles文件夹中有多个包含.md文件的文件夹。当前目录下files文件夹中有与.md文件路径对应的包含图片、视频或音频的文件夹。
2.在结尾插入html把文件夹中的图片、视频或音频文件添加到对应的.md文件，宽度＞高度 的图片不分列， 宽度<高度 的图片分3列显示，每列宽度400像素。音频和视频使用html添加。如果.md文件已有重复内容则不添加。添加时把路径转换为 https://github.com/Willian7004/Willian7004.github.io 仓库中的相应路径并使用raw=true 加载文件。
'''
import os
import glob
from PIL import Image

# 配置参数
ARTICLES_DIR = 'articles'
FILES_DIR = 'files'
REPO_BASE = 'https://github.com/Willian7004/Willian7004.github.io/raw/main/'
IMAGE_COLUMNS = 3
COLUMN_WIDTH = 400

def get_media_html(media_path, rel_path):
    """生成媒体文件的HTML代码"""
    ext = os.path.splitext(media_path)[1].lower()
    github_path = REPO_BASE + rel_path.replace('\\', '/') + '?raw=true'
    
    # 图片处理
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        try:
            with Image.open(media_path) as img:
                width, height = img.size
                if width > height:  # 横图不分列
                    return f'<img src="{github_path}" style="max-width:100%;height:auto;"/>'
                else:  # 竖图分列显示
                    return f'<img src="{github_path}" style="max-height:90%;display: flex; justify-content: center;"/>'
        except:
            return f'<img src="{github_path}" style="max-width:100%;height:auto;"/>'
    
    # 视频处理
    elif ext in ['.mp4', '.webm', '.mov']:
        return f'''
        <video controls style="max-width:100%;">
            <source src="{github_path}" type="video/{ext[1:]}">
            Your browser does not support the video tag.
        </video>
        '''
    
    # 音频处理
    elif ext in ['.mp3', '.wav', '.ogg']:
        return f'''
        <audio controls style="width:100%;">
            <source src="{github_path}" type="audio/{'mpeg' if ext == '.mp3' else ext[1:]}">
            Your browser does not support the audio element.
        </audio>
        '''
    
    return ''

def process_markdown_files():
    """处理所有Markdown文件"""
    for md_file in glob.glob(os.path.join(ARTICLES_DIR, '**', '*.md'), recursive=True):
        # 获取相对路径和对应的媒体文件夹
        rel_path = os.path.relpath(os.path.dirname(md_file), ARTICLES_DIR)
        media_dir = os.path.join(FILES_DIR, rel_path, os.path.splitext(os.path.basename(md_file))[0])
        
        if not os.path.exists(media_dir):
            continue
        
        # 读取Markdown内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 收集所有媒体文件HTML
        media_html = []
        for media_file in glob.glob(os.path.join(media_dir, '*')):
            rel_media_path = os.path.relpath(media_file, start='.')
            media_rel = os.path.relpath(media_file, os.path.dirname(md_file))
            html_snippet = get_media_html(media_file, rel_media_path)
            
            # 检查是否已存在相同内容
            if html_snippet and html_snippet not in content:
                media_html.append(html_snippet)
        
        if not media_html:
            continue
        
        # 分组处理竖图
        vertical_images = []
        other_media = []
        for html in media_html:
            if 'display:inline-block;' in html:
                vertical_images.append(html)
            else:
                other_media.append(html)
        
        # 构建分列容器
        columns_html = ''
        if vertical_images:
            columns_html = f'<div style="width:{IMAGE_COLUMNS * COLUMN_WIDTH}px;">'
            for i, img in enumerate(vertical_images):
                if i % IMAGE_COLUMNS == 0 and i != 0:
                    columns_html += '<div style="clear:both;"></div>'
                columns_html += img
            columns_html += '<div style="clear:both;"></div></div>'
        
        # 组合所有HTML
        final_html = '\n\n'.join(other_media + [columns_html]) if columns_html else '\n\n'.join(other_media)
        
        # 更新文件内容
        with open(md_file, 'a', encoding='utf-8') as f:
            f.write('\n\n' + final_html)

if __name__ == '__main__':
    process_markdown_files()
    print("媒体文件添加完成！")