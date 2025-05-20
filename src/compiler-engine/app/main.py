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
# In-memory store for build job statuses
jobs_status_map = {}  
# Load environment variables
DEFAULT_GROUP_ACCESS_TOKEN= os.getenv("DEFAULT_GROUP_ACCESS_TOKEN")
DEFAULT_GROUP_BOT_USERNAME = os.getenv("DEFAULT_GROUP_BOT_USERNAME")
DEFAULT_GITLAB_API_URL = os.getenv("DEFAULT_GITLAB_API_URL")
DEFAULT_SOURCE_DIR = os.getenv("DEFAULT_SOURCE_DIR")
DEFAULT_OUTPUT_DIR = os.getenv("DEFAULT_OUTPUT_DIR")
DEFAULT_LOG_DIR = os.getenv("DEFAULT_LOG_DIR")
DEFAULT_ARDUINO_DIR = os.getenv("DEFAULT_ARDUINO_DIR")
DEFAULT_ARDUINO_BINARY = os.getenv("DEFAULT_ARDUINO_BINARY")
DEFAULT_COMPILER_REGISTRY_URL = os.getenv("DEFAULT_COMPILER_REGISTRY_URL")

# Pydantic models for request bodies and responses
class Board(BaseModel):
    core: str
    variant: str
class ConfigProperty(BaseModel):
    key: str
    value: str
class StandardBuildRequest(BaseModel):
    git_repo_url: str
    firmware_tag: str
    board: Board
    libraries: Optional[List[str]] = None
    config: Optional[List[ConfigProperty]] = None

class CustomBuildRequest(BaseModel):
    git_repo_url: str
    git_repo_auth_token: str
    firmware_tag: str
    compiler_registry_url: str
    registry_auth_token: str
    registry_auth_username: str
    compiler_command: str

class BuildStatus(str, Enum):
    pending = "pending"
    running = "running"
    error = "error"
    successful = "successful"
    delivered = "delivered"

