from tools.code_executor import PythonCodeExecutor
from tools.db_agent import DBAgent
from tools.file_agent import FileAgent

# initializing the agents for the orchestration layer...

class ToolOrchestrator:
    """
    Main Orchestrator Agent for deciding which tool-calling sub-agents to invoke.
    Acts as the 'Planner' to handle complex user queries.
    """

    def __init__(self):
        # initializing agents and toolset...
        self.code_agent = PythonCodeExecutor()
        self.db_agent = DBAgent()
        self.file_agent = FileAgent()

    def route_query(self, user_query: str) -> dict:
        """
        Decision-making logic to map queries to tools based on keywords or intent.
        """
        # writing orchestration logic...
        user_query = user_query.lower()
        print(f"Orchestrating tools for query: '{user_query}'")

        # logic for CSV analysis: Orchestrator assigns File + Code Agents...
        if ".csv" in user_query and ("analyze" in user_query or "insights" in user_query):
            # step 1: use file agent to read CSV...
            print("→ Action: Reading CSV using FileAgent...")
            filename = self._extract_filename(user_query, ".csv")
            data = self.file_agent.read_csv(filename)
            
            # step 2: use code agent to process data...
            print("→ Action: Processing Data using CodeAgent...")
            # adding dynamic python command for calculations...
            code_snippet = f"data = {data}\nprint(f'Insights: Total rows processed: {{len(data)}}')"
            result = self.code_agent.execute(code_snippet)
            
            if result["status"] == "failed":
                return {"error": result["error"], "source": "Code Agent (Failed)"}
                
            return {"result": result["output"], "source": "File + Code Agent Chain"}

        # logic for SQL/Database queries: Orchestrator assigns DB Agent...
        elif "sql" in user_query or "database" in user_query or "table" in user_query:
            print("→ Action: Querying database using DBAgent...")
            # simplified query extraction...
            query = user_query.split("query")[-1].strip()
            result = self.db_agent.query_db(query)
            return {"result": result, "source": "DB Agent"}

        # logic for File/Search queries: Orchestrator assigns File Agent...
        elif "search" in user_query or "find" in user_query:
            print("→ Action: Local search using FileAgent...")
            # improving search term extraction...
            raw_term = user_query.split("search")[-1].strip() if "search" in user_query else user_query.split("find")[-1].strip()
            # removing common filler words like 'for' or 'the'...
            search_term = raw_term.replace("for binary", "").replace("for ", "").replace("the ", "").strip()
            
            results = self.file_agent.local_search(search_term)
            return {"result": f"Found matches in: {results}", "source": "File Agent Search"}

        else:
            return {"error": "No suitable agent found for this query.", "query": user_query}

    def _extract_filename(self, query: str, extension: str) -> str:
        """Helper to find filenames in a string."""
        # writing filename extraction logic...
        for word in query.split():
            if extension in word:
                return word.strip(".,!?;:")
        return "data.csv"

# adding an entry point for execution...
if __name__ == "__main__":
    orchestrator = ToolOrchestrator()
    print("Agent Orchestrator initialized. Ready for user query.")
    # Example: orchestrator.route_query("Analyze sales.csv and generate top 5 insights")
