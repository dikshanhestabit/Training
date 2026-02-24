import json
from src.retriever.integrated_rag import IntegratedRAG
from src.memory.memory_store import MemoryStore
from src.evaluation.rag_eval import RAGEvaluator
from src.generator.llm_client import LLMClient

class AdvancedRAG:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        self.rag_engine = IntegratedRAG(config_path)
        self.memory = MemoryStore()
        self.evaluator = RAGEvaluator()
        self.llm = LLMClient(config_path)

    def run(self, query: str):
        # 1. Retrieve Conversation History
        history = self.memory.get_context_string()
        
        # 2. Retrieval Step
        context, hits = self.rag_engine.run(query)
        
        # 3. Initial Generation
        system_prompt = "You are a helpful assistant. Use the provided context and conversation history to answer the user query."
        user_prompt = f"History:\n{history}\n\nContext:\n{context}\n\nQuestion: {query}"
        
        answer = self.llm.generate_response(system_prompt, user_prompt)
        
        # 4. Evaluation Loop
        metrics = self.evaluator.evaluate_response(query, context, answer)
        
        # 5. Refinement Loop (Self-Critique)
        if metrics.get("hallucination_detected", False) or metrics.get("faithfulness_score", 0) < 0.7:
            print("\n!!! Low Faithfulness or Hallucination Detected. Refining...")
            refine_prompt = f"""The previous answer was critiqued as follows: {metrics.get('critique')}
            
Please regenerate the answer ensuring it is strictly grounded in the context provided.
Context: {context}
Question: {query}"""
            
            answer = self.llm.generate_response("You are a self-correcting RAG agent.", refine_prompt)
            # Re-evaluate final version
            metrics = self.evaluator.evaluate_response(query, context, answer)
        
        # 6. Update Memory
        self.memory.add_message("user", query)
        self.memory.add_message("assistant", answer)
        
        return {
            "answer": answer,
            "metrics": metrics,
            "sources": [h['metadata'].get('source', 'unknown') for h in hits]
        }

if __name__ == "__main__":
    adv_rag = AdvancedRAG()
    result = adv_rag.run("Tell me about the recent company performance")
    print("\n--- Final Answer ---")
    print(result['answer'])
    print("\n--- Metrics ---")
    print(json.dumps(result['metrics'], indent=4))
