import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool

from stt import analyze_stt
from fastapi.middleware.cors import CORSMiddleware
#서버 가동
#uvicorn main:app --host 0.0.0.0 --port 8000
#test
#curl -X POST "http://localhost:8000/stt" -F "file=@파일 경로"
app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/stt")
async def stt(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "")[-1]

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp_path = temp.name
            temp.write(await file.read())

        result = await run_in_threadpool(analyze_stt, temp_path)

        return {
            "filename": file.filename,
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI/main.py

import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool

from stt import analyze_stt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/stt")
async def stt(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "")[-1]
    temp_path = None

    logger.info("STT request received: filename=%s, content_type=%s", file.filename, file.content_type)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp_path = temp.name
            content = await file.read()
            temp.write(content)

        logger.info("Uploaded file saved: path=%s, size=%d bytes", temp_path, len(content))

        result = await run_in_threadpool(analyze_stt, temp_path)

        logger.info("STT analysis completed: segments=%d", len(result))

        return {
            "success": True,
            "filename": file.filename,
            "result": result,
        }

    except Exception as e:
        logger.exception("STT analysis failed")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info("Temporary file deleted: path=%s", temp_path)

@app.get("/")
def root():
    return {"message": "STT API server is running"}