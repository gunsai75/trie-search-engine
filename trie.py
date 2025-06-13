from collections import defaultdict
from typing import List, Dict

class TrieNode:
    """A node in the prefix tree (trie).

    Attributes:
        text (str): The text associated with the node (prefix or word).
        children (dict): Dictionary mapping characters to child nodes.
        is_word (bool): Indicates if the node represents a complete word.
    """
    def __init__(self, text=''):
        self.text = text
        self.children = dict()
        self.is_word = False

class PrefixTree:
    """A prefix tree (trie) for storing words and their associated documents.

    Attributes:
        root (TrieNode): The root node of the trie.
        inverted_index (defaultdict): Maps words to sets of document names.
    """
    def __init__(self):
        """Initialize an empty prefix tree."""
        self.root = TrieNode()
        self.inverted_index = defaultdict(set)
    
    def insert(self, word: str, document_name: str) -> None:
        """Insert a word and its associated document name into the trie and inverted index.

        Args:
            word (str): The word to insert.
            document_name (str): The name of the document containing the word.
        """
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
    
    def insert_from_document(self, word_list: List[str], document_name: str) -> None:
        """Insert all words from a document into the trie.

        Args:
            word_list (List[str]): List of words to insert.
            document_name (str): Name of the document containing the words.
        """
        for word in word_list:
            self.insert(word, document_name)
    
    def find(self, word: str) -> TrieNode:
        """Find the node corresponding to a word in the trie.

        Args:
            word (str): The word to search for.

        Returns:
            TrieNode or None: The node if the word exists, None otherwise.
        """
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        if current.is_word:
            return current
       
    def starts_with(self, prefix: str) -> List[Dict]:
        """Find all words in the trie starting with a given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            List[Dict]: List of dictionaries containing words and their associated documents.
        """
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
    
    def __child_words_for(self, node: TrieNode, words: List[str]) -> None:
        """Recursively collect words from a node and its children.

        Args:
            node (TrieNode): The current node to process.
            words (List[str]): List to store collected words.
        """
        if node.is_word:
            words.append(node.text)
        for letter in node.children:
            self.__child_words_for(node.children[letter], words)