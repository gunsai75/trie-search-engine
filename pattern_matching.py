from typing import List, Dict

class PatternMatch:
    """A class for pattern matching algorithms including brute force and KMP.

    Provides methods for searching patterns in text and documents using brute force
    and Knuth-Morris-Pratt (KMP) algorithms.
    """
    
    def search_brute_force(self, text: str, pattern: str) -> List[int]:
        """Search for a pattern in text using brute force algorithm.

        Args:
            text (str): The text to search in.
            pattern (str): The pattern to search for.

        Returns:
            List[int]: List of starting indices where the pattern is found.
        """
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
        """Compute the Longest Prefix Suffix (LPS) array for KMP algorithm.

        Args:
            pattern (str): The pattern to compute LPS for.

        Returns:
            List[int]: The LPS array.
        """
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
        """Search for a pattern in text using KMP algorithm.

        Args:
            text (str): The text to search in.
            pattern (str): The pattern to search for.

        Returns:
            List[int]: List of starting indices where the pattern is found.
        """
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

    def get_results_bruteforce(self, text: str, pattern: str) -> Dict:
        """Get brute force search results for a pattern in text.

        Args:
            text (str): The text to search in.
            pattern (str): The pattern to search for.

        Returns:
            Dict: Dictionary containing pattern, matches, and match count.
        """
        results_bruteforce = self.search_brute_force(text, pattern)

        return {
            'pattern': pattern,
            'matches': results_bruteforce,
            'matches_count': len(results_bruteforce)
        }
    
    def get_results_kmp(self, text: str, pattern: str) -> Dict:
        """Get KMP search results for a pattern in text.

        Args:
            text (str): The text to search in.
            pattern (str): The pattern to search for.

        Returns:
            Dict: Dictionary containing pattern, matches, and match count.
        """
        results_kmp = self.search_kmp(text, pattern)

        return {
            'pattern': pattern,
            'matches': results_kmp,
            'matches_count': len(results_kmp)
        }
    
    def search_in_documents_kmp(self, document_texts: Dict[str, str], pattern: str, relevant_docs: List[str] = None) -> Dict:
        """Search for a pattern in multiple documents using KMP algorithm.

        Args:
            document_texts (Dict[str, str]): Dictionary mapping document names to their content.
            pattern (str): The pattern to search for.
            relevant_docs (List[str], optional): List of document names to search. Defaults to all documents.

        Returns:
            Dict: Dictionary containing search results including pattern, total matches, and document results.
        """
        results = {}
        total_matches = 0
        docs_to_search = relevant_docs if relevant_docs is not None else list(document_texts.keys())
        
        for doc_name in docs_to_search:
            if doc_name in document_texts:
                doc_result_kmp = self.get_results_kmp(document_texts[doc_name], pattern)
                results[doc_name] = doc_result_kmp # inserting into dict
                total_matches += doc_result_kmp['matches_count']  
           
        return {
            'match-type': "kmp",
            'pattern': pattern,
            'total_matches': total_matches,
            'documents_found': len(results),
            'document_results': results
        }
    
    def search_in_documents_bruteforce(self, document_texts: Dict[str, str], pattern: str, relevant_docs: List[str] = None) -> Dict:
        """Search for a pattern in multiple documents using brute force algorithm.

        Args:
            document_texts (Dict[str, str]): Dictionary mapping document names to their content.
            pattern (str): The pattern to search for.
            relevant_docs (List[str], optional): List of document names to search. Defaults to all documents.

        Returns:
            Dict: Dictionary containing search results including pattern, total matches, and document results.
        """
        results = {}
        total_matches = 0
        docs_to_search = relevant_docs if relevant_docs is not None else list(document_texts.keys())
        
        for doc_name in docs_to_search:
            if doc_name in document_texts:
                doc_result_bruteforce = self.get_results_bruteforce(document_texts[doc_name], pattern)
                results[doc_name] = doc_result_bruteforce # inserting into dict
                total_matches += doc_result_bruteforce['matches_count'] 
           
        return {
            'match-type': "brute force",
            'pattern': pattern,
            'total_matches': total_matches,
            'documents_found': len(results),
            'document_results': results
        }