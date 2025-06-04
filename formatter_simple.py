# Add this function to your test_ui.py file

def show_matches_with_context(results, doc_map, max_matches_per_doc=3, context_chars=25):
    """
    Show search results with readable text context
    """
    pattern = results['pattern']
    print(f"\n🔍 Found '{pattern}' in {results['documents_found']} documents ({results['total_matches']} total matches)")
    print("=" * 70)
    
    for doc_name, doc_info in results['document_results'].items():
        print(f"\n📄 {doc_name}: {doc_info['matches_count']} matches")
        print("-" * 50)
        
        doc_text = doc_map[doc_name]
        matches = doc_info['matches']
        
        # Show first few matches
        for i, pos in enumerate(matches[:max_matches_per_doc]):
            start = max(0, pos - context_chars)
            end = min(len(doc_text), pos + len(pattern) + context_chars)
            
            before = doc_text[start:pos]
            match = doc_text[pos:pos + len(pattern)]
            after = doc_text[pos + len(pattern):end]
            
            print(f"  Match {i+1} at position {pos}:")
            print(f"    ...{before}[{match}]{after}...")
        
        if len(matches) > max_matches_per_doc:
            print(f"    ... and {len(matches) - max_matches_per_doc} more matches")
        print()

# Then in your main code, replace:
# print(f"Brute Force Results: {bruteforce_results}")
# print(f"KMP Results: {kmp_results}")

# With:
# print("\n" + "="*50)
# print("SEARCH RESULTS")
# print("="*50)
# show_matches_with_context(bruteforce_results, doc_map)