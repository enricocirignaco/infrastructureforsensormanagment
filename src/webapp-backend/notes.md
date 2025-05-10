GET /sensor-nodes/?project-uuid=<uuid>&node-template-uuid=<uuid>
POST /sensor-nodes/
GET /sensor-nodes/<uuid>
PUT /sensor-nodes/<uuid>



{
    "uuid": "",
    "name": "",
    "description": "",
    state: SensorNodeStateEnum
}


SensorNodeStateEnum: Prepared, Active, Inactive, Archived