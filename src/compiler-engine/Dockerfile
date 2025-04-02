
FROM python:3.10-slim

# Install FastAPI dependencies
RUN pip install fastapi uvicorn docker

# Copy the Python application
COPY ./app /app
WORKDIR /app

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]