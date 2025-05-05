import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
  getNodeTemplatesDTO: function () {
    let url = BASE_URL + '/node-templates'
    const options = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    return Promise.resolve([
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            name: "the best template",
            hardware_type: "avr:esp32",
            status: "unused",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            name: "IoS temp template",
            hardware_type: "arduino:uno",
            status: "in-use",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            name: "the best template 3",
            hardware_type: "esp:esp32",
            status: "in-use",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            name: "the best template 4",
            hardware_type: "avr:esp32",
            status: "archived",
        }
    ])
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  getNodeTemplate(id) {
    let url = BASE_URL + '/node-template/' + id
    const options = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    return Promise.resolve(
{
    "name": "Temperature Sensor Node",
    "description": "A node template for monitoring ambient temperature using digital sensors.",
    "fields": [
        {
        "field_name": "temperature",
        "protbuf_datatype": "float",
        "unit": "°C",
        "commercial_sensor": "d7e3b9c4-2fa7-11ee-be56-0242ac120002"
        },
        {
        "field_name": "battery_level",
        "protbuf_datatype": "int32",
        "unit": "%",
        "commercial_sensor": "e5a1f7d8-2fa7-11ee-be56-0242ac120002"
        }
    ],
    "status": "in-use",
    "gitlab_url": "https://gitlab.example.com/sensor-nodes/temperature-sensor",
    "git_ref": "main",
    "hardware_type": "AVR:ESP32",
    "uuid": "c9a2b3d4-4f5e-11ee-be56-0242ac120002",
    "inherited_sensor_nodes": [],
    "logbook": [
        {
        "type": "Created",
        "date": "2025-01-15T10:12:30.000Z",
        "user": {
            "email": "admin@example.com",
            "full_name": "Alice Johnson",
            "role": "Admin",
            "uuid": "f9b3d5c6-4f5e-11ee-be56-0242ac120002"
        }
        },
        {
        "type": "Updated",
        "date": "2025-03-22T14:45:00.000Z",
        "user": {
            "email": "maintainer@example.com",
            "full_name": "Bob Smith",
            "role": "Maintainer",
            "uuid": "b4c3e7f8-4f5e-11ee-be56-0242ac120002"
        }
        }
    ]
    })
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
}