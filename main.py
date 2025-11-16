import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Lead, Project

app = FastAPI(title="Money By Tej API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Money By Tej API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# ------------------- Leads ---------------------
class LeadIn(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    message: Optional[str] = None

@app.post("/api/leads")
async def create_lead(payload: LeadIn):
    try:
        lead = Lead(**payload.model_dump())
        inserted_id = create_document("lead", lead)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/leads")
async def list_leads(limit: int = 50):
    try:
        docs = get_documents("lead", {}, limit)
        # Convert ObjectId to str for frontend
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return {"ok": True, "items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- Projects ---------------------
class ProjectIn(BaseModel):
    name: str
    location: Optional[str] = None
    developer: Optional[str] = None
    ownership_options: Optional[List[str]] = None
    investment_starts_from: Optional[str] = None
    benefits: Optional[List[str]] = None
    photos: Optional[List[str]] = None
    map_embed_url: Optional[str] = None

@app.post("/api/projects")
async def create_project(payload: ProjectIn):
    try:
        project = Project(**payload.model_dump())
        inserted_id = create_document("project", project)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/projects")
async def list_projects(limit: int = 20):
    try:
        docs = get_documents("project", {}, limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return {"ok": True, "items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
