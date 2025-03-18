from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import os
import requests
import docker
from urllib.parse import quote
from urllib.parse import quote, urlparse
import zipfile
import uuid
from datetime import datetime, timezone

# Initialize the FastAPI app
app = FastAPI(title="Compiler Engine",version="1.0")
# Connect to the host Docker daemon
docker_client = docker.from_env()
# In-memory store for compile job statuses
jobs_status_map = {}  
# GitLab API header with the access token
GITLAB_API_HEADER = {"PRIVATE-TOKEN": os.getenv("GROUP_ACCESS_TOKEN")}

# Pydantic models for request bodies and responses
class Board(BaseModel):
    core: str
    variant: str

class StadardCompileRequest(BaseModel):
    git_repo_url: str
    firmware_tag: str
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

# Endpoints to start a standard compile job with ardunio-cli
@app.post("/compile", tags=["Compile standard"])
async def compile_standard(request: StadardCompileRequest, background_tasks: BackgroundTasks):
    try:
        # Generate a unique job ID; if something goes wrong here, it will be caught.
        job_id = str(uuid.uuid4())
        jobs_status_map[job_id] = CompileStatus.pending
        jobs_status_map[job_id] = {
            "status": CompileStatus.pending,
            "message": "Compilation started in background"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate job ID: {str(e)}")

    try:
        # Schedule the background task; if this fails, catch and return an error.
        background_tasks.add_task(default_compile_task, job_id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule compile task: {str(e)}")
    
    return {
        "job_id": job_id,
        "status": jobs_status_map[job_id]["status"],
        "message": jobs_status_map[job_id]["message"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

@app.get("/compile/{job_id}/status", tags=["Compile standard"])
async def get_compile_status(job_id: str):
    # check if the job_id exists in the jobs_status_map
    if job_id not in jobs_status_map:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return {
        "status": jobs_status_map[job_id]["status"],
        "message": jobs_status_map[job_id]["message"]
    }

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
def download_source_code(gitlab_url: str, ref: str = "main"):
    encoded_repo_path = quote(gitlab_url.split("gitlab.ti.bfh.ch/")[1], safe="")
    request_url = f"{os.getenv("GITLAB_API_URL")}/{encoded_repo_path}/repository/archive.zip?ref={ref}"
    response = requests.get(request_url, headers=GITLAB_API_HEADER)

    if response.status_code != 200:
        raise Exception(f"Error downloading repository archive: {response.text}")
    
    destination_folder = os.getenv("SOURCE_DIR")
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    # Save the ZIP content to a file
    zip_file_path = f"{destination_folder}/repo_archive.zip"
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    # Unzip the archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    os.remove(zip_file_path)
############################################################################################################
def default_compile_task(job_id: str, request: StadardCompileRequest):
    jobs_status_map[job_id] = {
        "status": CompileStatus.running,
        "message": "Compilation in progress"
    }
    # Download the source code from the GitLab repository
    try:
        download_source_code(request.git_repo_url, request.firmware_tag)
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": CompileStatus.error,
            "message": f"Error downloading source code: {str(e)}"
        }
        return
    # Compile source code in the Docker container
    try:
        compile_command = f"""bash -c "
            mkdir -p /cache/boards /cache/arduino && \
            arduino-cli core install {request.board.core} && \
            arduino-cli lib install {" ".join(request.libraries)} && \
            arduino-cli core update-index && \
            arduino-cli compile \
            --fqbn {request.board.core}:{request.board.variant} \
            --output-dir /output/{job_id} \
            --log-file /logs/{job_id}.log \
            --verbose \
            /source/{os.getenv("DEFAULT_ARDUINO_FOLDER")} \
            {request.custom_flags if request.custom_flags else ""}
        " """
        container_output = docker_client.containers.run(
            os.getenv("DEFAULT_COMPILER_REGISTRY_URL"),
            compile_command,
            volumes={
                "compiler-engine-source": {"bind": "/source", "mode": "rw"},
                "compiler-engine-output": {"bind": "/output", "mode": "rw"},
                "compiler-engine-logs": {"bind": "/logs", "mode": "rw"},
                "compiler-engine-cache": {"bind": "/root/.arduino15", "mode": "rw"}
            },
            remove=True,
            detach=False
        )
        jobs_status_map[job_id] = {
            "status": CompileStatus.successful,
            "message": f"Compilation successful: {container_output.decode('utf-8')}"
        }
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": CompileStatus.error,
            "message": f"Error compiling source code: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)