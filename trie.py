from collections import defaultdict
from typing import List, Dict

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
       
    def starts_with(self, prefix: str) -> List[Dict]:
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
