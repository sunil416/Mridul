from sqlalchemy import text
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
load_dotenv()
#from Database.dbmain import DB_NAME
def get_schema(engine):
    """
    Fetches the database schema (tables, columns, data types).
    This function is compatible with PostgreSQL and MySQL.
    """
    
    # Check if the DBNAME environment variable is set
    db_name = os.getenv("DBNAME")
    if not db_name:
        print("Error: The DBNAME environment variable is not set.")
        return {}

    # SQL query to get schema information
    # The 'table_schema' filter is standard for both systems
    query = text("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :db_name
        ORDER BY table_name, ordinal_position;
    """)

    schema_dict = {}
    try:
        with engine.connect() as conn:
            # Pass the database name as a parameter to the query
            result = conn.execute(query, {"db_name": db_name})
            
            for table, column, data_type in result:
                schema_dict.setdefault(table, []).append((column, data_type))
                
    except Exception as e:
        print(f"An error occurred while fetching schema: {e}")
        return {}

    return schema_dict




def fetch_schema_for_all_databases(base_url, db_name=None, exclude_system_schemas=True):
    """
    Fetch only user-defined tables from the given database.
    Returns a dictionary like:
    {'Student': [('Rollnumber','INTEGER'), ('Name','VARCHAR'), ...], ...}
    """

    schema_data = {}

    try:
        # Build DB-specific engine
        if db_name:
            engine = create_engine(f"{base_url}{db_name}")
        else:
            engine = create_engine(base_url)

        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        for schema in schemas:
            # Skip system schemas if requested
            if exclude_system_schemas and schema.lower() in ["information_schema", "performance_schema", "mysql", "sys"]:
                continue

            tables = inspector.get_table_names(schema=schema)

            for table in tables:
                columns = inspector.get_columns(table, schema=schema)
                schema_data[table] = [
                    (col["name"], str(col["type"])) for col in columns
                ]

    except Exception as e:
        print(f"Error fetching schema: {e}")

    return schema_data

