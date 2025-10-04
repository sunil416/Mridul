from dotenv import load_dotenv
import sqlparse
import os
load_dotenv()
import google.generativeai as genai
#from Models.queryrequest import QueryRequest
from genquery.components.Database.dbmain import connect_to_database
from genquery.components.Database.connectionlist import get_connection_string
#from Database.dbtest import test_connection
from genquery.components.Database.fetchschema import get_schema , fetch_schema_for_all_databases
#from genquery.components.syntaxcheck import clean_sql_output , validate_sql_syntax
import re
from genquery.components.Prompts.Prompt import Prompt
#from genquery.components.Database.sample1 import fetch_database
from sqlalchemy import create_engine, text
# Load environment variables from .env file
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DatabasePassword")
''''
get_connection_string("mysql", DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)  # Example for MySQL
engine, success = test_connection(get_connection_string("mysql", DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
if isinstance(engine, str):
    raise ConnectionError(f"Database connection failed: {engine}")
else:
    print(success)  

schema = get_schema(engine=engine, DB_NAME=DB_NAME)
print(schema)  '''
'''
#from google import genai
'''
'''
DB_TYPE=input("DB YOU'RE CURRENTLY USING")
    DB_USER=input()
    DB_PASSWORD=input()
    DB_HOST=input()
'''
def list_databases(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SHOW DATABASES;"))
        return [row[0] for row in result]
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
def quer_gen(request:str):
    #db_name,L = fetch_database(request)
    #print(f"Database matched: {db_name}")
   # os.environ["DBNAME"]=db_name
    engine = connect_to_database("mysql")
    #base_url=get_connection_string("mysql","root","12345678","localhost")
    #print(base_url)
    #print(fetch_schema_for_all_databases(base_url))
    #DB_Name=input("Enter DB you want to work on")
    print(engine)
    #print(list_databases(engine))
    schema = get_schema(engine)
    print(schema)
    #whole_schema=fetch_schema_for_all_databases(engine.url)
    print(Prompt.format(schema=schema,request=request))
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    models=genai.GenerativeModel("gemini-2.5-flash")
    #prompt="Show all tables from my database"
    #full_prompt = f"Given the following database schema:\n{schema}\n\nGenerate an SQL query for the following request:\n{request}\n\nSQL Query:"
    response = models.generate_content(
        Prompt.format(schema=schema,request=request)
    )
    '''
    output=clean_sql_output(response.text)
    if validate_sql_syntax(output):
        print("Valid SQL syntax")
    else:
        raise ValueError("Generated SQL query has invalid syntax.")'''
    return response.text
if __name__ == "__main__":
    # Example usage
    request = "i want to check which employee worked less than 8hrs on 18th september 2025 "
    sql_query = quer_gen(request)
    print("Generated SQL Query:", sql_query)