from fastapi import FastAPI,HTTPException
from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse
#from fastapi.responses import JSONResponse
from Models.queryrequest import QueryRequest
from genquery.components.querygenerator import quer_gen
from genquery.components.Database.connectionlist import get_connection_string
from genquery.components.Database.dbmain import connect_to_database
from genquery.components.Database.dbrun import execute_query
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

#BASE_URL = "mysql+pymysql://username:password@localhost/"
'''
@app.get("/list-databases/")
def list_databases():
    try:
        engine = connect_to_database("mysql")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]
        return {"databases": databases}
    except Exception as e:
        return {"error": str(e)}

@app.get("/list-tables/{db_name}")
def list_tables(db_name: str):
    try:
        #os.environ["DBNAME"]=db_name
        engine = connect_to_database("mysql",db_name)
        #os.environ["engine"]=engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        os.environ["DBNAME"]=db_name
        #os.environ["engine"]=engine
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}
'''

HTML_FOLDER = "/Users/softsuave/Projects/querygen/templates"

@app.get("/", response_class=HTMLResponse)
def read_html_file():
    file_path = os.path.join(HTML_FOLDER, "chat.html")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/generate-query/")
async def generate_query(request: QueryRequest):
    sql_query = quer_gen(request)
    if sql_query:
        return {"query": sql_query}
    else:
        return {"error": "Failed to generate SQL query"}
    


@app.post("/run-query/")
def run_query(query: str = Body(...)):
    query = query.strip().lower()
    engine = create_engine(get_connection_string("mysql", "root", "12345678", "localhost", os.getenv("DBNAME")))
    # Special handling: show tables
    if "show tables" in query or "from information_schema.tables" in query or "from information_schema.columns" in query:
        try:
            #engine=create_engine(get_connection_string("mysql","root","12345678","localhost",os.getenv("DBNAME")))
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                )
                tables = [row[0] for row in result.fetchall()]
                return {"type": "tables", "data": tables}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # General query execution
    return execute_query(engine, query)
'''
@app.post("/execute-query/")
def execute(request: QueryRequest):
    try:
        engine = connect_to_database("mysql")
        result = execute_query(engine, request)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
