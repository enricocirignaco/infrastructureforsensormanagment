FROM debian:bullseye AS builder

RUN apt-get update && \
    apt-get install -y wget unzip build-essential

RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v31.0/protoc-31.0-linux-x86_64.zip -O protoc.zip && \
    unzip protoc.zip -d /out && \
    rm protoc.zip


FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y libprotobuf-dev

COPY --from=builder /out/bin/protoc /usr/local/bin/protoc
COPY --from=builder /out/include /usr/local/include

RUN protoc --version

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]