import os
import string
import shutil

def remove_punctuation(text):
    punctuations = set(string.punctuation)
    punctuations.add("\n")
    punctuations.add("\t")
    #punctuations.remove(" ")  
    return "".join([c for c in text if c not in punctuations])

def get_tokens(dir_path):
    files_input = os.listdir(dir_path)
    files_filtered_list = [file for file in files_input if file[-4:] == ".txt"]
    net_list = []

    for i in files_filtered_list:
        with (open(i)) as f:
            r = remove_punctuation(f.read()).split()
            net_list.append(r)

    return net_list

def insert_file(path_doc, target_dir):
    shutil.move(path_doc, target_dir)

def delete_file(target_dir, file_name):
    full_path = os.path.join(target_dir, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print("file doesn't exist")