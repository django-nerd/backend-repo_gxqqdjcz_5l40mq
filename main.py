import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import create_document
from schemas import Lead

app = FastAPI(title="Ecom Content Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Agency backend running"}

@app.get("/test")
def test_database():
    """Simple test to verify DB env is set"""
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
    }
    return response

class LeadResponse(BaseModel):
    id: str
    status: str

@app.post("/leads", response_model=LeadResponse)
async def create_lead(lead: Lead):
    """Capture contact form submissions and store in MongoDB (collection: lead)."""
    try:
        inserted_id = create_document("lead", lead)
        return {"id": inserted_id, "status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
