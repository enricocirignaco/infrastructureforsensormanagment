import os
import requests
import docker
from urllib.parse import quote
from fastapi import FastAPI, HTTPException
import base64

client = docker.from_env()  # Connect to the host Docker daemon

app = FastAPI()

GITLAB_TOKEN = os.getenv("GROUP_ACCESS_TOKEN")  # Read GitLab token from environment
GITLAB_PROJECT_ID = "46416"  # Replace with the actual numeric Project ID
GITLAB_API_URL = f"https://gitlab.ti.bfh.ch/api/v4/projects/{GITLAB_PROJECT_ID}/repository/files"
SOURCE_DIR = "/source/main"

@app.get("/")
def read_root():
    return {"message": "Compiler Engine API is running"}

@app.post("/compile")
def compile_code():
    return {"message": "Compilation triggered (dummy response)"}



@app.get("/test-compile")
def test_compile(file_path: str = "main/main.ino", ref: str = "main"):
    try:
        # Step 1: Fetch the file from GitLab
        headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
        encoded_file_path = quote(file_path, safe="")
        url = f"{GITLAB_API_URL}/{encoded_file_path}?ref={ref}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching file: {response.text}")

        file_data = response.json()

        # Step 2: Decode and save the file inside the Docker volume
        try:
            decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
            file_save_path = os.path.join(SOURCE_DIR, os.path.basename(file_path))

            os.makedirs(SOURCE_DIR, exist_ok=True)  # Ensure the volume directory exists
            with open(file_save_path, "w") as file:
                file.write(decoded_content)

        except Exception as decode_error:
            raise HTTPException(status_code=500, detail=f"Error decoding/saving file: {str(decode_error)}")

        # Step 3: Run the Arduino compiler container with the same volume
        container_output = client.containers.run(
            "registry.gitlab.ti.bfh.ch/internetofsoils/infrastructureforsensormanagment/arduino-compiler:latest",
            f"arduino-cli compile --fqbn arduino:avr:uno /source/main/{os.path.basename(file_path)}",
            volumes={"source-volume": {"bind": "/source", "mode": "rw"}},  # Bind the same volume
            remove=True,
            detach=False
        )

        return {"message": "Compilation completed", "output": container_output.decode("utf-8") if isinstance(container_output, bytes) else container_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/get-source")
def get_source_code(file_path: str = "main/main.ino", ref: str = "main"):
    """
    Fetches the content of a file from a GitLab repository.

    :param file_path: Path of the file in the repo (e.g., "main.py")
    :param ref: The branch, tag, or commit SHA (default: "main")
    :return: The file content as plain text
    """
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    encoded_file_path = quote(file_path, safe="")
    url = f"{GITLAB_API_URL}/{encoded_file_path}?ref={ref}"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        return {"file_name": file_data["file_path"], "content": file_data["content"]}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching file: {response.text}")
    
@app.get("/get-sourcev2")
def get_source_code(file_path: str = "main/main.ino", ref: str = "main"):
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    encoded_file_path = quote(file_path, safe="")
    url = f"{GITLAB_API_URL}/{encoded_file_path}?ref={ref}"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        try:
            decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
            return {"file_name": file_data["file_path"], "content": decoded_content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error decoding file: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching file: {response.text}")