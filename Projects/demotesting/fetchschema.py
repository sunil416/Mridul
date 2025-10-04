from sqlalchemy import text
import os
from dotenv import load_dotenv
load_dotenv()
#from Database.dbmain import DB_NAME
def get_schema(engine,DBNAME=None):
    """Fetch and return the database schema (tables, columns, data types)."""
    query = text("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :db_name
        ORDER BY table_name, ordinal_position;
    """)

    schema_dict = {}
    with engine.connect() as conn:
        result = conn.execute(query, {"db_name": os.getenv("DBNAME")})
        for table, column, data_type in result:
            schema_dict.setdefault(table, []).append((column, data_type))

    return schema_dict


from sqlalchemy import create_engine, inspect, text

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

