import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from download import router as download_router
from download_srt import router as download_srt_router
from video_stream import router as video_router          # ← 추가

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_router)
app.include_router(download_srt_router)
app.include_router(video_router)                          # ← 추가

@app.get("/health")
def health_check():
    return {"status": "ok"}