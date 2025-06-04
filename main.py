import preprocessing
import trie
import formatter_verbose
import formatter_simple
import pattern_matching_test
from typing import Dict, List
import os
import time

def preprocess_docs(dir_path: str) -> Dict[str, List[str]]:
    """Preprocess all .txt files in a directory into a dictionary of tokenized words.
    
    Args:
        dir_path (str): Path to the directory containing text files.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping document names to lists of tokenized words.
    """
    doc_tokens = preprocessing.get_tokens(dir_path)
    return doc_tokens

def query_process(query: str) -> List[str]:
    """Clean and split a query string into individual words.
    
    Args:
        query (str): The user-provided query string.
    
    Returns:
        List[str]: List of cleaned query words (punctuation removed, split by spaces).
    """
    q_clean = preprocessing.remove_punctuation(query)
    q_split = q_clean.split(" ")
    return q_split

def main():
    """Main function to run the document search system."""
    print("Welcome to Document Search")
    print("Only .txt files are supported")

    # Get and validate directory path
    target_path = input("Enter the path for your target directory: ")
    target_path = repr(target_path)[1:-1]  # Convert to raw string (TODO: Improve input handling)
    
    if not os.path.exists(target_path):
        print(f"Error: Directory '{target_path}' does not exist!")
        exit(1)
    
    print(f"Looking in directory: {target_path}")
    if os.path.isdir(target_path):
        files = [f for f in os.listdir(target_path) if f.endswith('.txt')]
        print(f"Found .txt files: {files}")
    else:
        print("Error: Path is not a directory!")
        exit(1)
    
    usr_query = input('Enter the phrase to search: ')
    
    # Initialize trie for prefix-based search
    trie_instance = trie.PrefixTree()
    
    # Preprocess documents into tokens
    doc_collection = preprocess_docs(target_path)  # {doc_name: [list of words]}
    
    # Insert words into trie with associated document names
    for doc in doc_collection:
        word_list = doc_collection[doc]
        trie_instance.insert_from_document(word_list, doc)
    
    # Process query into individual words
    query_split = query_process(usr_query)
    
    # Map document names to their full text
    doc_map = preprocessing.map_documents(target_path)  # {doc_name: text}
    
    # Lists to store execution times for performance comparison
    bruteforce_times = []
    kmp_times = []
    
    # Search for each query word in relevant documents
    for q in query_split:
        trie_results = trie_instance.starts_with(q)  # Get words with prefix q and their documents
        if not trie_results:
            print(f"No matches found for prefix '{q}'")
            break
        
        # Get unique documents containing prefix matches
        relevant_docs = set()
        for result in trie_results:
            relevant_docs.update(result['documents'])
        relevant_docs = list(relevant_docs)
        
        # Initialize pattern matcher
        matcher = pattern_matching_test.PatternMatch()
        
        # Brute force search
        bruteforce_time_start = time.monotonic()
        bruteforce_results = matcher.search_in_documents_bruteforce(doc_map, q, relevant_docs)
        bruteforce_time_end = time.monotonic()
        bruteforce_times.append(bruteforce_time_end - bruteforce_time_start)
        
        # KMP search
        kmp_time_start = time.monotonic()
        kmp_results = matcher.search_in_documents_kmp(doc_map, q, relevant_docs)
        kmp_time_end = time.monotonic()
        kmp_times.append(kmp_time_end - kmp_time_start)
        
        # Display results (simple format)
        print("BRUTEFORCE")
        print(bruteforce_results)
        print("KMP")
        print(kmp_results)
    
    # Display average execution times
    if bruteforce_times:
        print("=" * 30)
        print("Total time taken:")
        print(f"Bruteforce: {sum(bruteforce_times) / len(bruteforce_times):.6f} seconds")
        print(f"KMP: {sum(kmp_times) / len(kmp_times):.6f} seconds")

if __name__ == "__main__":
    main()