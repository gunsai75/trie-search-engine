import preprocessing
import trie
import pattern_matching
from collections import defaultdict
from typing import Dict, List, Tuple
import os
import time
# import formatter_verbose
# import formatter_simple

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
    q_clean = preprocessing.remove_punctuation(query).lower()
    q_split = q_clean.split(" ")
    return q_split

def rank_documents(results_list: List[Dict]) -> List[Tuple[str, int, Dict]]:
    """Rank documents by total number of matches across all query words.
    
    Args:
        results_list (List[Dict]): List of search results for each query word.
    
    Returns:
        List[Tuple[str, int, Dict]]: List of (document_name, total_matches, details) sorted by total_matches in descending order.
    
    Raises:
        ValueError: If results_list is not a list of valid result dictionaries.
    """
    if not isinstance(results_list, list) or not all(isinstance(r, dict) for r in results_list):
        raise ValueError("Results list must be a list of dictionaries")
    
    # Aggregate match counts per document
    doc_scores = defaultdict(int)
    doc_details = defaultdict(list)
    
    for result in results_list:
        doc_results = result.get('document_results', {})
        for doc_name, doc_result in doc_results.items():
            matches_count = doc_result.get('matches_count', 0)
            doc_scores[doc_name] += matches_count
            doc_details[doc_name].append(doc_result)
    
    # Sort documents by total matches (descending)
    ranked = [
        (doc_name, score, doc_details[doc_name])
        for doc_name, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return ranked

def main():
    """Main function to run the document search system."""
    print("Welcome to Document Search")
    print("Only .txt files are supported")

    # Get and validate directory path
    target_path = input("Enter the path for your target directory: ")
    target_path = os.path.abspath(target_path) # Convert to raw string (TODO: Improve input handling)
    
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

    """ 
    Bhuvan needs to add Insertion and Deletion part here
    From the preprocessing module, insert_file and delete_file can be used
    The preprocessing module is already imported.
    """
    
    usr_query = input('Enter the phrase to search: ')
    
    # Initialize trie for prefix-based search
    trie_instance = trie.PrefixTree()
    
    # Preprocess documents into tokens
    doc_collection = preprocess_docs(target_path)  # {doc_name: [list of words]}
    # print(doc_collection) 

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
    all_results = []
    
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
        matcher = pattern_matching.PatternMatch()
        
        # Brute force search
        bruteforce_time_start = time.monotonic()
        bruteforce_results = matcher.search_in_documents_bruteforce(doc_map, q, relevant_docs)
        bruteforce_time_end = time.monotonic()

        bruteforce_times.append(bruteforce_time_end - bruteforce_time_start)
        all_results.append(bruteforce_results)

        # KMP search
        kmp_time_start = time.monotonic()
        kmp_results = matcher.search_in_documents_kmp(doc_map, q, relevant_docs)
        kmp_time_end = time.monotonic()

        kmp_times.append(kmp_time_end - kmp_time_start)
        all_results.append(kmp_results)

        # Display results (simple format)
        print("BRUTEFORCE")
        # print(bruteforce_results)
        print("KMP")
        # print(kmp_results)

        # Ranking by Relevance
        if all_results:
            print("\n" + "=" * 50)
            print("Ranked Documents by Relevance (Total Matches)")
            print("=" * 50)
            ranked_docs = rank_documents(all_results)
            if not ranked_docs:
                print("No matching documents found.")
            else:
                for doc_name, score, details in ranked_docs:
                    print(f"\nDocument: {doc_name}")
                    print(f"Total Matches: {score}")
                    print("Details:")
                    for detail in details:
                        pattern = detail['pattern']
                        matches = detail['matches']
                        count = detail['matches_count']
                        print(f"  Pattern '{pattern}': {count} matches at positions {matches}")
    
    # Display average execution times
    if bruteforce_times:
        print("=" * 70)
        print("Total Time: ")
        print(f"Bruteforce: {sum(bruteforce_times)}")
        print(f"KMP: {sum(kmp_times)} \n")
        print("Average of all times:")
        print(f"Bruteforce: {sum(bruteforce_times) / len(bruteforce_times):.6f} seconds")
        print(f"KMP: {sum(kmp_times) / len(kmp_times):.6f} seconds")

if __name__ == "__main__":
    main()