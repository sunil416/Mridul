from sqlalchemy import create_engine, text
import pandas as pd
def execute_query(engine, query):
    """Execute a SQL query and return the results or a message."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(query))

            # Check if the query is a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                # For SELECT, fetch and return the rowszzz
                rows = result.fetchall()
                df = pd.DataFrame([dict(row._mapping) for row in rows])
                return {"type": "table", "data": df.to_dict(orient="records")}
            else:
                # For INSERT, UPDATE, DELETE, commit the transaction and return rowcount
                connection.commit()
                print(f"Query executed successfully. Rows affected: {result.rowcount}")
                return {"message": "Query executed successfully", "rows_affected": result.rowcount}
        
        except Exception as e:
            # Handle potential errors during query execution
            print(f"An error occurred: {e}")
            return {"error": str(e)}
if __name__ == "__main__":
    # Example usage
    engine = create_engine("mysql+mysqlconnector://root:12345678@localhost/sample3")  # Replace with your actual database URL
    query = "SELECT * FROM orders;"  # Replace with your actual query
    results = execute_query(engine, query)
    print(results)