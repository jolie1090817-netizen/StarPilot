#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檔案整理工具：按文件類型分類
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def organize_files(source_dir):
    """整理檔案按類型分類"""
    
    source_path = Path(source_dir)
    
    # 定義檔案類型映射
    file_categories = {
        '文件': ['.pdf', '.docx', '.doc'],
        '圖片': ['.jpg', '.jpeg', '.png'],
        '影片': ['.mp4', '.avi', '.mov'],
    }
    
    # 建立分類資料夾
    print("📁 建立分類資料夾...")
    for category in file_categories.keys():
        category_path = source_path / category
        category_path.mkdir(exist_ok=True)
        print(f"  ✓ 建立: {category}/")
    
    # 統計要移動的檔案
    file_stats = defaultdict(list)
    unmoved_files = []
    
    print("\n📋 掃描檔案...")
    for file_path in source_path.iterdir():
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            moved = False
            
            # 找出檔案所屬的分類
            for category, extensions in file_categories.items():
                if file_ext in extensions:
                    file_stats[category].append(file_path.name)
                    moved = True
                    break
            
            if not moved:
                unmoved_files.append(file_path.name)
    
    # 移動檔案
    print("\n🚚 移動檔案...\n")
    total_moved = 0
    
    for category, files in file_categories.items():
        category_path = source_path / category
        moved_count = 0
        
        for file_name in file_stats[category]:
            src = source_path / file_name
            dst = category_path / file_name
            
            try:
                shutil.move(str(src), str(dst))
                print(f"  ✓ {file_name} → {category}/")
                moved_count += 1
                total_moved += 1
            except Exception as e:
                print(f"  ✗ 失敗: {file_name} ({e})")
        
        if moved_count > 0:
            print(f"  {category}: 已移動 {moved_count} 個檔案\n")
    
    # 顯示未分類的檔案
    if unmoved_files:
        print("⚠️  未分類的檔案（保留在原位置）:")
        for file_name in unmoved_files:
            print(f"  - {file_name}")
    
    print(f"\n✅ 完成！共移動 {total_moved} 個檔案")
    
    # 顯示最終結構
    print("\n📂 最終結構:")
    for category in sorted(file_categories.keys()):
        category_path = source_path / category
        if category_path.exists():
            files = list(category_path.glob('*'))
            print(f"\n  📁 {category}/ ({len(files)} 個檔案)")
            for f in sorted(files):
                print(f"     - {f.name}")

if __name__ == '__main__':
    source_directory = '/workspaces/StarPilot/examples/01_檔案整理/測試資料_待整理'
    organize_files(source_directory)
