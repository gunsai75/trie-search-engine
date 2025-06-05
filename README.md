# Document Search System

A Python-based document search engine that uses advanced data structures and algorithms for efficient text pattern matching and retrieval.

## Features

- **Multi-Algorithm Pattern Matching**: Compare performance between Brute Force and KMP (Knuth-Morris-Pratt) algorithms
- **Prefix Tree (Trie) Implementation**: Fast prefix-based word searching with inverted indexing
- **Document Ranking**: Rank search results by relevance based on match frequency
- **Performance Metrics**: Real-time execution time comparison between algorithms
- **File Management**: Insert and delete documents from the search corpus

## Project Structure

```
document-search/
├── main.py              # Main application entry point
├── pattern_matching.py  # Pattern matching algorithms (Brute Force & KMP)
├── preprocessing.py     # Text preprocessing and file handling utilities
├── trie.py             # Prefix tree implementation with inverted indexing
└── README.md           # Project documentation
```

## Requirements

- Python 3.6+
- Standard library modules only (no external dependencies)

## Installation

1. Clone or download the project files
2. Ensure all Python files are in the same directory
3. Create a directory with `.txt` files you want to search

## Usage

### Basic Usage

1. Run the main application:
   ```bash
   python main.py
   ```

2. When prompted, enter the path to your directory containing `.txt` files:
   ```
   Enter the path for your target directory: /path/to/your/documents
   ```

3. Enter your search query:
   ```
   Enter the phrase to search: your search term
   ```

4. The system will display:
   - Search results from both algorithms
   - Ranked documents by relevance
   - Performance comparison between algorithms

### Example Output

```
Welcome to Document Search
Only .txt files are supported
Enter the path for your target directory: ./sample_docs
Looking in directory: /absolute/path/to/sample_docs
Found .txt files: ['document1.txt', 'document2.txt', 'document3.txt']
Enter the phrase to search: python programming

BRUTEFORCE
KMP

==================================================
Ranked Documents by Relevance (Total Matches)
==================================================

Document: document1.txt
Total Matches: 15
Details:
  Pattern 'python': 8 matches at positions [12, 45, 78, 123, 156, 189, 234, 267]
  Pattern 'programming': 7 matches at positions [23, 67, 134, 178, 245, 289, 323]

======================================================================
Total Time: 
Bruteforce: 0.002341
KMP: 0.001876 

Average of all times:
Bruteforce: 0.001171 seconds
KMP: 0.000938 seconds
```

## Algorithm Details

### Pattern Matching Algorithms

#### Brute Force Search
- **Time Complexity**: O(n×m) where n = text length, m = pattern length
- **Space Complexity**: O(1)
- Simple character-by-character comparison

#### KMP (Knuth-Morris-Pratt) Algorithm
- **Time Complexity**: O(n+m) where n = text length, m = pattern length
- **Space Complexity**: O(m) for the LPS (Longest Proper Prefix Suffix) array
- Optimized pattern matching using failure function

### Data Structures

#### Prefix Tree (Trie)
- Efficient prefix-based searching
- Integrated inverted index for document mapping
- **Time Complexity**: O(m) for search where m = word length
- **Space Complexity**: O(ALPHABET_SIZE × N × M) where N = number of words, M = average word length

## API Reference

### Main Functions

#### `preprocess_docs(dir_path: str) -> Dict[str, List[str]]`
Preprocesses all `.txt` files in a directory into tokenized words.

#### `query_process(query: str) -> List[str]`
Cleans and splits a query string into individual words.

#### `rank_documents(results_list: List[Dict]) -> List[Tuple[str, int, Dict]]`
Ranks documents by total number of matches across all query words.

### PatternMatch Class

#### `search_brute_force(text: str, pattern: str) -> List[int]`
Performs brute force pattern matching.

#### `search_kmp(text: str, pattern: str) -> List[int]`
Performs KMP pattern matching.

#### `search_in_documents_kmp(document_texts: Dict, pattern: str, relevant_docs: List[str]) -> Dict`
Searches for pattern in multiple documents using KMP.

#### `search_in_documents_bruteforce(document_texts: Dict, pattern: str, relevant_docs: List[str]) -> Dict`
Searches for pattern in multiple documents using brute force.

### PrefixTree Class

#### `insert(word: str, document_name: str)`
Inserts a word into the trie with associated document name.

#### `starts_with(prefix: str) -> List[Dict]`
Returns all words that start with the given prefix along with their document locations.

### Preprocessing Functions

#### `remove_punctuation(text: str) -> str`
Removes punctuation and special characters from text.

#### `get_tokens(dir_path: str) -> Dict[str, List[str]]`
Tokenizes all `.txt` files in a directory.

#### `map_documents(target_dir: str) -> Dict[str, str]`
Creates a mapping of document names to their cleaned text content.

## Performance Considerations

- **KMP Algorithm**: Generally faster for longer patterns and texts
- **Brute Force**: May be faster for very short patterns or small texts
- **Memory Usage**: Trie structure requires significant memory for large vocabularies
- **Preprocessing**: One-time cost that improves search performance

## File Format Support

- Currently supports only `.txt` files
- Files should be UTF-8 encoded
- Binary files are ignored

## Future Enhancements

The codebase includes placeholder comments for:
- File insertion and deletion capabilities (partially implemented)
- Verbose and simple output formatters
- Extended file format support

## Error Handling

- Invalid directory paths
- Non-existent files
- Empty search queries
- Malformed input data

## Contributing

When contributing to this project:
1. Follow existing code style and structure
2. Add appropriate error handling
3. Include performance considerations
4. Test with various file sizes and query types

## License

This project is provided as-is for educational and research purposes.