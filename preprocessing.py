import os
import string
import shutil
from typing import Dict, List

def remove_punctuation(text: str) -> str:
    """Remove punctuation, newlines, and tabs from the input text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The text with punctuation, newlines, and tabs removed.
    """
    punctuations = set(string.punctuation)
    punctuations.add("\n")
    punctuations.add("\t")
    # punctuations.remove(" ")  
    return "".join([c for c in text if c not in punctuations])

def only_txt_files(files_list: List[str]) -> List[str]:
    """Filter a list of files to include only those with a .txt extension.

    Args:
        files_list (List[str]): List of file names.

    Returns:
        List[str]: List of file names with .txt extension.
    """
    filtered_list = [file for file in files_list if file[-4:] == ".txt"]
    return filtered_list

def get_tokens(dir_path: str) -> Dict[str, str]:
    """Process text files in a directory and return a dictionary of tokenized content.

    Args:
        dir_path (str): Path to the directory containing text files.

    Returns:
        Dict[str, str]: Dictionary mapping document names to their tokenized content.
    """
    # we will be using this for making the trie
    # takes in path to the folder of interest, and returns a dict {doc_name, processed_content}
    files_input = os.listdir(dir_path) # Takes file path and returns a list all the contents 
    files_filtered_list = only_txt_files(files_input)
    doc_tokens = {key: None for key in files_filtered_list}

    for i in files_filtered_list:
        file_path = os.path.join(dir_path, i) # folder + doc_name
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            r = remove_punctuation(f.read().replace("\n"," ")).split()
            # take r and add them as values to each doc
            doc_tokens[i] = r # replacing values in dictionary 

    return doc_tokens # dictionary of key doc_name: content as values

# takes in path to document and the directory you want to insert in
def insert_file(path_doc: str, target_dir: str) -> None: 
    """Move a document to the specified target directory.

    Args:
        path_doc (str): Path to the document to move.
        target_dir (str): Path to the target directory.
    """
    shutil.move(path_doc, target_dir)

# takes in path to folder and the file you want to delete
def delete_file(target_dir: str, file_name: str) -> None:
    """Delete a file from the specified directory.

    Args:
        target_dir (str): Path to the directory containing the file.
        file_name (str): Name of the file to delete.
    """
    full_path = os.path.join(target_dir, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print("file doesn't exist")

# we will be using for matching
# pass the folder of interest, get a dictionary of {doc_name: raw_content}
def map_documents(target_dir: str) -> Dict[str, str]:
    """Create a dictionary mapping document names to their cleaned content.

    Args:
        target_dir (str): Path to the directory containing text files.

    Returns:
        Dict[str, str]: Dictionary mapping document names to their cleaned content.
    """
    documents_table = {}
    files_input = os.listdir(target_dir) # List of all documents
    filtered = only_txt_files(files_input)
    for i in filtered:
        file_path = os.path.join(target_dir, i)  # Create full path
        with open(file_path, 'r', encoding='utf-8') as f:  # Use full path
            file_text = f.read().lower()
            cleaned_text = remove_punctuation(file_text)
            documents_table[i] = cleaned_text  # Correct dictionary assignment
    
    return documents_table