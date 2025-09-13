'''
写一个python程序，实现以下功能：
1.当前目录下articles文件夹中有多个包含.md文件的文件夹。当前目录下files文件夹中有与.md文件路径对应的包含图片、视频或音频的文件夹。
2.在结尾插入html把文件夹中的图片、视频或音频文件添加到对应的.md文件，宽度＞高度 的图片不分列， 宽度<高度 的图片在 宽度>=900 的设备设置display=flex，最大宽度450像素，在宽度小于900的设备不分列。音频和视频使用html添加。添加时使用 .md 文件的相对路径，如果.md文件已有重复内容则不添加。
'''
import os
import glob
from PIL import Image

# 支持的媒体文件扩展名
IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
VIDEO_EXTS = ['.mp4', '.webm', '.mov', '.avi']
AUDIO_EXTS = ['.mp3', '.wav', '.ogg', '.m4a']

def generate_media_html(media_dir, md_rel_path):
    """生成媒体文件夹对应的HTML代码，支持竖图分组"""
    media_html = []
    base_dir = os.path.dirname(md_rel_path)
    
    # 获取媒体文件夹中的所有文件并排序
    media_files = sorted(glob.glob(os.path.join(media_dir, '*')))
    
    # 收集连续的竖图分组
    portrait_groups = []
    current_group = []
    
    for file_path in media_files:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # 仅处理图片文件
        if ext in IMAGE_EXTS:
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                
                # 竖图添加到当前分组
                if width <= height:
                    current_group.append(file_path)
                else:
                    # 横图结束当前分组
                    if current_group:
                        portrait_groups.append(current_group)
                        current_group = []
            except Exception as e:
                print(f"Error processing image {file_path}: {e}")
                continue
        else:
            # 非图片文件结束当前分组
            if current_group:
                portrait_groups.append(current_group)
                current_group = []
    
    # 添加最后一个分组
    if current_group:
        portrait_groups.append(current_group)
    
    # 生成媒体文件HTML
    for file_path in media_files:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        rel_path = os.path.relpath(file_path, base_dir).replace('\\', '/')
        
        # 检查是否图片文件
        if ext in IMAGE_EXTS:
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                
                # 检查当前图片是否在竖图分组中
                in_group = False
                for group in portrait_groups:
                    if file_path in group:
                        # 如果是分组中的第一张图片
                        if file_path == group[0]:
                            group_html = []
                            for img_path in group:
                                img_rel_path = os.path.relpath(img_path, base_dir).replace('\\', '/')
                                img_html = f'<img src="{img_rel_path}" style="max-width:100%;">'
                                group_html.append(f'<div class="portrait-item">{img_html}</div>')
                            
                            # 生成整个竖图组的HTML
                            media_html.append(
                                f'<div class="portrait-group">\n' + 
                                '\n'.join(group_html) + 
                                '\n</div>'
                            )
                        in_group = True
                        break
                
                # 如果不是竖图分组中的图片，单独处理
                if not in_group:
                    if width > height:  # 横图
                        img_html = f'<img src="{rel_path}" style="width:100%;">'
                        media_html.append(f'<div class="image-container">{img_html}</div>')
                    else:  # 竖图（但不在分组中，可能是单独一张）
                        img_html = f'<img src="{rel_path}" style="max-width:100%;">'
                        media_html.append(f'<div class="portrait-container">{img_html}</div>')
            except Exception as e:
                print(f"Error processing image {file_path}: {e}")
        
        # 处理视频和音频文件
        elif ext in VIDEO_EXTS:
            video_html = (
                f'<video controls style="width:100%;">'
                f'<source src="{rel_path}" type="video/{ext[1:]}">'
                f'Your browser does not support the video tag.'
                f'</video>'
            )
            media_html.append(f'<div class="media-container">{video_html}</div>')
        
        elif ext in AUDIO_EXTS:
            audio_html = (
                f'<audio controls style="width:100%;">'
                f'<source src="{rel_path}" type="audio/{ext[1:]}">'
                f'Your browser does not support the audio element.'
                f'</audio>'
            )
            media_html.append(f'<div class="media-container">{audio_html}</div>')
    
    return '\n\n'.join(media_html)

def update_md_files():
    """更新所有Markdown文件，添加媒体HTML"""
    css_style = '''
<style>
/* 竖图组容器 - 大屏使用flex布局 */
@media (min-width: 900px) {
  .portrait-group {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
  }
  .portrait-item {
    max-width: 450px;
    flex: 1 1 auto;
  }
}

/* 小屏竖图组布局 */
@media (max-width: 899px) {
  .portrait-group {
    display: block;
  }
  .portrait-item {
    margin-bottom: 20px;
  }
}

/* 单独竖图容器 */
.portrait-container {
  margin: 20px 0;
  text-align: center;
}

/* 横图和媒体容器 */
.image-container, .media-container {
  margin: 20px 0;
}

/* 确保图片在容器内正确缩放 */
img {
  max-width: 100%;
  height: auto;
  display: block;
}
</style>
'''

    # 遍历articles目录中的所有Markdown文件
    for md_path in glob.glob('articles/**/*.md', recursive=True):
        # 获取相对路径（不带扩展名）
        rel_path = os.path.splitext(os.path.relpath(md_path, 'articles'))[0]
        media_dir = os.path.join('files', rel_path)
        
        # 检查对应的媒体文件夹是否存在
        if not os.path.isdir(media_dir):
            print(f"Media directory not found: {media_dir}")
            continue
            
        # 生成媒体HTML
        media_html = generate_media_html(media_dir, md_path)
        if not media_html:
            print(f"No media found in: {media_dir}")
            continue
            
        # 添加CSS样式
        full_html = f'\n<!-- AUTO-GENERATED MEDIA -->\n{css_style}\n{media_html}'
        
        # 读取Markdown文件内容
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已包含相同内容
        if '<!-- AUTO-GENERATED MEDIA -->' in content:
            parts = content.split('<!-- AUTO-GENERATED MEDIA -->', 1)
            existing_content = parts[0].rstrip('\n')
            new_content = existing_content + full_html
        else:
            if content and not content.endswith('\n'):
                content += '\n'
            new_content = content + full_html
        
        # 写回文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'Updated: {md_path}')

if __name__ == '__main__':
    update_md_files()