############################################################################################################
# Endpoints to start a standard build job with ardunio-cli
############################################################################################################
@app.post("/build", tags=["Build"])
async def build(request_data: StandardBuildRequest, background_tasks: BackgroundTasks):
    try:
        # Generate a unique job ID; if something goes wrong here, it will be caught.
        job_id = str(uuid.uuid4())
        jobs_status_map[job_id] = {
            "status": BuildStatus.pending,
            "message": "Building process started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate job ID: {str(e)}")

    try:
        # Schedule the background task; if this fails, catch and return an error.
        background_tasks.add_task(default_compile_task, job_id, request_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule build task: {str(e)}")
    
    return {
        "job_id": job_id,
        "status": jobs_status_map[job_id]["status"],
        "message": jobs_status_map[job_id]["message"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
############################################################################################################
# Endpoints to start a custom build job with a custom compiler
############################################################################################################
@app.post("/generic-build", tags=["Generic Build"])
async def generic_build(request_data: CustomBuildRequest, background_tasks: BackgroundTasks):
    try:
        # Generate a unique job ID; if something goes wrong here, it will be caught.
        job_id = str(uuid.uuid4())
        jobs_status_map[job_id] = {
            "status": BuildStatus.pending,
            "message": "Building process started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate job ID: {str(e)}")

    try:
        # Schedule the background task; if this fails, catch and return an error.
        background_tasks.add_task(
            generic_compile_task,
            job_id,
            request_data.git_repo_url,
            request_data.git_repo_auth_token,
            request_data.compiler_registry_url,
            request_data.compiler_command,
            request_data.registry_auth_token,
            request_data.registry_auth_username
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule build task: {str(e)}")
    
    return {
        "job_id": job_id,
        "status": jobs_status_map[job_id]["status"],
        "message": jobs_status_map[job_id]["message"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
############################################################################################################
# Endpoint to get the status of a build job
############################################################################################################
@app.get("/job/{job_id}/status", tags=["Build Job"])
async def get_buil_status(job_id: str):
    # check if the job_id exists in the jobs_status_map
    if job_id not in jobs_status_map:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return {
        "status": jobs_status_map[job_id]["status"],
        "message": jobs_status_map[job_id]["message"]
    }
############################################################################################################
# Endpoint to get the artifacts of a build job
############################################################################################################
@app.get("/job/{job_id}/artifacts", tags=["Build Job"])
async def get_build_artifacts(
    job_id: str,
    get_source_code: bool = Query(False, description="Include the source code in the artifacts"),
    get_logs: bool = Query(False, description="Include the logs in the artifacts"),
    bin_only: bool = Query(False, description="Return only the compiled binary file")
):
    if job_id not in jobs_status_map:
        raise HTTPException(status_code=404, detail="Job ID not found")
    if jobs_status_map[job_id]["status"] != BuildStatus.successful and jobs_status_map[job_id]["status"] != BuildStatus.delivered:
        raise HTTPException(status_code=400, detail="Job is not successful, use GET /status to get more informations")
    if bin_only and (get_source_code or get_logs):
        raise HTTPException(status_code=400, detail="Cannot include source code or logs when bin_only is set to true")
    
    try:
        # Return only the compiled binary file if bin_only is set to true
        if bin_only:
            try:
                jobs_status_map[job_id]["status"] = BuildStatus.delivered
                return FileResponse(f"{DEFAULT_OUTPUT_DIR}/{job_id}/{DEFAULT_ARDUINO_BINARY}", media_type="application/octet-stream", filename=DEFAULT_ARDUINO_BINARY)
            except Exception:
                raise HTTPException(status_code=404, detail="Compiled binary file not found")
        # Package the compiled output folder, source folder, and log file into a ZIP archive
        zip_path = f"{DEFAULT_OUTPUT_DIR}/{job_id}/artifacts.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # package output folder
            output_folder = f"{DEFAULT_OUTPUT_DIR}/{job_id}"
            if not os.path.isdir(output_folder):
                raise HTTPException(status_code=404, detail="Output code folder not found")
            for root, _, files in os.walk(output_folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Skip the artifacts.zip file to prevent recursive zipping crash
                    if full_path == zip_path:
                        continue
                    arcname = os.path.relpath(full_path, start=output_folder)
                    zipf.write(full_path, arcname=os.path.join("output", arcname))
            # package source code
            if get_source_code:
                source_folder = f"{DEFAULT_SOURCE_DIR}/{job_id}"
                if not os.path.isdir(source_folder):
                    raise HTTPException(status_code=404, detail="Source code folder not found")
                for root, _, files in os.walk(source_folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, start=source_folder)
                        zipf.write(full_path, arcname=os.path.join("source", arcname))
            # package log file
            if get_logs:
                log_file_path = f"/{DEFAULT_LOG_DIR}/{job_id}.log"
                if os.path.isfile(log_file_path):
                    zipf.write(log_file_path, arcname="compilation.log")

        jobs_status_map[job_id]["status"] = BuildStatus.delivered
        return FileResponse(zip_path, media_type="application/zip", filename="artifacts.zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

############################################################################################################
def download_source_code(request_url: str, job_id: str, repo_auth_token: str):
    response = requests.get(request_url, headers={"PRIVATE-TOKEN": repo_auth_token})

    if response.status_code != 200:
        raise Exception(f"Error downloading repository archive: {response.text}")
    
    # Ensure the destination folder exists
    os.makedirs(DEFAULT_SOURCE_DIR , exist_ok=True)
    # Save the ZIP content to a file
    zip_file_path = f"{DEFAULT_SOURCE_DIR }/{job_id}.zip"
    folder_name = None
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    # Get name of unzipped folder and then unzip the archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        files_name = zip_ref.namelist()
        # Assume the top-level folder is the first name ending with '/'
        folder_name = next((name for name in files_name if name.endswith('/')), None)
        # Unzip the archive
        zip_ref.extractall(DEFAULT_SOURCE_DIR )
    # Rename the top-level folder to the job_id
    if folder_name:
        os.rename(f"{DEFAULT_SOURCE_DIR }/{folder_name}", f"{DEFAULT_SOURCE_DIR }/{job_id}")
    # Remove the ZIP file
    os.remove(zip_file_path)

############################################################################################################
def default_compile_task(job_id: str, request: StandardBuildRequest):
    try:
        encoded_repo_path = quote(request.git_repo_url.split("gitlab.ti.bfh.ch/")[1], safe="")
    except IndexError:
        jobs_status_map[job_id] = {
            "status": BuildStatus.error,
            "message": "Invalid GitLab repository URL"
        }
        return
    git_repo_url = f"{DEFAULT_GITLAB_API_URL}/{encoded_repo_path}/repository/archive.zip?sha={request.firmware_tag}&path={DEFAULT_ARDUINO_DIR}"
    compile_command = f"""bash -c "
            mkdir -p /cache/boards /cache/arduino && \
            arduino-cli core install {request.board.core} && \
            arduino-cli lib install {" ".join(request.libraries)} && \
            arduino-cli core update-index && \
            arduino-cli compile \
            --fqbn {request.board.core}:{request.board.variant} \
            --output-dir {DEFAULT_OUTPUT_DIR}/{job_id} \
            --log-file {DEFAULT_LOG_DIR}/{job_id}.log \
            --verbose \
            {DEFAULT_SOURCE_DIR}/{job_id}/{DEFAULT_ARDUINO_DIR}
        " """
    # generate config.h file content
    if request.config:
        try:
            config_file = "// Auto-generated config.h\n"
            config_file += "#ifndef CONFIG_H\n#define CONFIG_H\n\n"
            for prop in request.config:
                config_file += f"#define {prop.key} \"{prop.value}\"\n"
            config_file += "\n#endif // CONFIG_H\n"
        except Exception as e:
            jobs_status_map[job_id] = {
                "status": BuildStatus.error,
                "message": f"Error generating config.h content: {str(e)}"
            }
            return
    else:
        config_file = None
    # build the source code
    generic_compile_task(
        job_id, git_repo_url,
        DEFAULT_GROUP_ACCESS_TOKEN,
        DEFAULT_COMPILER_REGISTRY_URL,
        compile_command,
        DEFAULT_GROUP_ACCESS_TOKEN,
        DEFAULT_GROUP_BOT_USERNAME,
        config_file
        )

############################################################################################################
def generic_compile_task(
        job_id: str,
        git_repo_url: str,
        git_repo_auth_token: str,
        compiler_registry_url: str,
        compiler_command: str,
        registry_auth_token: str,
        registry_auth_username: str,
        config_file: str = None
        ):
    # Set the job status to running
    jobs_status_map[job_id] = {
        "status": BuildStatus.running,
        "message": "Building process in progress"
    }
    # Download the source code from the GitLab repository
    try:
        download_source_code(git_repo_url, job_id, git_repo_auth_token)
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": BuildStatus.error,
            "message": f"Error downloading source code: {str(e)}"
        }
        return
    if config_file:
        # Write the config.h file to the source code folder
        try:
            with open(f"{DEFAULT_SOURCE_DIR}/{job_id}/{DEFAULT_ARDUINO_DIR}/config.h", "w") as f:
                f.write(config_file)
        except Exception as e:
            jobs_status_map[job_id] = {
                "status": BuildStatus.error,
                "message": f"Error writing config.h file: {str(e)}"
            }
            return
        # include the config.h file in the source code
        try:
            ino_file_path = f"{DEFAULT_SOURCE_DIR}/{job_id}/{DEFAULT_ARDUINO_DIR}/main.ino"
            with open(ino_file_path, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write('#include "config.h"\n\n' + content)
        except Exception as e:
            jobs_status_map[job_id] = {
                "status": BuildStatus.error,
                "message": f"Error including config.h in main.ino: {str(e)}"
            }
            return

    # Build source code in the Docker container
    try:
        docker_client.images.pull(
            compiler_registry_url,
            auth_config={
                "username": registry_auth_username,
                "password": registry_auth_token
            }
)
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
            detach=False
        )
        message = container_output.decode('utf-8') if isinstance(container_output, bytes) else container_output
        jobs_status_map[job_id] = {
            "status": BuildStatus.successful,
            "message": f"Building process successful: {message}"
        }
    except Exception as e:
        jobs_status_map[job_id] = {
            "status": BuildStatus.error,
            "message": f"Error compiling source code: {str(e)}"
        }

############################################################################################################
# Main
############################################################################################################
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)