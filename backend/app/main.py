from fastapi import FastAPI, Depends, HTTPException, Response, UploadFile, File
from contextlib import asynccontextmanager
import os
from datetime import datetime
from pathlib import Path
from .db import create_db_and_tables, get_session
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, text
import time
from fastapi.security import OAuth2PasswordRequestForm
from .auth import authenticate_user, create_access_token, get_current_user
from .chat import chat_with_agent, ChatRequest
import re

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://aayushbot-v3.vercel.app",  # Production frontend on Vercel
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database and tables if not...")
    create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """
    Root endpoint - accessible from both local and production.
    Returns basic server information.
    """
    return {
        "status": "running",
        "service": "Aayushmaan Bot API",
        "version": "3.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "admin": "/admin",
            "docs": "/docs",
        },
        "message": "Welcome to Aayushmaan's AI Bot API! 🤖",
    }


@app.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        start_time = time.time()
        result = session.exec(text("SELECT 1")).first()
        latency_ms = (time.time() - start_time) * 1000

        return {
            "server": "running successfully 🎉",
            "timestamp": datetime.now().isoformat(),
            "database": {"connected": True, "latency_ms": round(latency_ms, 2)},
        }
    except Exception as e:
        # If database fails, return error
        raise HTTPException(
            status_code=503,
            detail={
                "server": "running but database error",
                "timestamp": datetime.now().isoformat(),
                "database": {"connected": False, "error": str(e)},
            },
        )


@app.post("/admin")
def get_access(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = authenticate_user(db, form.username, form.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    create_access_token(data={"sub": str(user.id)}, response=response)
    return {"access": "granted"}


@app.get("/admin")
def verify_admin(user_id: str = Depends(get_current_user)):
    return {"ok": True, "user_id": user_id}


@app.post("/admin/upload")
async def upload_admin_pdf(
    pdf: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
):
    if pdf.content_type not in ("application/pdf", "application/x-pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Store uploads in backend/upload (repo-friendly location)
    backend_dir = Path(__file__).resolve().parents[1]
    uploads_dir = backend_dir / "upload"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    original_name = (pdf.filename or "document.pdf").split("/")[-1].split("\\")[-1]
    # Sanitize filename to avoid path traversal / weird filesystem chars
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", original_name).strip("._")
    if not safe_name:
        safe_name = "document.pdf"
    if not safe_name.lower().endswith(".pdf"):
        safe_name = f"{safe_name}.pdf"

    # Save with the same (sanitized) filename as uploaded. If it already exists, overwrite.
    target = uploads_dir / safe_name

    contents = await pdf.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    target.write_bytes(contents)

    # Trigger RAG pipeline to process the uploaded file
    try:
        # Import the RAG upload function
        import sys

        agents_dir = backend_dir / "agents"
        if str(agents_dir) not in sys.path:
            sys.path.insert(0, str(agents_dir))

        from rag import upload_documents, clear_pinecone_index  # type: ignore

        # Clear all existing data from Pinecone before uploading new file
        print("🗑️  Clearing existing data from Pinecone...")
        clear_pinecone_index()

        # Process the uploaded PDF with RAG pipeline
        print(f"📤 Uploading new document: {safe_name}")
        document_ids = upload_documents(str(target))
        rag_status = {
            "processed": True,
            "chunks_uploaded": len(document_ids),
            "cleared_old_data": True,
        }
    except Exception as e:
        # Log error but don't fail the upload
        print(f"❌ RAG pipeline error: {str(e)}")
        rag_status = {
            "processed": False,
            "error": str(e),
        }

    return {
        "ok": True,
        "uploaded_by": user_id,
        "filename": safe_name,
        "stored_as": target.name,
        "size_bytes": len(contents),
        "rag_pipeline": rag_status,
    }


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=os.getenv("COOKIE_NAME", "access_token"), path="/")
    return {"ok": True}


@app.post("/admin/reset-agent")
async def admin_reset_agent(user_id: str = Depends(get_current_user)):
    """
    Admin endpoint to manually reset the agent.
    Forces agent to reinitialize with latest prompt on next chat request.
    """
    await reset_agent()
    return {
        "ok": True,
        "message": "Agent reset successfully. Will reinitialize with latest prompt on next chat.",
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint using the unified agent.
    Supports conversation threads and maintains context.
    """
    return await chat_with_agent(request)


if __name__ == "__main__":
    import uvicorn

    # Run with module notation since we use relative imports
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
