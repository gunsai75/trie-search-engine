def display_search_results(results, doc_map, context_length=30):
    """
    Display search results with text context around each match
    
    Args:
        results: The search results dictionary from your pattern matching
        doc_map: Dictionary mapping document names to their full text
        context_length: Number of characters to show before and after the match
    """
    pattern = results['pattern']
    print(f"\n=== Search Results for '{pattern}' ===")
    print(f"Total matches: {results['total_matches']}")
    print(f"Documents found: {results['documents_found']}")
    print("-" * 50)
    
    for doc_name, doc_results in results['document_results'].items():
        print(f"\n {doc_name} ({doc_results['matches_count']} matches):")
        print("=" * 40)
        
        doc_text = doc_map[doc_name]
        matches = doc_results['matches']
        
        # Show first few matches to avoid overwhelming output
        max_display = min(5, len(matches))  # Show max 5 matches per document
        
        for i, match_pos in enumerate(matches[:max_display]):
            # Extract context around the match
            start = max(0, match_pos - context_length)
            end = min(len(doc_text), match_pos + len(pattern) + context_length)
            context = doc_text[start:end]
            
            # Highlight the match (simple approach)
            match_in_context = context.replace(pattern, f"**{pattern}**")
            
            print(f"  Match {i+1} (position {match_pos}): ...{match_in_context}...")
        
        if len(matches) > max_display:
            print(f"  ... and {len(matches) - max_display} more matches")

def display_compact_results(results, doc_map, context_length=15):
    """
    Display compact search results showing just the matched words with brief context
    """
    pattern = results['pattern']
    print(f"\n=== Compact Results for '{pattern}' ===")
    
    for doc_name, doc_results in results['document_results'].items():
        print(f"\n{doc_name} ({doc_results['matches_count']} matches):")
        
        doc_text = doc_map[doc_name]
        matches = doc_results['matches']
        
        # Group nearby matches to avoid repetition
        contexts = []
        for match_pos in matches[:3]:  # Show first 3 matches
            start = max(0, match_pos - context_length)
            end = min(len(doc_text), match_pos + len(pattern) + context_length)
            context = doc_text[start:end].strip()
            if context not in contexts:
                contexts.append(f"...{context}...")
        
        for context in contexts:
            print(f"  • {context}")

def display_summary_results(results):
    """
    Display a summary table of search results
    """
    pattern = results['pattern']
    print(f"\n=== Summary for '{pattern}' ===")
    print(f"{'Document':<15} {'Matches':<8} {'First Match':<12} {'Last Match':<12}")
    print("-" * 50)
    
    for doc_name, doc_results in results['document_results'].items():
        matches = doc_results['matches']
        first_match = matches[0] if matches else "N/A"
        last_match = matches[-1] if matches else "N/A"
        
        print(f"{doc_name:<15} {len(matches):<8} {first_match:<12} {last_match:<12}")

def get_word_context(doc_text, match_pos, pattern, word_radius=3):
    """
    Get context in terms of whole words around the match
    
    Args:
        doc_text: Full document text
        match_pos: Position of the match
        pattern: The search pattern
        word_radius: Number of words to show before and after the match
    """
    # Split into words while keeping track of positions
    words = doc_text.split()
    
    # Find which word contains our match
    current_pos = 0
    target_word_idx = 0
    
    for i, word in enumerate(words):
        if current_pos <= match_pos < current_pos + len(word):
            target_word_idx = i
            break
        current_pos += len(word) + 1  # +1 for space
    
    # Get surrounding words
    start_idx = max(0, target_word_idx - word_radius)
    end_idx = min(len(words), target_word_idx + word_radius + 1)
    
    context_words = words[start_idx:end_idx]
    
    # Highlight the target word
    if target_word_idx < len(words):
        target_word = words[target_word_idx]
        highlighted_word = target_word.replace(pattern, f"**{pattern}**")
        context_words[target_word_idx - start_idx] = highlighted_word
    
    return " ".join(context_words)

# Example usage function to add to your main script:
def enhanced_display_results(bruteforce_results, kmp_results, doc_map):
    """
    Enhanced display function to replace your current print statements
    """
    print("\n" + "="*60)
    print("BRUTE FORCE RESULTS")
    print("="*60)
    display_search_results(bruteforce_results, doc_map)
    
    print("\n" + "="*60)
    print("KMP RESULTS SUMMARY")
    print("="*60)
    display_summary_results(kmp_results)
    
    # Verify both algorithms give same results
    if (bruteforce_results['total_matches'] == kmp_results['total_matches']):
        print(f"\n Both algorithms found {bruteforce_results['total_matches']} matches")
    else:
        print(f"\n Mismatch: BF={bruteforce_results['total_matches']}, KMP={kmp_results['total_matches']}")