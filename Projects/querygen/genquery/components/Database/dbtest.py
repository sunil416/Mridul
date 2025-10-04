from sqlalchemy import create_engine, inspect, text

def test_connection(db_url):
    """Test database connection and return SQLAlchemy engine if successful."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine, "Connection successful"
    except Exception as e:
        return None, f"Connection failed: {e}"

'''
def explore_databases(base_url):
    """
    Connect to the server (no db name specified in base_url),
    list all databases, their tables, and schemas.
    """
    try:
        engine = create_engine(base_url)
        with engine.connect() as conn:
            # This will work for MySQL / MariaDB
            result = conn.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]

        for db in databases:
            print(f"\n=== Database: {db} ===")
            db_engine = create_engine(f"{base_url}{db}")
            inspector = inspect(db_engine)
            tables = inspector.get_table_names()

            for table in tables:
                print(f"  Table: {table}")
                columns = inspector.get_columns(table)
                for col in columns:
                    print(f"    {col['name']} ({col['type']})")

    except Exception as e:
        print(f"Error while exploring databases: {e}")'''
if __name__ == "__main__":
    print(test_connection("mysql+mysqlconnector://root:12345678@localhost/sample2"))
