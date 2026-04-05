import chromadb
from fastapi import APIRouter, HTTPException
from sentence_transformers import SentenceTransformer

from src.app.models.feedback_request import FeedbackRequest
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Access values
MODEL_PATH = config["MODEL_PATH"]
CHROMA_PATH = config["CHROMA_PATH"]
CONFIDENCE_THRESHOLD = config["CONFIDENCE_THRESHOLD"]


router = APIRouter(
    prefix="",       # All routes here will start with /items
    tags=["Items"]         # Tag for Swagger docs
)


model = SentenceTransformer(MODEL_PATH)
client = chromadb.PersistentClient(path=CHROMA_PATH) # type: ignore
collection = client.get_or_create_collection(name="sql_templates")
from src.app.scripts.gemini_service import gemini_reasoner # Import your service

@router.post("/feedback")
async def process_feedback(feedback: FeedbackRequest):
    # CASE 1: User says "No, this is wrong"
    if not feedback.is_correct:
        # Trigger Gemini to analyze the failure
        analysis = gemini_reasoner.analyze_sql_failure(
            user_text=feedback.user_phrase,
            matched_template=feedback.matched_sql or "Unknown",
            extracted_params=feedback.extracted_params or {}
        )
        
        return {
            "status": "ai_correction",
            "analysis": analysis.get("explanation"),
            "suggestion": analysis.get("fix_suggestion"),
            "error_type": analysis.get("error_type")
        }

    # CASE 2: User says "Yes, this is correct" -> System Learns
    # Retrieve original SQL for the template
    original = collection.get(ids=[feedback.template_id])
    if not original["metadatas"] or not original["metadatas"][0]:
        raise HTTPException(status_code=404, detail="Original Template ID not found in Chroma.")
    
    target_sql = original["metadatas"][0]["sql"]
    
    # Generate a unique ID for the new entry
    new_id = f"fb_{feedback.template_id}_{abs(hash(feedback.user_phrase))}"
    
    collection.add(
        ids=[new_id],
        embeddings=[model.encode(feedback.user_phrase).tolist()],
        metadatas=[{"sql": target_sql, "is_feedback": "true"}],
        documents=[feedback.user_phrase]
    )
    
    return {"status": "updated", "message": "System learned from your phrasing!"}