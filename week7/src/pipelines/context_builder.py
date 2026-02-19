import hashlib
from typing import List, Dict

class ContextBuilder:
    def __init__(self, max_chars: int = 4000):
        # Initializing context settings
        self.max_chars = max_chars

    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        # Removing duplicate chunks
        seen_hashes = set()
        unique_results = []
        
        for res in results:
            content = res['metadata']['text']
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_results.append(res)
        
        return unique_results

    def build_context(self, results: List[Dict]) -> str:
        # Building context from results
        unique_results = self._deduplicate(results)
        
        context_blocks = []
        current_length = 0
        
        for i, res in enumerate(unique_results):
            source = res['metadata'].get('source', 'Unknown Source')
            text = res['metadata']['text']
            
            # Formatting with traceability
            block = f"--- [SOURCE {i+1}]: {source} ---\n{text}\n"
            
            if current_length + len(block) > self.max_chars:
                print(f"Warning: Context limit reached. Truncating at {i} sources.")
                break
                
            context_blocks.append(block)
            current_length += len(block)
            
        return "\n".join(context_blocks)

if __name__ == "__main__":
    # Test harness
    builder = ContextBuilder(max_chars=1000)
    
    mock_results = [
        {"metadata": {"text": "Credit underwriting is a verification process.", "source": "policy_2024.pdf"}},
        {"metadata": {"text": "Credit underwriting is a verification process.", "source": "policy_duplicate.pdf"}}, # Duplicate content
        {"metadata": {"text": "Underwriters check credit scores and history.", "source": "manual_v1.pdf"}}
    ]
    
    context = builder.build_context(mock_results)
    print("\n--- Formatted Context ---")
    print(context)
    
    print("\n--- Verification ---")
    print(f"Duplicates removed: {'Yes' if 'policy_duplicate.pdf' not in context else 'No'}")
    print(f"Traceability present: {'Yes' if '[SOURCE 1]' in context else 'No'}")
