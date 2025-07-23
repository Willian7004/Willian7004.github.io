#!/usr/bin/env python3
"""
Generate JSON files for the static webpage navigation
"""
import os
import json
from datetime import datetime
from pathlib import Path

def get_file_creation_time(file_path):
    """Get file creation time as ISO format string"""
    try:
        stat = os.stat(file_path)
        # Use modification time as creation time might not be available on all systems
        return datetime.fromtimestamp(stat.st_mtime).isoformat()
    except:
        return datetime.now().isoformat()

def scan_articles():
    """Scan articles folder and return structured data"""
    articles_data = {"pinned": [], "folders": {}}
    
    articles_path = Path("articles")
    if not articles_path.exists():
        return articles_data
    
    # Process pinned folder
    pinned_path = articles_path / "pinned"
    if pinned_path.exists():
        for md_file in sorted(pinned_path.glob("*.md")):
                articles_data["pinned"].append({
                    "name": md_file.stem,
                    "path": str(md_file.relative_to(articles_path)).replace('\\', '/'),
                    "created": get_file_creation_time(md_file)
                })
    
    # Process date folders (202507, etc.)
    for folder in sorted(articles_path.iterdir()):
        if folder.is_dir() and folder.name != "pinned":
            folder_articles = []
            for md_file in sorted(folder.glob("*.md")):
                folder_articles.append({
                    "name": md_file.stem,
                    "path": str(md_file.relative_to(articles_path)).replace('\\', '/'),
                    "created": get_file_creation_time(md_file)
                })
            
            if folder_articles:
                # Sort by creation time (newest first)
                folder_articles.sort(key=lambda x: x["created"], reverse=True)
                articles_data["folders"][folder.name] = folder_articles
    
    return articles_data

def scan_pages():
    """Scan pages folder and return structured data"""
    pages_data = {}
    
    pages_path = Path("pages")
    if not pages_path.exists():
        return pages_data
    
    for category_folder in sorted(pages_path.iterdir()):
        if category_folder.is_dir():
            category_pages = []
            for html_file in sorted(category_folder.glob("*.html")):
                category_pages.append({
                    "name": html_file.stem,
                    "path": str(html_file.relative_to(pages_path)).replace('\\', '/'),
                    "created": get_file_creation_time(html_file)
                })
            
            if category_pages:
                # Sort by creation time (newest first)
                category_pages.sort(key=lambda x: x["created"], reverse=True)
                pages_data[category_folder.name] = category_pages
    
    return pages_data

def scan_projects():
    """Scan projects folder and return structured data"""
    projects_data = []
    
    projects_path = Path("projects")
    if not projects_path.exists():
        return projects_data
    
    for project_folder in sorted(projects_path.iterdir()):
        if project_folder.is_dir():
            has_index = (project_folder / "index.html").exists()
            has_readme = (project_folder / "README.md").exists()
            
            projects_data.append({
                "name": project_folder.name,
                "path": project_folder.name,
                "has_index": has_index,
                "has_readme": has_readme,
                "created": get_file_creation_time(project_folder)
            })
    
    # Sort by creation time (newest first)
    projects_data.sort(key=lambda x: x["created"], reverse=True)
    return projects_data

def generate_all_json():
    """Generate all JSON files"""
    os.makedirs("data", exist_ok=True)
    
    # Generate articles.json
    articles_data = scan_articles()
    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    # Generate pages.json
    pages_data = scan_pages()
    with open("data/pages.json", "w", encoding="utf-8") as f:
        json.dump(pages_data, f, ensure_ascii=False, indent=2)
    
    # Generate projects.json
    projects_data = scan_projects()
    with open("data/projects.json", "w", encoding="utf-8") as f:
        json.dump(projects_data, f, ensure_ascii=False, indent=2)
    
    print("Generated JSON files:")
    print("- data/articles.json")
    print("- data/pages.json")
    print("- data/projects.json")

if __name__ == "__main__":
    generate_all_json()
