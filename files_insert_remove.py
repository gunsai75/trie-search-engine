import shutil
import os

def insert_file(path_doc, target_dir):
    shutil.move(path_doc, target_dir)

def delete_file(target_dir, file_name):
    full_path = os.path.join(target_dir, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print("file doesn't exist")