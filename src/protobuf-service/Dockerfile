FROM debian:bullseye AS builder

RUN apt-get update && \
    apt-get install -y wget unzip build-essential

RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v31.0/protoc-31.0-linux-x86_64.zip -O protoc.zip && \
    unzip protoc.zip -d /out && \
    rm protoc.zip

RUN wget https://jpa.kapsi.fi/nanopb/download/nanopb-0.4.9.1-linux-x86.tar.gz -O nanopb.tar.gz && \
    mkdir -p /nanopb && \
    tar -xzf nanopb.tar.gz -C /nanopb --strip-components=1 && \
    rm nanopb.tar.gz

FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y libprotobuf-dev

COPY --from=builder /out/bin/protoc /usr/local/bin/protoc
COPY --from=builder /out/include /usr/local/include
COPY --from=builder /nanopb/generator /nanopb/generator
COPY --from=builder /nanopb/pb.h /nanopb/
COPY --from=builder /nanopb/pb_common.* /nanopb/
COPY --from=builder /nanopb/pb_encode.* /nanopb/
COPY --from=builder /nanopb/pb_decode.* /nanopb/

RUN protoc --version

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]