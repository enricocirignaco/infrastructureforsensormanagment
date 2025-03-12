import docker
from fastapi import FastAPI, HTTPException

client = docker.from_env()  # Connect to the host Docker daemon

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Compiler Engine API is running"}

@app.post("/compile")
def compile_code():
    return {"message": "Compilation triggered (dummy response)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/test-compile")
def test_compile():
    try:
        # Run the Arduino compiler container
        container = client.containers.run(
            "registry.gitlab.ti.bfh.ch/internetofsoils/infrastructureforsensormanagment/arduino-compiler:latest",  # Name of the compiler image
            "arduino-cli",  # Command to run inside the container
            remove=True,  # Automatically remove the container after execution
            detach=False  # Run synchronously (wait for output)
        )
        return {"message": "Arduino CLI ran from gitlab CICDsuccessfully", "output": container.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))