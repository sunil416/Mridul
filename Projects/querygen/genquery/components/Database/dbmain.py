from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from genquery.components.Database.dbtest import test_connection
from genquery.components.Database.connectionlist import get_connection_string
from genquery.components.Database.dbrun import execute_query
from genquery.components.Database.fetchschema import get_schema, fetch_schema_for_all_databases
# Load Enviroment variables from .env file
load_dotenv()

DB_NAME = os.getenv("DBNAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DatabasePassword")
# Connection strings for different databases:
def connect_to_database(db_type: str):
    engine, success = test_connection(get_connection_string(db_type, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))    
    if isinstance(engine, str):
        raise ConnectionError(f"Database connection failed: {engine}")
    else:
        print(success)
    return engine
# Connection strings for different databases:
'''connections = {
   "sqlite": "sqlite:///my_database.db",
    "mysql": f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    "postgresql": "postgresql+psycopg2://user:password@localhost/mydb",
    "mssql": "mssql+pyodbc://user:password@localhost/mydb?driver=ODBC+Driver+17+for+SQL+Server"
}'''

'''def test_connection(db_url):
    """Test database connection."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)
        
   '''
if __name__ == "__main__":
    # Pick which DB you want to connect to:
    db=input("Enter the database you want to connect to (mysql/sqlite/postgresql/mssql): ").strip().lower()
    db_url =get_connection_string(db,DB_USER,DB_PASSWORD,DB_HOST, DB_NAME) 
    print(db_url)  # change "sqlite" -> "mysql" / "postgresql" / "mssql"
    print(f"Connecting to {db} database...")
    engine,success=test_connection(db_url)
    print(success)
    print(fetch_schema_for_all_databases(db_url))
    #print(get_schema(engine,DB_NAME))
    # Use connection
   # print(execute_query(engine, f"SHOW TABLES FROM {DB_NAME}")  )# replace with your query