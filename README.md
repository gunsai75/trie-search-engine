# Document Search System

A Python-based document search engine that efficiently searches through text files using advanced string matching algorithms and data structures.

## Features

- **Multiple Search Algorithms**: Implements both Brute Force and KMP (Knuth-Morris-Pratt) pattern matching algorithms
- **Prefix-Based Search**: Uses a Trie data structure for efficient prefix matching
- **Document Management**: Insert and delete files from the search directory
- **Relevance Ranking**: Ranks documents by total number of matches across all query terms
- **Performance Comparison**: Measures and compares execution times between different algorithms
- **Text Preprocessing**: Handles punctuation removal and tokenization

## Project Structure

```
document-search/
├── main.py              # Main application entry point
├── pattern_matching.py  # Pattern matching algorithms (Brute Force & KMP)
├── preprocessing.py     # Text preprocessing and file operations
├── trie.py             # Trie data structure implementation
└── README.md           # This file
```

## Requirements

- Python 3.6+
- Standard library modules only (no external dependencies)

## Installation

1. Clone or download the project files
2. Ensure all Python files are in the same directory
3. Run the main application:

```bash
python main.py
```

## Usage

### Basic Search

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Enter directory path**: 
   - Provide the path to your directory containing `.txt` files
   - Leave empty to use current working directory

3. **Choose an action**:
   - `1`: Continue with search (default)
   - `2`: Insert a file into the directory
   - `3`: Delete a file from the directory

4. **Enter search query**: 
   - Type the phrase or words you want to search for
   - The system will search for each word as a prefix

### File Management

#### Insert a File
- Select option `2` when prompted
- Enter the full path of the file you want to insert
- The file will be moved to the target directory

#### Delete a File
- Select option `3` when prompted
- Enter the filename you want to delete
- The file will be removed from the target directory

## Algorithm Details

### Pattern Matching Algorithms

#### 1. Brute Force Search
- **Time Complexity**: O(n×m) where n is text length, m is pattern length
- **Space Complexity**: O(1)
- Simple character-by-character comparison

#### 2. KMP (Knuth-Morris-Pratt) Algorithm
- **Time Complexity**: O(n+m)
- **Space Complexity**: O(m)
- Uses a failure function to avoid redundant comparisons
- More efficient for longer patterns and texts

### Data Structures

#### Trie (Prefix Tree)
- Enables efficient prefix-based searching
- **Time Complexity**: O(m) for search operations
- Stores an inverted index mapping words to documents

#### Inverted Index
- Maps each word to the set of documents containing it
- Enables quick lookup of relevant documents for each query term

## Output Format

The system provides detailed output including:

1. **Search Results**: Shows matches found by both algorithms
2. **Document Ranking**: Lists documents ranked by total number of matches
3. **Match Details**: For each document, shows:
   - Pattern searched
   - Number of matches
   - Positions of matches in the text
4. **Performance Metrics**:
   - Total execution time for each algorithm
   - Average execution time across all searches

### Sample Output

```
Document: example.txt
Total Matches: 5
Details:
  Pattern 'search': 3 matches at positions [10, 45, 78]
  Pattern 'algorithm': 2 matches at positions [23, 56]

======================================================================
Total Time: 
Bruteforce: 0.002341
KMP: 0.001567 

Average of all times:
Bruteforce: 0.001171 seconds
KMP: 0.000784 seconds
```

## File Format Requirements

- Only `.txt` files are supported
- Files should be encoded in UTF-8
- The system handles punctuation removal and text normalization automatically

## Technical Implementation

### Text Preprocessing
- Removes punctuation and special characters
- Converts text to lowercase for case-insensitive matching
- Tokenizes text by whitespace

### Search Process
1. **Preprocessing**: Tokenize all documents and build trie structure
2. **Query Processing**: Clean and split user query into individual terms
3. **Prefix Matching**: Use trie to find words starting with each query term
4. **Document Filtering**: Identify documents containing relevant words
5. **Pattern Matching**: Apply both brute force and KMP algorithms
6. **Ranking**: Sort documents by total number of matches
7. **Results Display**: Show ranked results with detailed match information

## Error Handling

The system includes error handling for:
- Invalid directory paths
- Missing files
- Invalid file operations
- Empty search results
- Malformed input data

## Performance Considerations

- **Memory Usage**: Stores entire document collection in memory for fast access
- **Scalability**: Suitable for small to medium-sized document collections
- **Algorithm Choice**: KMP is generally faster, especially for longer patterns
- **Preprocessing Overhead**: One-time cost for building trie and inverted index

## Limitations

- Only supports plain text files (.txt)
- Entire document collection must fit in memory
- Case-insensitive search only
- No support for regular expressions or complex queries

## Future Enhancements

Potential improvements could include:
- Support for additional file formats (PDF, DOCX, etc.)
- Boolean query operators (AND, OR, NOT)
- Fuzzy matching for approximate searches
- Web interface for easier usage
- Database storage for larger document collections
- Advanced ranking algorithms (TF-IDF, BM25)

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.
