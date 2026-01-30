import os
import shutil

source_dir = os.path.expanduser("/home/username/Desktop/PL/sem6/test_files/")

def sort_files_in_dir(directory):
    print(f"Анализ директории: {directory}...")
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isdir(filepath):
            continue

        _, file_extension = os.path.splitext(filename)
        
        if not file_extension:
            continue
            
        extension = file_extension[1:].lower()
        
        target_folder = os.path.join(directory, extension)
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"Создана директория: {target_folder}")
            
        try:
            shutil.move(filepath, os.path.join(target_folder, filename))
            print(f"Перемещен файл: {filename} -> {extension}/")
        except Exception as e:
            print(f"Ошибка при перемещении {filename}: {e}")

if __name__ == "__main__":
    sort_files_in_dir(source_dir)
    print("Нет файлов, которые можно переместить.")
