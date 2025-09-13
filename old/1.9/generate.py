import os
import json
import time

def get_file_info(path):
    return {
        "name": os.path.basename(path),
        "path": path,
        "ctime": time.ctime(os.path.getctime(path)),
        "mtime": time.ctime(os.path.getmtime(path))
    }

def generate_structure():
    structure = {"articles": {}, "pages": {}}
    
    # Process articles
    articles_root = "articles"
    for root, dirs, files in os.walk(articles_root):
        rel_path = os.path.relpath(root, articles_root)
        if rel_path == ".":
            continue
            
        category = "pinned" if "pinned" in rel_path else rel_path
        structure["articles"].setdefault(category, [])
        
        for f in sorted(files, key=lambda x: os.path.getctime(os.path.join(root, x)), reverse=True):
            if f.endswith(".md"):
                structure["articles"][category].append(
                    get_file_info(os.path.join(root, f))
                )
    
    # Process pages
    pages_root = "pages"
    for root, dirs, files in os.walk(pages_root):
        rel_path = os.path.relpath(root, pages_root)
        if rel_path == ".":
            continue
            
        structure["pages"].setdefault(rel_path, [])
        for f in sorted(files, key=lambda x: os.path.getctime(os.path.join(root, x)), reverse=True):
            if f.endswith(".html"):
                structure["pages"][rel_path].append(
                    get_file_info(os.path.join(root, f))
                )
    
    # Sort article categories (pinned first, then year-month descending)
    sorted_articles = {}
    if "pinned" in structure["articles"]:
        sorted_articles["pinned"] = sorted(
            structure["articles"]["pinned"],
            key=lambda x: os.path.getctime(os.path.join(articles_root, "pinned", x["name"])),
            reverse=True
        )
    
    # 获取除pinned外的所有键，按年月倒序排序
    other_keys = sorted(
        [k for k in structure["articles"] if k != "pinned"],
        key=lambda x: (int(x[:4]), int(x[4:])),  # 按年份和月份排序
        reverse=True
    )
    
    for key in other_keys:
        sorted_articles[key] = sorted(
            structure["articles"][key],
            key=lambda x: os.path.getctime(os.path.join(articles_root, key, x["name"])),
            reverse=True
        )
    
    structure["articles"] = sorted_articles
    
    with open("data/structure.json", "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_structure()
