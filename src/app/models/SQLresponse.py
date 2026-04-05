from typing import Dict, Optional
from pydantic import BaseModel, Field

class SQLResponse(BaseModel):
    matched_sql: Optional[str] = None
    template_id: Optional[str] = None
    distance: Optional[float] = None
    status: str
    message: str
    extracted_params: Optional[Dict[str, str]] = None