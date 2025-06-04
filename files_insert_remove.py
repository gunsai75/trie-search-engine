import shutil
import os
import preprocessing
import trie

def form_trie(target_dir):
    forward_index = preprocessing.get_tokens(target_dir)
    for doc in forward_index:
        word_list = forward_index[doc]
        trie.trie.insert_from_document(word_list, doc)

def insert_file(path_doc, target_dir):
    shutil.move(path_doc, target_dir)
    # trie formation
    form_trie(target_dir)

def delete_file(target_dir, file_name):
    full_path = os.path.join(target_dir, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
        form_trie(target_dir)   # forming a new trie
    else:
        print("file doesn't exist")