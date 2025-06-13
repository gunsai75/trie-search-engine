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
    doc_tokens = preprocessing.get_tokens(dir_path) # we get a disct {doc_name: processed content}
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

def rank_documents(results_list: List[Dict]) -> Dict[str, List[Tuple[str, int, Dict]]]:
    """Rank documents by total number of matches across all query words, grouped by algorithm.
    
    Args:
        results_list (List[Dict]): List of search results for each query word with algorithm info.
    
    Returns:
        Dict[str, List[Tuple[str, int, Dict]]]: Dictionary with algorithm names as keys and 
        lists of (document_name, total_matches, details) sorted by total_matches in descending order.
    
    Raises:
        ValueError: If results_list is not a list of valid result dictionaries.
    """
    if not isinstance(results_list, list) or not all(isinstance(r, dict) for r in results_list):
        raise ValueError("Results list must be a list of dictionaries")
    
    # Separate results by algorithm
    algorithm_results = defaultdict(lambda: defaultdict(int))
    algorithm_details = defaultdict(lambda: defaultdict(list))
    
    for result in results_list:
        algorithm = result.get('algorithm', 'unknown')
        doc_results = result.get('document_results', {})
        
        for doc_name, doc_result in doc_results.items():
            matches_count = doc_result.get('matches_count', 0)
            algorithm_results[algorithm][doc_name] += matches_count
            algorithm_details[algorithm][doc_name].append(doc_result)
    
    # Sort documents by total matches for each algorithm
    ranked_by_algorithm = {}
    for algorithm in algorithm_results:
        ranked = [
            (doc_name, score, algorithm_details[algorithm][doc_name])
            for doc_name, score in sorted(algorithm_results[algorithm].items(), 
                                        key=lambda x: x[1], reverse=True)
        ]
        ranked_by_algorithm[algorithm] = ranked
    
    return ranked_by_algorithm

def display_ranked_results(ranked_results: Dict[str, List[Tuple[str, int, Dict]]], 
                          execution_times: Dict[str, List[float]]):
    """Display ranked results grouped by algorithm with execution times.
    
    Args:
        ranked_results: Dictionary with algorithm names as keys and ranked document lists as values
        execution_times: Dictionary with algorithm names as keys and execution time lists as values
    """
    print("\n" + "=" * 70)
    print("SEARCH RESULTS BY ALGORITHM")
    print("=" * 70)
    
    for algorithm, ranked_docs in ranked_results.items():
        print(f"\n{'='*20} {algorithm.upper()} RESULTS {'='*20}")
        
        # Display execution time info
        if algorithm in execution_times and execution_times[algorithm]:
            times = execution_times[algorithm]
            total_time = sum(times)
            avg_time = total_time / len(times)
            print(f"Total Time: {total_time:.6f} seconds")
            print(f"Average Time: {avg_time:.6f} seconds")
        
        print("-" * 50)
        
        if not ranked_docs:
            print("No matching documents found.")
        else:
            for rank, (doc_name, score, details) in enumerate(ranked_docs, 1):
                print(f"\nRank {rank}: {doc_name}")
                print(f"Total Matches: {score}")
                print("Match Details:")
                for detail in details:
                    pattern = detail.get('pattern', 'N/A')
                    matches = detail.get('matches', [])
                    count = detail.get('matches_count', 0)
                    print(f"  Pattern '{pattern}': {count} matches at positions {matches}")
        print()

def main():
    print("Welcome to Document Search")
    print("Only .txt files are supported")

    # Get and validate directory path
    target_path = input("Enter the path for your target directory: ")
    if target_path == '':
        print("Empty input detected. Defaulting to the current working directory.")
        
    target_path = os.path.abspath(target_path) # Convert to raw string (TODO: Improve input handling)
    
    if not os.path.exists(target_path):
        print(f"Error: Directory '{target_path}' does not exist!")
        exit(1)
    
    # if it's successful
    print(f"Looking in directory: {target_path}")
    if os.path.isdir(target_path):
        files = [f for f in os.listdir(target_path) if f.endswith('.txt')]
        print(f"Found .txt files: {files}")
    else:
        print("Error: Path is not a directory!")
        exit(1)

    """ 
    TODO: need to add Insertion and Deletion part here
    From the preprocessing module, insert_file and delete_file can be used
    The preprocessing module is already imported.
    """
    print("\n\n\nWhat do you want to do in this directory? ")
    print("1. Continue with search [DEFAULT]")
    print("2. Insert a file in this directory")
    print("3. Delete a file in this directory")

    usr_choice = int(input("Enter a number: "))
    if ((not type(usr_choice) is not int) and (usr_choice not in [1,2,3])):
        raise TypeError("Only integers are allowed")

    while(usr_choice != 1):
        if usr_choice == 3:
            try:
                del_file_name = input("Enter file name to delete: ")
                preprocessing.delete_file(target_path, del_file_name)
                print("Deleted.")
            except:
                print("----- ERROR: Enter valid file name -----")
            finally:
                print("\nDefaulting to searching.")
                usr_choice = 1

        elif usr_choice == 2:
            try:
                path_file_insert = input("Enter file path to insert: ")
                path_file_insert = os.path.abspath(path_file_insert)
                preprocessing.insert_file(path_file_insert, target_path)
                print("\n\nFile Inserted.")
            except:
                print("----- ERROR: Enter valid file name -----")
            finally:
                print("\nDefaulting to searching.")
                usr_choice = 1

        else:
            break
        

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
    
    # Dictionary to store execution times by algorithm
    execution_times = {
        'bruteforce': [],
        'kmp': []
    }
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

        # Add algorithm identifier to results
        bruteforce_results['algorithm'] = 'bruteforce'
        execution_times['bruteforce'].append(bruteforce_time_end - bruteforce_time_start)
        all_results.append(bruteforce_results)

        # KMP search
        kmp_time_start = time.monotonic()
        kmp_results = matcher.search_in_documents_kmp(doc_map, q, relevant_docs)
        kmp_time_end = time.monotonic()

        # Add algorithm identifier to results
        kmp_results['algorithm'] = 'kmp'
        execution_times['kmp'].append(kmp_time_end - kmp_time_start)
        all_results.append(kmp_results)

    # Ranking by Algorithm and Relevance
    if all_results:
        ranked_results = rank_documents(all_results)
        display_ranked_results(ranked_results, execution_times)
        
        # Performance comparison summary
        print("=" * 70)
        print("PERFORMANCE COMPARISON SUMMARY")
        print("=" * 70)
        
        for algorithm in ['bruteforce', 'kmp']:
            if execution_times[algorithm]:
                total_time = sum(execution_times[algorithm])
                avg_time = total_time / len(execution_times[algorithm])
                print(f"{algorithm.upper()}:")
                print(f"  Total Time: {total_time:.6f} seconds")
                print(f"  Average Time: {avg_time:.6f} seconds")
        
        # Determine faster algorithm
        if execution_times['bruteforce'] and execution_times['kmp']:
            avg_bf = sum(execution_times['bruteforce']) / len(execution_times['bruteforce'])
            avg_kmp = sum(execution_times['kmp']) / len(execution_times['kmp'])
            faster = "KMP" if avg_kmp < avg_bf else "Brute Force"
            speedup = abs(avg_bf - avg_kmp) / max(avg_bf, avg_kmp) * 100
            print(f"\nFaster Algorithm: {faster}")
            print(f"Speed Improvement: {speedup:.2f}%")

if __name__ == "__main__":
    main()