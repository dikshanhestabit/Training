from src.generator.llm_client import LLMClient

# class for generating sql using llm
class SQLGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # creating sql from natural language
    def generate_sql(self, user_query: str, schema_ddl: str, error_msg: str = None) -> str:
        # loading system prompt from file
        with open("src/prompts/sql_gen_system.txt", "r") as f:
            system_prompt = f.read().format(schema_ddl=schema_ddl)
        
        # if error from previous run, try to fix it
        if error_msg:
            user_prompt = f"""
            The previous query failed validation or execution.
            Error: {error_msg}
            Original Intent: {user_query}
            
            Please provide a corrected SQL query that follows the provided schema exactly.
            """
        else:
            # creating normal user prompt
            user_prompt = f"Natural Language Query: {user_query}"
            
        # calling llm client
        sql = self.llm_client.generate_response(system_prompt, user_prompt)
        
        # cleaning up llm output
        sql = sql.replace('```sql', '').replace('```', '').strip()
        
        # fallback if sql is empty or error
        if not sql or "Error" in sql or "FALLBACK" in sql:
            return "SELECT * FROM Customers LIMIT 10;"

        return sql
