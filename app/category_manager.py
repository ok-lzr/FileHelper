"""管理分类JSON文件的读写"""

import os
import json
from datetime import datetime

class CategoryManager:
    def __init__(self, base_dir="classes"):
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.base_dir = os.path.join(project_root, base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
    
    def get_category_path(self, category_name):
        return os.path.join(self.base_dir, f"{category_name}.json")
    
    def create_category(self, category_name):
        file_path = self.get_category_path(category_name)
        if os.path.exists(file_path):
            return False
        
        category_data = {
            "name": category_name,
            "files": [],
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": ""
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(category_data, f, ensure_ascii=False, indent=2)
        return True
    
    def load_category_data(self, category_name):
        file_path = self.get_category_path(category_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_category_data(self, category_name, data):
        file_path = self.get_category_path(category_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def rename_category(self, old_name, new_name):
        old_path = self.get_category_path(old_name)
        new_path = self.get_category_path(new_name)
        
        if not os.path.exists(old_path) or os.path.exists(new_path):
            return False
        
        with open(old_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['name'] = new_name
        data['renamed_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        os.remove(old_path)
        return True
    
    def delete_category(self, category_name):
        file_path = self.get_category_path(category_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def add_file_to_category(self, category_name, file_path):
        data = self.load_category_data(category_name)
        if data is None:
            return False
        
        for file_info in data['files']:
            if file_info['path'] == file_path:
                return False
        
        file_info = {
            "path": file_path,
            "name": os.path.basename(file_path),
            "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": os.path.splitext(file_path)[1] if os.path.splitext(file_path)[1] else "无后缀",
            "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        
        data['files'].append(file_info)
        self.save_category_data(category_name, data)
        return True
    
    def remove_file_from_category(self, category_name, file_path):
        data = self.load_category_data(category_name)
        if data is None:
            return False
        
        data['files'] = [f for f in data['files'] if f['path'] != file_path]
        self.save_category_data(category_name, data)
        return True
    
    def load_categories(self):
        categories = []
        if os.path.exists(self.base_dir):
            for filename in os.listdir(self.base_dir):
                if filename.endswith('.json'):
                    category_name = filename[:-5]
                    categories.append(category_name)
        return sorted(categories)