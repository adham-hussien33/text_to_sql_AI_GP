from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    template_id: str = Field(..., description="The ID of the SQL template from ChromaDB")
    user_phrase: str = Field(..., description="The original natural language text typed by the user")
    is_correct: bool = Field(..., description="True if the user liked the result, False otherwise")
    
    # Context fields needed for Gemini reasoning
    matched_sql: Optional[str] = Field(None, description="The final SQL query that was shown to the user")
    extracted_params: Optional[Dict[str, Any]] = Field(None, description="The variables spaCy extracted (e.g., {'email': 'test@test.com'})")