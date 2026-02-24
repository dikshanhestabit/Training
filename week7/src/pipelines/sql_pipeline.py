import sqlite3
import pandas as pd
import re
import logging
from datetime import datetime
from src.utils.schema_loader import SchemaLoader
from src.generator.sql_generator import SQLGenerator
from src.generator.llm_client import LLMClient

# setting up logging for query audit
logging.basicConfig(
    filename='src/logs/query_audit.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# main pipeline class
class SQLPipeline:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.loader = SchemaLoader(db_path)
        self.llm = LLMClient()
        self.generator = SQLGenerator(self.llm)

    # redacting sensitive info like emails and phones
    def redact_pii(self, text: str) -> str:
        # redacting emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', text)
        # redacting phone numbers
        text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE]', text)
        return text

    # validating sql before execution
    def validate_sql(self, sql: str, schema_map: dict):
        import sqlglot
        from sqlglot import exp

        # checking for forbidden commands
        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
        for cmd in forbidden:
            if re.search(rf"\b{cmd}\b", sql.upper()):
                return False, f"Security Violation: Forbidden command '{cmd}'"

        try:
            # parsing sql to check columns and tables
            parsed = sqlglot.parse_one(sql)
            
            all_valid_tables = {t.lower() for t in schema_map.keys()}
            all_valid_columns = {c.lower() for cols in schema_map.values() for c in cols}

            # checking if columns exist in schema
            for column in parsed.find_all(exp.Column):
                col_name = column.this.name.lower()
                if col_name not in all_valid_columns:
                    return False, f"Schema Error: Column '{col_name}' not found."

            # checking if tables exist in schema
            for table in parsed.find_all(exp.Table):
                tbl_name = table.this.name.lower()
                if tbl_name not in all_valid_tables:
                    return False, f"Schema Error: Table '{tbl_name}' not found."

            return True, "Valid"
        except Exception as e:
            return False, f"SQL Syntax Error: {str(e)}"

    # running end to end logic
    def run(self, user_query: str):
        # logging request
        logging.info(f"Incoming Request: {user_query}")
        
        # redacting pii
        safe_query = self.redact_pii(user_query)
        if safe_query != user_query:
            logging.info(f"PII Redacted: {safe_query}")

        # loading schema
        schema_ddl = self.loader.get_ddl()
        schema_map = self.loader.get_schema_info()
        
        # generating sql
        sql = self.generator.generate_sql(safe_query, schema_ddl)
        logging.info(f"Generated SQL: {sql}")
        
        # validating sql
        is_valid, msg = self.validate_sql(sql, schema_map)
        if not is_valid:
            logging.warning(f"Validation Failure: {msg}")
            # trying to self correct once
            sql = self.generator.generate_sql(safe_query, schema_ddl, error_msg=msg)
            is_valid, msg = self.validate_sql(sql, schema_map)
            if not is_valid:
                return {"error": f"Policy Violation: {msg}"}

        # executing sql on db
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            
            # summarizing results
            summary = self.summarize_results(safe_query, sql, df)
            logging.info("Query successfully handled.")
            return {"sql": sql, "data": df.to_dict(orient='records'), "summary": summary}
        except Exception as e:
            logging.error(f"Runtime Error: {str(e)}")
            return {"error": str(e)}

    # creating summary of data using llm
    def summarize_results(self, query, sql, df):
        # loading system prompt for summary
        with open("src/prompts/summary_system.txt", "r") as f:
            system_prompt = f.read()
            
        # loading user prompt template
        with open("src/prompts/summary_user_template.txt", "r") as f:
            user_prompt = f.read().format(query=query, sql=sql, df_str=df.to_string())
            
        return self.llm.generate_response(system_prompt, user_prompt)

if __name__ == "__main__":
    # connecting to customer db
    db_path = "src/data/customers.db"
    
    pipeline = SQLPipeline(db_path)
    
    # testing with sample queries
    test_queries = [
        "How many customers are from Chile?",
        "Show me the first 5 customers who subscribed in 2021",
        "Which companies are located in 'East Leonard'?"
    ]
    
    for q in test_queries:
        print(f"\n>>> Query: {q}")
        result = pipeline.run(q)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"SQL: {result['sql']}")
            print(f"Answer: {result['summary']}")
