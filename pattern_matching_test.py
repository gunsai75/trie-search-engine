from typing import List, Dict


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
            'matches_count': len(results_kmp)
        }
    
    # def search_in_documents(self, pattern: str, relevant_docs: List[str] = None) -> Dict:
    #     results = {}
    #     total_matches = 0
    #     docs_to_search = relevant_docs
    #     docs_map = test1.map_documents()
    #     for doc_name in docs_to_search:
    #         if doc_name in document_texts:
    #             doc_result = self.search_kmp(get_text_doc, pattern) 
	# 			result = doc_result
	# 			total_matches += doc_result['matches_count']
    #     return {
    #         'pattern': pattern,
    #         'total_matches': total_matches,
    #         'documents_found': len(results),
    #         'document_results': result
    #     }

    def search_in_documents_kmp(self, document_texts: Dict[str, str], pattern: str, relevant_docs: List[str] = None) -> Dict:
        results = {}
        total_matches = 0
        docs_to_search = relevant_docs if relevant_docs is not None else list(document_texts.keys())
        
        for doc_name in docs_to_search:
            if doc_name in document_texts:
                doc_result_kmp = self.get_results_kmp(document_texts[doc_name], pattern)
                results[doc_name] = doc_result_kmp # inserting into dict
                total_matches += doc_result_kmp['matches_count']  
           
        return {
            'pattern': pattern,
            'total_matches': total_matches,
            'documents_found': len(results),
            'document_results': results
        }
    
    def search_in_documents_bruteforce(self, document_texts: Dict[str, str], pattern: str, relevant_docs:List[str] = None) -> Dict:
        results = {}
        total_matches = 0
        docs_to_search = relevant_docs if relevant_docs is not None else list(document_texts.keys())
        
        for doc_name in docs_to_search:
            if doc_name in document_texts:
                doc_result_brtfrc = self.get_results_bruteforce(document_texts[doc_name], pattern)
                results[doc_name] = doc_result_brtfrc # inserting into dict
                total_matches += doc_result_brtfrc['matches_count']  
           
        return {
            'pattern': pattern,
            'total_matches': total_matches,
            'documents_found': len(results),
            'document_results': results
        }