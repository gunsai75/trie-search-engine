import preprocessing
import trie
import formatter_verbose
import formatter_simple
import pattern_matching_test
from typing import Dict, List
import os

def preprocess_docs(dir_path: str) -> Dict[str, str]:
    doc_tokens = preprocessing.get_tokens(dir_path)
    return doc_tokens

def query_process(query: str) -> List:
    q_clean = preprocessing.remove_punctuation(query)
    q_split = q_clean.split(" ")
    return q_split

print("Welcome to Document Search")
print("Only .txt files tho")

target_path = input("Enter the path for your target directory: ")
target_path = repr(target_path)[1:-1] # Converting to raw string

if not os.path.exists(target_path):
    print(f"Error: Directory '{target_path}' does not exist!")
    exit(1)

print(f"Looking in directory: {target_path}")
if os.path.isdir(target_path):
    files = [f for f in os.listdir(target_path) if f.endswith('.txt')]
    print(f"Found .txt files: {files}")
else:
    print("Path is not a directory!")

usr_query = input('Enter the phrase to search: ')

trie = trie.PrefixTree()

doc_collection = preprocess_docs(target_path) # creates a dictionary {doc_name: [list of words]}

for doc in doc_collection: # traversing a dictionary
    word_list = doc_collection[doc]
    trie.insert_from_document(word_list, doc)

 # list of words in query
query_split = query_process(usr_query)

doc_map = preprocessing.map_documents(target_path) # maps doc name to it's text

# trying to get prefixes found in trie and then putting then in matching algos 
state = 1
for q in query_split: # each query gets it's own thing
    trie_results = trie.starts_with(q) 
    if len(trie_results) == 0:
        state = 0
        print("No phrases found")
        break
    else:
        state = 1
        match = pattern_matching_test.PatternMatch()
        # bruteforce
        relevant_docs = set()
        for result in trie_results:
            relevant_docs.update(result['documents'])
        relevant_docs = list(relevant_docs)
        
        # bruteforce
        bruteforce_results = match.search_in_documents_bruteforce(doc_map, q, relevant_docs)
        # kmp
        kmp_results = match.search_in_documents_kmp(doc_map, q, relevant_docs)

        # VERBOSE DISPLAY----
        # formatter_verbose.enhanced_display_results(bruteforce_results, kmp_results, doc_map)

        # SIMPLE DISPLAY ----- (uncomment the above line and comment the whole section below to implement VERBOSE)
        print("\n" + "="*70)
        print("BRUTE FORCE SEARCH RESULTS")
        print("="*70)
        formatter_simple.show_matches_with_context(bruteforce_results, doc_map)

        print("\n" + "="*70)
        print("KMP SEARCH RESULTS")
        print("="*70)
        formatter_simple.show_matches_with_context(kmp_results, doc_map)

        # Verify both algorithms give identical results
        if bruteforce_results['total_matches'] == kmp_results['total_matches']:
            print(f"\n✅ VERIFICATION: Both algorithms found {bruteforce_results['total_matches']} matches")
            print("✅ Results are identical - algorithms working correctly!")
        else:
            print(f"\n❌ MISMATCH DETECTED:")
            print(f"   Brute Force: {bruteforce_results['total_matches']} matches")
            print(f"   KMP: {kmp_results['total_matches']} matches")