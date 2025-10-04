from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()
from google import genai  # or appropriate import
from sqlalchemy import create_engine, text
import os

client = genai.Client(api_key="<GEMINI_API_KEY>")  # authenticates with the GEMINI_API_KEY

prompt = "select all tables from sample database"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
sql_query = response.text
print("Generated SQL:", sql_query)
# Connection strings for different databases:
connections = {
   # "sqlite": "sqlite:///my_database.db",
    "mysql": f"mysql+mysqlconnector://root:{os.getenv('DatabasePassword')}@localhost/sample",
   # "postgresql": "postgresql+psycopg2://user:password@localhost/mydb",
    #"mssql": "mssql+pyodbc://user:password@localhost/mydb?driver=ODBC+Driver+17+for+SQL+Server"
}

# Pick which DB you want to connect to:
db_url = connections["mysql"]   # change "sqlite" -> "mysql" / "postgresql" / "mssql"

# Create engine
engine = create_engine(db_url)

# Use connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Query result:", result.scalar())
