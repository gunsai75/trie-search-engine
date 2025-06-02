import os
import string

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
