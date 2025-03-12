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

@app.get("/")
def read_root():
    return {"message": "Compiler Engine API is running"}

@app.post("/compile")
def compile_code():
    return {"message": "Compilation triggered (dummy response)"}

@app.get("/test-compile")
def test_compile():
    try:
        # Run the Arduino compiler container
        container_output = client.containers.run(
            "registry.gitlab.ti.bfh.ch/internetofsoils/infrastructureforsensormanagment/arduino-compiler:latest",
            "arduino-cli",
            remove=True,
            detach=False
        )
        return {"message": "Arduino CLI ran from GitLab CI/CD successfully", "output": container_output}
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