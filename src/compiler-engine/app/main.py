from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import os
import requests
import docker
from urllib.parse import quote
import base64
from urllib.parse import quote, urlparse

app = FastAPI(
    title="Compiler Engine",
    version="1.0",
)
GITLAB_API_URL = os.getenv("GITLAB_API_URL")
gitlab_api_headers = {"PRIVATE-TOKEN": os.getenv("GROUP_ACCESS_TOKEN")}

# Pydantic models for request bodies and responses

class Board(BaseModel):
    core: str
    variant: str

class StadardCompileRequest(BaseModel):
    git_repo_url: str
    board: Board
    libraries: List[str]
    custom_flags: Optional[Dict[str, str]] = None

class CustomCompileRequest(BaseModel):
    git_repo_url: str
    docker_image: str
    registry_auth_token: str
    custom_flags: Optional[Dict[str, str]] = None

class CompileStatus(str, Enum):
    pending = "pending"
    running = "running"
    error = "error"
    successful = "successful"
    delivered = "delivered"

class Status(BaseModel):
    status: CompileStatus


# Endpoints for standard compile
@app.post("/compile", tags=["Compile standard"])
async def compile_standard(request: StadardCompileRequest):
    request.git_repo_url = convert_gilab_url(request.git_repo_url)
    # Business logic placeholder:
    # - Clone the repo from request.git_repo_url
    # - Use request.board, request.libraries, and request.custom_flags with the built-in toolchain (arduino-cli)
    # - Initiate a compile job and generate a job_id and timestamp.
    return {"job_id": 10, "timestamp": "2021-10-10T10:10:10Z", "gitlab_url": request.git_repo_url}

@app.get("/compile/{job_id}/status", tags=["Compile standard"])
async def get_compile_status(job_id: int):
    # Business logic placeholder:
    # - Retrieve the status of the compile job from your database or in-memory store.
    # - Validate job_id and return appropriate status.
    return {"status": CompileStatus.running}

@app.get("/compile/{job_id}/artefacts", tags=["Compile standard"])
async def get_compile_artefacts(
    job_id: int,
    get_source_code: bool = Query(False, description="Include the source code in the artefacts"),
    get_logs: bool = Query(False, description="Include the logs in the artefacts")
):
    # Business logic placeholder:
    # - Retrieve artefacts for the given job_id.
    # - Optionally include source code and logs based on query parameters.
    # - Package artefacts into a zip file.
    dummy_zip_path = "dummy.zip"  # Replace with the actual artefact zip file path.
    try:
        return FileResponse(dummy_zip_path, media_type="application/zip", filename="artefacts.zip")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoints for custom compile

@app.post("/custom-compile", tags=["Compile custom"])
async def compile_custom(request: CustomCompileRequest):
    # Business logic placeholder:
    # - Clone the repo from request.git_repo_url
    # - Use the provided docker_image and registry_auth_token to run the custom toolchain.
    # - Initiate a compile job and generate a job_id and timestamp.
    return {"job_id": 10, "timestamp": "2021-10-10T10:10:10Z"}

@app.get("/custom-compile/{job_id}/status", tags=["Compile custom"])
async def get_custom_compile_status(job_id: int):
    # Business logic placeholder:
    # - Retrieve the status of the custom compile job.
    # - Validate job_id and return the status.
    return {"status": CompileStatus.running}

@app.get("/custom-compile/{job_id}/artefacts", tags=["Compile custom"])
async def get_custom_compile_artefacts(job_id: int):
    # Business logic placeholder:
    # - Retrieve and package artefacts for the custom compile job.
    dummy_zip_path = "dummy_custom.zip"  # Replace with the actual artefact zip file path.
    try:
        return FileResponse(dummy_zip_path, media_type="application/zip", filename="artefacts.zip")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
############################################################################################################
def get_source_code(gitlab_url: str, ref: str = "main"):
    encoded_repo_path = quote(gitlab_url.split("gitlab.ti.bfh.ch/")[1], safe="")
    encoded_source_path = quote(os.getenv("DEFAULT_SOURCE_PATH"), safe="")
    request_url = f"{GITLAB_API_URL}/{encoded_repo_path}/repository/files/{encoded_source_path}?ref={ref}"
    request_url = f"{GITLAB_API_URL}/{encoded_repo_path}/repository/archive.zip?ref={ref}"
    response = requests.get(request_url, headers=gitlab_api_headers)

    if response.status_code == 200:
        print("Repository archive downloaded successfully")
        return response.content
    else:
        print("Error downloading repository archive:", response.text)
        return None
############################################################################################################


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)