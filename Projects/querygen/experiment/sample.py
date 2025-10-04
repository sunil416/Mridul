from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()

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
