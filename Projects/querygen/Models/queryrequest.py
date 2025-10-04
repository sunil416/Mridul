from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str
    #database: Optional[str] = None
    #tables: Optional[List[str]] = None
    #columns: Optional[List[str]] = None
    #conditions: Optional[str] = None    
