import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add project root to sys.path so `python server/app.py` works directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from server.kernel.runtime_config import runtime
from server.store.sqlite_store import bootstrap_store
from server.routes import scan, reviews, corpora, engines, tuning, equity, trials, briefs, preferences

from starlette.middleware.base import BaseHTTPMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database schema on startup
    bootstrap_store()
    yield

app = FastAPI(
    title="CivilLens: Transparent, Feedback-Tuned Screening of Abusive Online Language",
    description="CivilLens research console: explainable, feedback-tuned screening of abusive online language",
    version="1.0.0",
    lifespan=lifespan
)

class FreshOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(FreshOnlyMiddleware)

# Enable CORS for local research interfaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(scan.router)
app.include_router(reviews.router)
app.include_router(corpora.router)
app.include_router(engines.router)
app.include_router(tuning.router)
app.include_router(equity.router)
app.include_router(trials.router)
app.include_router(briefs.router)
app.include_router(preferences.router)

# Mount web console assets
web_root = runtime.base_dir / "web"
if web_root.exists():
    app.mount("/assets", StaticFiles(directory=str(web_root)), name="assets")
    if (web_root / "styles").exists():
        app.mount("/styles", StaticFiles(directory=str(web_root / "styles")), name="styles")
    if (web_root / "scripts").exists():
        app.mount("/scripts", StaticFiles(directory=str(web_root / "scripts")), name="scripts")

pitch_dir = runtime.base_dir / "pitch"
if pitch_dir.exists():
    app.mount("/pitch", StaticFiles(directory=str(pitch_dir)), name="pitch")

visuals_dir = runtime.base_dir / "corpus" / "source" / "visuals"
if visuals_dir.exists():
    app.mount("/corpus/source/visuals", StaticFiles(directory=str(visuals_dir)), name="corpus_visuals")

@app.get("/")
def serve_home():
    home_file = runtime.base_dir / "web" / "home.html"
    if home_file.exists():
        return FileResponse(str(home_file))
    return {"message": "CivilLens API is live. Open /docs for the interactive API reference."}

@app.get("/pulse")
def pulse():
    return {
        "status": "healthy",
        "app": "CivilLens: Transparent, Feedback-Tuned Screening of Abusive Online Language",
        "device": runtime.device,
        "database": str(runtime.database_path)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)
