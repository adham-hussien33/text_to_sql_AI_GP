from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    user_text: str = Field(description="The natural language query", examples=["How many students are in CS?"])
