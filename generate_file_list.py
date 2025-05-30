import os
import json
from datetime import datetime

def generate_file_list(dirs):
    data = {}
    for dir_name in dirs:
        dir_path = os.path.join(os.getcwd(), dir_name)
        files = []
        for f in os.listdir(dir_path):
            if f.endswith(".html"):
                path = os.path.join(dir_path, f)
                mtime = os.path.getmtime(path)
                files.append({
                    "name": os.path.splitext(f)[0],
                    "path": f"{dir_name}/{f}",
                    "mtime": mtime
                })
        # 按修改时间倒序排序
        files.sort(key=lambda x: x["mtime"], reverse=True)
        data[dir_name] = [{"name": f["name"], "path": f["path"]} for f in files]
    return data

if __name__ == "__main__":
    target_dirs = ["工具", "2D", "3D"]
    result = generate_file_list(target_dirs)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
