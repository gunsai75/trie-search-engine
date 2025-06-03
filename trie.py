import preprocessing
from collections import defaultdict

class TrieNode:
    def __init__(self, text=''):
        self.text = text
        self.children = dict()
        self.is_word = False

class PrefixTree:
    def __init__(self):
        self.root = TrieNode()
        self.inverted_index = defaultdict(set)  # word -> set of documents
    
    def insert(self, word, document_name):
        # Insert into trie
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0:i+1]
                current.children[char] = TrieNode(prefix)
            current = current.children[char]
        current.is_word = True
        
        # Add to inverted index
        self.inverted_index[word].add(document_name)
   
    def insert_from_document(self, word_list, document_name):
        for word in word_list:
            self.insert(word, document_name)
    
    def find(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        if current.is_word:
            return current
       
    def starts_with(self, prefix):
        words = []
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
       
        self.__child_words_for(current, words)
        
        # Add document information to results
        results = []
        for word in words:
            results.append({
                'word': word,
                'documents': list(self.inverted_index[word])
            })
        return results
    
    def __child_words_for(self, node, words):
        if node.is_word:
            words.append(node.text)
        for letter in node.children:
            self.__child_words_for(node.children[letter], words)

# Running some test cases

# if __name__ == '__main__':
#     trie = PrefixTree()
#     path = <path to file>
#     forward_index = test1.get_tokens(path)
    
#     # Insert words with document information
#     for doc in forward_index:
#         word_list = forward_index[doc]
#         trie.insert_from_document(word_list, doc)
    
#     # Search and display results
#     results = trie.starts_with('co')
#     print(f"Found {len(results)} words starting with 'co':")
#     for result in results:
#         print(f"  '{result['word']}' appears in: {', '.join(result['documents'])}")
    
#     # You can also search the inverted index directly
#     print(f"\nDirect lookup - 'computer' appears in: {list(trie.inverted_index.get('computer', []))}")