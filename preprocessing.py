import os
import string
import shutil
from typing import Dict, List

def remove_punctuation(text: str) -> str:
    punctuations = set(string.punctuation)
    punctuations.add("\n")
    punctuations.add("\t")
    #punctuations.remove(" ")  
    return "".join([c for c in text if c not in punctuations])

def only_txt_files(files_list: List[str]) -> List[str]:
    filtered_list = [file for file in files_list if file[-4:] == ".txt"]
    return filtered_list

def get_tokens(dir_path: str) -> Dict[str,str]:
    files_input = os.listdir(dir_path)
    files_filtered_list = only_txt_files(files_input)
    doc_tokens = {key: None for key in files_filtered_list}

    for i in files_filtered_list:
        file_path = os.path.join(dir_path, i)
        with open(file_path) as f:
            r = remove_punctuation(f.read().replace("\n"," ")).split()
            # take r and add them as values to each doc
            doc_tokens[i] = r 

    return doc_tokens

def insert_file(path_doc: str, target_dir: str) -> None:
    shutil.move(path_doc, target_dir)

def delete_file(target_dir: str, file_name: str) -> None:
    full_path = os.path.join(target_dir, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print("file doesn't exist")

def map_documents(target_dir: str) -> Dict[str, str]:
    documents_table = {}
    files_input = os.listdir(target_dir) # List of all documents
    filtered = only_txt_files(files_input)
    for i in filtered:
        file_path = os.path.join(target_dir, i)  # Create full path
        with open(file_path) as f:  # Use full path
            file_text = f.read()
            cleaned_text = remove_punctuation(file_text)
            documents_table[i] = cleaned_text  # Correct dictionary assignment
    
    return documents_table

