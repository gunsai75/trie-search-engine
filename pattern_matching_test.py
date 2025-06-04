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

    def get_results_bruteforce(self, text: str, pattern: str) -> Dict:
        results_bruteforce = self.search_brute_force(text, pattern)

        return {
            'match-type': "brute force",
            'pattern': pattern,
            'matches': results_bruteforce,
            'matches_count': len(results_bruteforce)
        }
    
    def get_results_kmp(self, text: str, pattern: str) -> Dict:
        results_kmp = self.search_kmp(text, pattern)

        return {
            'match-type': 'kmp',
            'pattern': pattern,
            'matches': results_kmp,
            'matches-count': len(results_kmp)
        }
