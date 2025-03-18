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

# Endpoints to get the status of a standard compile job
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
    job_id: str,
    get_source_code: bool = Query(False, description="Include the source code in the artefacts"),
    get_logs: bool = Query(False, description="Include the logs in the artefacts")
):
    
    if job_id not in jobs_status_map:
        raise HTTPException(status_code=404, detail="Job ID not found")
    if jobs_status_map[job_id]["status"] != CompileStatus.successful and jobs_status_map[job_id]["status"] != CompileStatus.delivered:
        raise HTTPException(status_code=400, detail="Job is not successful, use GET /status to get more informations")
    
    jobs_status_map[job_id]["status"] = CompileStatus.delivered
    binary_path = f"/output/{job_id}/main.ino.hex"
    if not os.path.isfile(binary_path):
        raise HTTPException(status_code=404, detail="Compiled hex file not found")
    try:
        # Return only the compiled hex file if no additional artefacts are requested
        if not get_source_code and not get_logs:
            return FileResponse(binary_path, media_type="application/octet-stream", filename="main.ino.hex")
        # Package the compiled hex file, source code, and logs into a ZIP archive
        zip_path = f"/output/{job_id}/artefacts.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(binary_path, arcname="main.ino.hex")
            if get_logs:
                log_file_path = f"/logs/{job_id}.log"
                if os.path.isfile(log_file_path):
                    zipf.write(log_file_path, arcname="compilation.log")
            if get_source_code:
                source_folder = f"/source/{job_id}/main"
                for root, _, files in os.walk(source_folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, start=source_folder)
                        zipf.write(full_path, arcname=os.path.join("source", arcname))

        return FileResponse(zip_path, media_type="application/zip", filename="artefacts.zip")
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
def download_source_code(gitlab_url: str, job_id: str, sha: str = "main"):
    encoded_repo_path = quote(gitlab_url.split("gitlab.ti.bfh.ch/")[1], safe="")
    GITLAB_API_URL = os.getenv("GITLAB_API_URL")
    request_url = f"{GITLAB_API_URL}/{encoded_repo_path}/repository/archive.zip?sha={sha}&path={os.getenv('DEFAULT_ARDUINO_FOLDER')}"
    response = requests.get(request_url, headers=GITLAB_API_HEADER)

    if response.status_code != 200:
        raise Exception(f"Error downloading repository archive: {response.text}")
    
    destination_folder = os.getenv("SOURCE_DIR")
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    # Save the ZIP content to a file
    zip_file_path = f"{destination_folder}/{job_id}.zip"
    folder_name = None
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    # Get name of unzipped folder and then unzip the archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        files_name = zip_ref.namelist()
        # Assume the top-level folder is the first name ending with '/'
        folder_name = next((name for name in files_name if name.endswith('/')), None)
        # Unzip the archive
        zip_ref.extractall(destination_folder)
    # Rename the top-level folder to the job_id
    if folder_name:
        os.rename(f"{destination_folder}/{folder_name}", f"{destination_folder}/{job_id}")
    # Remove the ZIP file
    os.remove(zip_file_path)
############################################################################################################
def default_compile_task(job_id: str, request: StadardCompileRequest):
    jobs_status_map[job_id] = {
        "status": CompileStatus.running,
        "message": "Compilation in progress"
    }
    # Download the source code from the GitLab repository
    try:
        download_source_code(request.git_repo_url, job_id, request.firmware_tag)
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
            /source/{job_id}/{os.getenv("DEFAULT_ARDUINO_FOLDER")} \
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