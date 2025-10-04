from dotenv import load_dotenv
import os
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DatabasePassword")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DBNAME")

def get_connection_string(db_type, user=None, password=None, host=None, dbname=None):
    """
    Build a SQLAlchemy connection string dynamically.
    db_type: one of "sqlite", "mysql", "postgresql", "mssql"
    """

    if db_type == "sqlite":
        # SQLite does not use user/pass/host
        return f"sqlite:///{dbname or 'my_database.db'}"

    elif db_type == "mysql":
        return f"mysql+mysqlconnector://{user}:{password}@{host}/{dbname or ''}"

    elif db_type == "postgresql":
        return f"postgresql+psycopg2://{user}:{password}@{host}/{dbname or ''}"

    elif db_type == "mssql":
        return f"mssql+pyodbc://{user}:{password}@{host}/{dbname or ''}?driver=ODBC+Driver+17+for+SQL+Server"

    else:
        raise ValueError(f"Unsupported db_type: {db_type}")
    
if __name__ == "__main__":
    # Example usage:
   # print(get_connection_string("sqlite", dbname="example.db"))
    print(get_connection_string("mysql", DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
    #print(get_connection_string("postgresql", DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
    #print(get_connection_string("mssql", DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
