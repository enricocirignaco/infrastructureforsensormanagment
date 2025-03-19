from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import os
import requests
import docker
from urllib.parse import quote
import zipfile
import uuid
from datetime import datetime, timezone
import uvicorn

# Initialize the FastAPI app
app = FastAPI(title="Compiler Engine",version="1.0")
# Connect to the host Docker daemon
docker_client = docker.from_env()
# In-memory store for compile job statuses
jobs_status_map = {}  
# GitLab API header with the access token
GROUP_ACCESS_TOKEN = os.getenv("GROUP_ACCESS_TOKEN")
GITLAB_API_URL = os.getenv("GITLAB_API_URL")
DEFAULT_ARDUINO_FOLDER = os.getenv('DEFAULT_ARDUINO_FOLDER')
DEFAULT_SOURCE_PATH= os.getenv("SOURCE_DIR")
DEFAULT_COMPILER_REGISTRY_URL = os.getenv("DEFAULT_COMPILER_REGISTRY_URL")
GROUP_BOT_USERNAME = os.getenv("GROUP_BOT_USERNAME")
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
    repo_auth_token: str
    firmware_tag: str
    compiler_registry_url: str
    registry_auth_token: str
    registry_auth_username: str
    compiler_command: str

class CompileStatus(str, Enum):
    pending = "pending"
    running = "running"
    error = "error"
    successful = "successful"
    delivered = "delivered"

class Status(BaseModel):
    status: CompileStatus

# Endpoints to start a standard compile job with ardunio-cli
@app.post(["/compile", "/custom-compile"], tags=["Compile custom", "Compile standard"])
async def compile(request_data: StadardCompileRequest, background_tasks: BackgroundTasks, request: Request,):
    try:
        # Generate a unique job ID; if something goes wrong here, it will be caught.
        job_id = str(uuid.uuid4())
        jobs_status_map[job_id] = {
            "status": CompileStatus.pending,
            "message": "Compilation started in background"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate job ID: {str(e)}")

    try:
        # Schedule the background task; if this fails, catch and return an error.
        if(request.url.path == "/compile"):
            background_tasks.add_task(default_compile_task, job_id, request_data)
        elif(request.url.path == "/custom-compile"):
            background_tasks.add_task(custom_compile_task, job_id, request_data)
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

# Endpoints to get the artefacts of a standard compile job
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
                if not os.path.isdir(source_folder):
                    raise HTTPException(status_code=404, detail="Source code folder not found")
                for root, _, files in os.walk(source_folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, start=source_folder)
                        zipf.write(full_path, arcname=os.path.join("source", arcname))

        return FileResponse(zip_path, media_type="application/zip", filename="artefacts.zip")
    except Exception:
                raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/custom-compile/{job_id}/artefacts", tags=["Compile custom"])
async def get_custom_compile_artefacts(
    job_id: str,
    get_source_code: bool = Query(False, description="Include the source code in the artefacts"),
    get_logs: bool = Query(False, description="Include the logs in the artefacts")
):
    try:
        output_folder = f"/output/{job_id}"
        if not os.path.isdir(output_folder):
            raise HTTPException(status_code=404, detail="Output folder not found")

        zip_path = f"/output/{job_id}/artefacts.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=output_folder)
                    zipf.write(full_path, arcname=os.path.join("output", arcname))

            if get_logs:
                log_file_path = f"/logs/{job_id}.log"
                if os.path.isfile(log_file_path):
                    zipf.write(log_file_path, arcname="compilation.log")

            if get_source_code:
                source_folder = f"/source/{job_id}"
                if os.path.isdir(source_folder):
                    for root, _, files in os.walk(source_folder):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, start=source_folder)
                            zipf.write(full_path, arcname=os.path.join("source", arcname))

        return FileResponse(zip_path, media_type="application/zip", filename="artefacts.zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
############################################################################################################
def download_source_code(request_url: str, job_id: str, repo_auth_token: str):
    response = requests.get(request_url, headers={"PRIVATE-TOKEN": repo_auth_token})

    if response.status_code != 200:
        raise Exception(f"Error downloading repository archive: {response.text}")
    
    # Ensure the destination folder exists
    os.makedirs(DEFAULT_SOURCE_PATH, exist_ok=True)
    # Save the ZIP content to a file
    zip_file_path = f"{DEFAULT_SOURCE_PATH}/{job_id}.zip"
    folder_name = None
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    # Get name of unzipped folder and then unzip the archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        files_name = zip_ref.namelist()
        # Assume the top-level folder is the first name ending with '/'
        folder_name = next((name for name in files_name if name.endswith('/')), None)
        # Unzip the archive
        zip_ref.extractall(DEFAULT_SOURCE_PATH)
    # Rename the top-level folder to the job_id
    if folder_name:
        os.rename(f"{DEFAULT_SOURCE_PATH}/{folder_name}", f"{DEFAULT_SOURCE_PATH}/{job_id}")
    # Remove the ZIP file
    os.remove(zip_file_path)
############################################################################################################
def default_compile_task(job_id: str, request: StadardCompileRequest):
    encoded_repo_path = quote(request.git_repo_url.split("gitlab.ti.bfh.ch/")[1], safe="")
    git_repo_url = f"{GITLAB_API_URL}/{encoded_repo_path}/repository/archive.zip?sha={request.firmware_tag}&path={DEFAULT_ARDUINO_FOLDER}"
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
            /source/{job_id}/{DEFAULT_ARDUINO_FOLDER}
        " """
    generic_compile_task(job_id, git_repo_url, GROUP_ACCESS_TOKEN, DEFAULT_COMPILER_REGISTRY_URL, compile_command, GROUP_ACCESS_TOKEN, GROUP_BOT_USERNAME)

############################################################################################################
def generic_compile_task(
        job_id: str,
        git_repo_url: str,
        git_repo_auth_token: str,
        compiler_registry_url: str,
        compiler_command: str,
        registry_auth_token: str,
        registry_auth_username: str
        ):
    # Set the job status to running
    jobs_status_map[job_id] = {
        "status": CompileStatus.running,
        "message": "Compilation in progress"
    }
    # Download the source code from the GitLab repository
    try:
        download_source_code(git_repo_url, job_id, git_repo_auth_token)
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": CompileStatus.error,
            "message": f"Error downloading source code: {str(e)}"
        }
        return
    # Compile source code in the Docker container
    try:
        container_output = docker_client.containers.run(
            compiler_registry_url,
            compiler_command,
            volumes={
                "compiler-engine-source": {"bind": "/source", "mode": "rw"},
                "compiler-engine-output": {"bind": "/output", "mode": "rw"},
                "compiler-engine-logs": {"bind": "/logs", "mode": "rw"},
                "compiler-engine-cache": {"bind": "/root/.arduino15", "mode": "rw"}
            },
            remove=True,
            detach=False,
            auth_config={
                "username": registry_auth_username,
                "password": registry_auth_token
            }
        )
        message = container_output.decode('utf-8') if isinstance(container_output, bytes) else container_output
        jobs_status_map[job_id] = {
            "status": CompileStatus.successful,
            "message": f"Compilation successful: {message}"
        }
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": CompileStatus.error,
            "message": f"Error compiling source code: {str(e)}"
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)