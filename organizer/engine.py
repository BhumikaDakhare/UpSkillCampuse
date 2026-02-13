import os
import shutil
from pathlib import Path
from .config import FILE_CATEGORIES, DEFAULT_FOLDER

def organize_directory(target_path, recursive=False, progress_callback=None):
    directory = Path(target_path)
    move_history = [] 
    
    if not directory.is_dir():
        return move_history

    # Collect files first to determine total count for progress bar
    items = [f for f in (directory.rglob("*") if recursive else directory.iterdir()) 
             if f.is_file() and f.name != "main.py"]
    
    total_files = len(items)
    
    for index, item in enumerate(items):
        file_ext = item.suffix.lower()
        dest_folder_name = DEFAULT_FOLDER
        
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                dest_folder_name = category
                break
        
        dest_path = directory / dest_folder_name
        dest_path.mkdir(exist_ok=True)
        
        try:
            target_file_path = dest_path / item.name
            shutil.move(str(item), str(target_file_path))
            move_history.append((str(target_file_path), str(item)))
            
            if progress_callback:
                # Calculate percentage
                progress = (index + 1) / total_files
                progress_callback(progress)
        except Exception:
            continue

    return move_history

def undo_changes(history):
    success_count = 0
    fail_count = 0
    for current_path, original_path in reversed(history):
        try:
            shutil.move(current_path, original_path)
            success_count += 1
        except Exception:
            fail_count += 1
    return success_count, fail_count    