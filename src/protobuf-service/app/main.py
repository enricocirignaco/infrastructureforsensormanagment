from fastapi import APIRouter, Response, status, FastAPI
from pydantic import BaseModel, field_validator
from typing import List
import tempfile
import subprocess
import re
import os
import zipfile
from enum import Enum
from fastapi.responses import StreamingResponse
from io import BytesIO

class ProtobufDatatypeEnum(str, Enum):
    DOUBLE = 'double'
    FLOAT = 'float'
    INT32 = 'int32'
    INT64 = 'int64'
    UINT32 = 'uint32'
    UINT64 = 'uint64'
    SINT32 = 'sint32'
    SINT64 = 'sint64'
    FIXED32 = 'fixed32'
    FIXED64 = 'fixed64'
    SFIXED32 = 'sfixed32'
    SFIXED64 = 'sfixed64'
    BOOL = 'bool'
    STRING = 'string'
    BYTES = 'bytes'

class ProtobufSchemaField(BaseModel):
    field_name: str
    protobuf_datatype: ProtobufDatatypeEnum
    
    @field_validator('field_name')
    @classmethod
    def validate_field_name(cls, v):
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', v):
            raise ValueError('Invalid field_name: must be a valid identifier without spaces')
        return v

class ProtobufSchema(BaseModel):
    message_name: str
    fields: List[ProtobufSchemaField]
    
    @field_validator('message_name')
    @classmethod
    def validate_message_name(cls, v):
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', v):
            raise ValueError('Invalid message_name: must be a valid identifier without spaces')
        return v

router = APIRouter(
    prefix="/protobuf",
    tags=["protobuf"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/file-descriptor", response_class=Response, status_code=status.HTTP_200_OK)
async def generate_descriptor_file(schemas: List[ProtobufSchema]) -> Response:
    with tempfile.TemporaryDirectory() as tmpdir:
        proto_file = f"{tmpdir}/schema.proto"
        with open(proto_file, 'w') as f:
            f.write('edition = "2023";\n\n')
            for schema in schemas:
                f.write(f"message {schema.message_name} {{\n")
                for idx, field in enumerate(schema.fields, 1):
                    f.write(f"  {field.protobuf_datatype.value} {field.field_name} = {idx};\n")
                f.write("}\n\n")

        # Kompiliere mit protoc
        desc_file = f"{tmpdir}/schema.desc"
        subprocess.run([
            "protoc",
            f"-I={tmpdir}",
            f"--descriptor_set_out={desc_file}",
            proto_file
        ], check=True)

        # Lies das File-Descriptor-File und gib es zurück
        with open(desc_file, "rb") as f:
            content = f.read()
            return Response(content=content, media_type="application/octet-stream")

@router.post("/schema", response_class=Response, status_code=status.HTTP_200_OK)
async def generate_protobuf_schema(schema: ProtobufSchema) -> Response:
    lines = []
    lines.append('edition = "2023";\n')
    lines.append(f"message {schema.message_name} {{")
    for idx, field in enumerate(schema.fields, start=1):
        lines.append(f"  {field.protobuf_datatype.value} {field.field_name} = {idx};")
    lines.append("}\n")
        
    return Response(
        content="\n".join(lines),
        media_type="text/plain; charset=utf-8"
    )

@router.post("/nanopb", response_class=Response, status_code=status.HTTP_200_OK)
async def generate_nanopb_code(schema: ProtobufSchema) -> StreamingResponse:
    with tempfile.TemporaryDirectory() as tmpdir:
        proto_file = os.path.join(tmpdir, "schema.proto")
        with open(proto_file, 'w') as f:
            f.write('edition = "2023";\n\n')
            f.write(f"message {schema.message_name} {{\n")
            for idx, field in enumerate(schema.fields, start=1):
                f.write(f"  {field.protobuf_datatype.value} {field.field_name} = {idx};\n")
            f.write("}\n\n")

        # Generiere Nanopb-Code (.pb.h, .pb.c)
        output_dir = os.path.join(tmpdir, "out")
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run([
            "python3", "/nanopb/generator/nanopb_generator.py",
            f"-I={tmpdir}",
            f"--output-dir={output_dir}",
            proto_file
        ], check=True)

        # Erstelle ein ZIP-Archiv mit .pb.h/.pb.c und Laufzeitdateien
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            # Alle generierten Dateien in nanopb/
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                zipf.write(filepath, arcname=os.path.join("nanopb", filename))

            # Laufzeitdateien ebenfalls in nanopb/
            nanopb_files = [
                "pb.h", "pb_common.c", "pb_common.h",
                "pb_encode.c", "pb_encode.h",
                "pb_decode.c", "pb_decode.h"
            ]
            for fname in nanopb_files:
                src_path = os.path.join("/nanopb", fname)
                if os.path.exists(src_path):
                    zipf.write(src_path, arcname=os.path.join("nanopb", fname))

        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=nanopb.zip"})

app = FastAPI()
app.include_router(router)