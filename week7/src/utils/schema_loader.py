import sqlite3
import os
import pandas as pd

# class for loading database schema
class SchemaLoader:
    def __init__(self, db_path: str):
        self.db_path = db_path

    # getting tables and columns for validation
    def get_schema_info(self):
        if not os.path.exists(self.db_path):
            return {}
        
        # connecting to db
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # getting all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        
        schema = {}
        # getting columns for each table
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
            schema[table] = columns
            
        conn.close()
        return schema

    # creating ddl string for llm with sample data
    def get_ddl(self, include_samples=True):
        schema = self.get_schema_info()
        ddl_statements = []
        
        # connecting to db
        conn = sqlite3.connect(self.db_path)
        
        # loops through tables to create create statements
        for table, columns in schema.items():
            cols_str = ", ".join(columns)
            ddl_statements.append(f"CREATE TABLE {table} ({cols_str});")
            
            # adding sample rows to help llm understand data
            if include_samples:
                try:
                    df_sample = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 2", conn)
                    sample_str = df_sample.to_string(index=False)
                    ddl_statements.append(f"-- Sample data for {table}:\n/*\n{sample_str}\n*/")
                except:
                    pass
        
        conn.close()
        return "\n".join(ddl_statements)
