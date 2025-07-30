import os
import json
from pathlib import Path
import time

def get_creation_time(path):
    """获取文件或文件夹的创建时间"""
    try:
        return os.path.getctime(path)
    except:
        return 0

def generate_pages_index():
    """生成pages文件夹的索引"""
    pages_dir = Path("pages")
    if not pages_dir.exists():
        return []
    
    html_files = []
    for file_path in pages_dir.glob("*.html"):
        html_files.append({
            "name": file_path.name,
            "path": str(file_path).replace("\\", "/"),
            "creation_time": get_creation_time(file_path)
        })
    
    # 按创建时间从新到旧排序
    html_files.sort(key=lambda x: x["creation_time"], reverse=True)
    return html_files

def generate_slides_index():
    """生成slides文件夹的索引"""
    slides_dir = Path("slides")
    if not slides_dir.exists():
        return []
    
    folders = []
    for folder_path in slides_dir.iterdir():
        if folder_path.is_dir():
            # 查找文件夹中的HTML文件
            html_files = list(folder_path.glob("*.html"))
            if html_files:
                # 获取文件夹中最大的文件编号
                max_page = 0
                for html_file in html_files:
                    try:
                        # 假设文件名是数字.html格式
                        page_num = int(html_file.stem)
                        max_page = max(max_page, page_num)
                    except ValueError:
                        pass
                
                folders.append({
                    "name": folder_path.name,
                    "path": str(folder_path).replace("\\", "/"),
                    "creation_time": get_creation_time(folder_path),
                    "max_page": max_page
                })
    
    # 按创建时间从新到旧排序
    folders.sort(key=lambda x: x["creation_time"], reverse=True)
    return folders

def main():
    """主函数"""
    index_data = {
        "pages": generate_pages_index(),
        "slides": generate_slides_index()
    }
    
    # 保存索引到文件
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print("索引生成完成！")

if __name__ == "__main__":
    main()
