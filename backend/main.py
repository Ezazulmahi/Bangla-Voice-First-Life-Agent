from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from routers import audio, auth, conversations, reminders, tools

app = FastAPI(title="Sohai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    # Raised by voice/stt.py and agents/llm.py when GROQ_API_KEY is missing —
    # surface it as a clear 503 instead of an opaque 500.
    return JSONResponse(status_code=503, content={"detail": str(exc)})

app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")

app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(audio.router)
app.include_router(tools.router)
app.include_router(reminders.router)


@app.get("/health")
def health():
    return {"status": "ok"}
