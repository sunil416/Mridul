from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
import openai
from Database.fetchschema import fetch_schema_for_all_databases
# Replace with your MySQL connection details
# The 'mysql' part of the string specifies the dialect, 'mysqlconnector' specifies the driver.
# The 'host' can be 'localhost' or a server IP.
# The 'database' part is optional here, as we are connecting to the server level, but it's good practice to specify it.
def fetch_database(user_query):
    DATABASE_URI = "mysql+mysqlconnector://root:12345678@localhost/"
    SYSTEM_DBS = ["information_schema", "mysql", "performance_schema", "sys"]
    try:
        # Create an engine
        engine = create_engine(DATABASE_URI)

        # Get the inspector for the engine
        inspector = Inspector.from_engine(engine)

        # Use the inspector to get a list of all schema names (databases)
        # This is a more 'SQLAlchemy-native' way to do it
        databases = inspector.get_schema_names()
        L=[]
        print("List of databases:")
        for db in databases:
            if db not in SYSTEM_DBS:
                L.append(db)
                print(type(db))
        print(L)

    except Exception as e:
        print(f"An error occurred: {e}")


    fetch_schema_for_all_databases(DATABASE_URI)

    client = openai.OpenAI(
        api_key="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",
        base_url="https://api.groq.com/openai/v1"
    )
    #user_query = "Today I want to work with the Sample"

    prompt = f"""
    You are given a list of available databases: {L}.
    User query: "{user_query}"

    Your task:
    - Try to find the database name the user is referring to.
    - Consider approximate matches and ignore small differences like underscores, capitalization, or spaces.
    - If the user's intent clearly points to one of the database names, return that name.
    - If none match, return null.

    Use this format (strict JSON only):
    {{
    "database": "<db_name or null>"
    }}
    """


    response = client.responses.create(
        model="llama-3.3-70b-versatile",
        input=prompt,
    )
    print("Full Response:", response)
    # Step 4: Extract clean JSON
    import json
    # Clean the markdown fences if they exist
    cleaned_output = response.output_text.strip()
    if cleaned_output.startswith("```"):
        cleaned_output = cleaned_output.strip("`")
        # Remove possible "json" language tag
        if cleaned_output.startswith("json"):
            cleaned_output = cleaned_output[len("json"):].strip()

    try:
        db_match = json.loads(cleaned_output)["database"]
    except Exception as e:
        print("JSON parse error:", e)
        db_match = None
    return db_match,L
