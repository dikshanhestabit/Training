from src.generator.llm_client import LLMClient
import re
import json

class RAGEvaluator:
    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    def evaluate_response(self, query: str, context: str, answer: str):
        """Perform a multi-point evaluation of the generated answer."""
        
        system_prompt = """You are an expert RAG auditor. Evaluate the answer based on the context.
Return your evaluation in STRICT JSON format with these exact keys:
- "hallucination_detected": boolean (true if answer contains facts NOT in context)
- "faithfulness_score": float (0 to 1, how much of the answer is supported by context)
- "confidence_score": float (0 to 1, how confident you are in this answer)
- "context_relevance": float (0 to 1, how relevant the context was to the query)
- "critique": string (brief explanation of scores)
"""

        user_prompt = f"""
Query: {query}
Context: {context}
Answer: {answer}

Perform the evaluation now."""

        response_text = self.llm.generate_response(system_prompt, user_prompt)
        
        try:
            # Extract JSON from response if LLM wraps it in backticks
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response_text)
        except Exception as e:
            print(f"Evaluation Parsing Error: {str(e)}")
            return {
                "hallucination_detected": False,
                "faithfulness_score": 0.5,
                "confidence_score": 0.5,
                "context_relevance": 0.5,
                "critique": f"Failed to parse evaluation: {str(e)}"
            }

if __name__ == "__main__":
    # Internal test logic
    evaluator = RAGEvaluator()
    sample_query = "What is the capital of France?"
    sample_context = "Paris is the capital and largest city of France."
    sample_answer = "The capital of France is Paris. It is also famous for the Eiffel Tower."
    
    metrics = evaluator.evaluate_response(sample_query, sample_context, sample_answer)
    print("Evaluation Metrics:")
    print(json.dumps(metrics, indent=4))
