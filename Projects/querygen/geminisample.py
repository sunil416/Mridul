from openai import OpenAI
from sample1frontend import call_generate_query, call_run_query
import json
from genquery.components.Database.dbmain import connect_to_database
from genquery.components.Database.connectionlist import get_connection_string
#from Database.dbtest import test_connection
from genquery.components.Database.fetchschema import get_schema , fetch_schema_for_all_databases
from genquery.components.Prompts.SystemPrompt import SQL_ASSISTANT_PROMPT
def llm(user_input: str) -> str:
  client = OpenAI(
      api_key="AIzaSyCcxSXCnCWl_asxRlzZf4WAhDrz9oC4eBc",
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

  tools = [
    {
      "type": "function",
      "function": {
        "name": "call_generate_query",
        "description": "This function generates a SQL query based on the user request",
        "parameters": {
          "type": "object",
          "properties": {
            "user_input": {
              "type": "string",
              "description": "It is user request what they want to do regarding database"
            }
          },
          "required": ["user_input"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "call_run_query",
        "description": "This function executes a SQL query against the database",
        "parameters": {
          "type": "object",
          "properties": {
            "sql_query": {
              "type": "string",
              "description": "It is the SQL query to be executed"
            }
          },
          "required": ["sql_query"]
        }
      }
    }
  ]

  engine = connect_to_database("mysql")
  schema = get_schema(engine)
  print(schema)
  #user_input = "i want to see how many suppliers are there in total"
  Prompt = SQL_ASSISTANT_PROMPT.format(schema=schema, request=user_input)
  print(Prompt)
  messages = [
    {
      "role": "system",
      "content": Prompt
    },
    {
      "role": "user",
      "content": user_input
    }
  ]

  response = client.chat.completions.create(
      model="gemini-2.0-flash",
      messages=messages,
      tools=tools,
      tool_choice="auto"
  )

  msg = response.choices[0].message
  print("Full Response:", msg)
  # Step 1: Check if model called a tool
  if msg.tool_calls:
      for tool_call in msg.tool_calls:
          fn_name = tool_call.function.name
          fn_args = json.loads(tool_call.function.arguments)

          if fn_name == "call_generate_query":
              # Generate SQL
              sql_query = call_generate_query(fn_args["user_input"])
              print("Generated SQL:", sql_query)
              # Step 2: Feed SQL into run_query tool
              run_result = call_run_query(sql_query)
              return run_result
          if fn_name == "call_run_query":
              # Step 2: Feed SQL into run_query tool
              run_result = call_run_query(fn_args["sql_query"])
              return run_result
if __name__ == "__main__":
    query="SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE();"
    result = llm(query)
    print(type(result))
    print("Query Result:", result)