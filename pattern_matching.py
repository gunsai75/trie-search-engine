from typing import List, Tuple, Dict

class PatternMatch:
    def search_brute_force(self, text: str, pattern: str) -> List[int]:
        matches = []
        n, m = len(text), len(pattern)
        
        # Handle edge cases
        if m == 0:
            return list(range(n + 1))  # Empty pattern matches at every position
        if n == 0 or m > n:
            return []
        
        comparisons = 0
        for i in range(n - m + 1):
            j = 0
            while j < m and text[i + j] == pattern[j]:
                comparisons += 1
                j += 1
            if j == m:
                matches.append(i)
            if j > 0:
                comparisons += 1
       
        return matches
    
    # end of brute force search
    # start of KMP
    def compute_lps_arr(self, pattern: str) -> List[int]:
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
   
    def search_kmp(self, text: str, pattern: str) -> List[int]:
        matches = []
        n, m = len(text), len(pattern)
        
        # Handle edge cases
        if m == 0:
            return list(range(n + 1))  # Empty pattern matches at every position
        if n == 0 or m > n:
            return []
        
        comparisons = 0
       
        # getting lps
        lps = self.compute_lps_arr(pattern)
        i = 0
        j = 0
        
        while i < n:
            comparisons += 1
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:  # Fixed: added i < n check
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return matches
    
    def search_with_comparision(self, text: str, pattern: str) -> Dict:
        results_brute_force = self.search_brute_force(text, pattern)
        results_kmp = self.search_kmp(text, pattern)
        results_match = results_brute_force == results_kmp
        return {
            'pattern': pattern,
            'matches': results_kmp,
            'matches_count': len(results_kmp),  # Fixed: was 'match_count'
            'results_match': results_match,
        }
   
    def search_in_documents(self, document_texts: Dict[str, str], pattern: str, relevant_docs: List[str] = None) -> Dict:
        results = {}
        total_matches = 0
        docs_to_search = relevant_docs if relevant_docs else document_texts.keys()
        
        for doc_name in docs_to_search:
            if doc_name in document_texts:
                doc_result = self.search_with_comparision(document_texts[doc_name], pattern)
                if doc_result['matches_count'] > 0:  # Fixed: was 'match_count'
                    results[doc_name] = doc_result
                    total_matches += doc_result['matches_count']  # Fixed: was 'match_count'
           
        return {
            'pattern': pattern,
            'total_matches': total_matches,
            'documents_found': len(results),
            'document_results': results
        }

# def test_pattern_matching():
#     """Test function to validate implementations"""
#     matcher = PatternMatch()
#     # Test cases
#     test_cases = [
#         ("ABABDABACDABABCABCABCABCABC", "ABABCAB"),
#         ("AABAACAADAABAABA", "AABA"),
#         ("hello world hello", "hello"),
#         ("", "test"),  # Edge case: empty text
#         ("test", ""),   # Edge case: empty pattern
#         ("abcdef", "xyz"),  # No matches
#         ("aaaa", "aa"),     # Overlapping matches
#     ]
    
#     print("Pattern Matching Test Results:")
#     print("=" * 50)
    
#     for text, pattern in test_cases:
#         result = matcher.search_with_comparision(text, pattern)
#         print(f"Text: '{text}'")
#         print(f"Pattern: '{pattern}'")
#         print(f"Matches found at indices: {result['matches']}")
#         print(f"Match count: {result['matches_count']}")
#         print(f"Algorithms match: {result['results_match']}")
#         print("-" * 30)

# if __name__ == "__main__":
#     test_pattern_matching()