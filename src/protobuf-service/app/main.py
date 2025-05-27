from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, FastAPI
from pydantic import BaseModel, field_validator
from typing import List
import tempfile
import subprocess
from enum import Enum
import re

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

@router.post("/schema", response_class=Response, status_code=status.HTTP_200_OK)
async def generate_protobuf_schema(schemas: List[ProtobufSchema]) -> Response:
    with tempfile.TemporaryDirectory() as tmpdir:
        proto_file = f"{tmpdir}/schema.proto"
        with open(proto_file, 'w') as f:
            for schema in schemas:
                f.write(f"edition = \"2023\";\n\n")
                f.write(f"message {schema.message_name} {{\n")
                for idx, field in enumerate(schema.fields, 1):
                    f.write(f"  {field.protobuf_datatype.value} {field.field_name} = {idx};\n")
                f.write("}\n")
        
        # Kompiliere mit protoc
        descriptor_file = f"{tmpdir}/schema.desc"
        subprocess.run([
            "protoc",
            f"-I={tmpdir}",
            f"--descriptor_set_out={descriptor_file}",
            proto_file
        ], check=True)
        
        # Lies das Descriptor-File und gib es zurück
        with open(descriptor_file, "rb") as f:
            content = f.read()
            return Response(content=content, media_type="application/octet-stream")

app = FastAPI()
app.include_router(router)