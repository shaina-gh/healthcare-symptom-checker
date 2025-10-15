# main.py (Corrected Version)
import os
from dotenv import load_dotenv

# --- FIX ---
# Load environment variables from the .env file at the very beginning.
# This ensures the API key is available for all other imported files.
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm_service import get_llm_analysis
from database import save_check, get_all_checks, init_db

# Initialize the database on startup
init_db()

app = FastAPI()

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # The default Vite/React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Input/Output Validation ---
class SymptomCheckRequest(BaseModel):
    symptoms: str

class SymptomCheck(BaseModel):
    id: int
    symptoms: str
    response: str
    created_at: str

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Healthcare Symptom Checker API"}

@app.post("/check_symptoms")
async def check_symptoms(request: SymptomCheckRequest):
    """
    Accepts user symptoms, gets analysis from an LLM, and saves the interaction.
    """
    if not request.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty.")

    try:
        # Get analysis from our LLM service
        llm_response_json = await get_llm_analysis(request.symptoms)

        # Save the interaction to the database
        save_check(symptoms=request.symptoms, response=llm_response_json)

        return llm_response_json
    except Exception as e:
        # Generic error handler to catch issues with the LLM call
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/history", response_model=list[SymptomCheck])
async def get_history():
    """
    Retrieves all past symptom checks from the database.
    """
    history = get_all_checks()
    return history