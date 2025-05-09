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
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  getNodeTemplate(id) {
    let url = BASE_URL + '/node-templates/' + id
    const options = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  getNodeTemplateSchema(id) {
    let url = BASE_URL + '/node-templates/' + id + '/schema'
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
            "detail": [
              {
                "loc": ["body", "temperature"],
                "msg": "Field must be a float representing degrees Celsius",
                "type": "type_error.float"
              },
              {
                "loc": ["body", "battery_level"],
                "msg": "Value must be an integer between 0 and 100",
                "type": "value_error.range"
              },
              {
                "loc": ["body", "timestamp"],
                "msg": "Invalid ISO 8601 datetime format",
                "type": "value_error.datetime"
              }
            ],
            "metadata": {
              "schema_version": "v1.2.0",
              "generated_at": "2025-05-04T18:30:00Z",
              "author": "system"
            }
          })
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  deleteNodeTemplate(id) {
    let url = BASE_URL + '/node-template/' + id
    const options = {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    return Promise.resolve(
        {
        })
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  editNodeTemplate(id){
    let url = BASE_URL + '/node-templates/' + id
    const options = {
      method: 'PUT',
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
                "commercial_sensor":
                {
                    "uuid": "a53be75c-dec2-44cb-ba02-0b83b9caaae9",
                    "name": "Temperature Sensor",
                    "alias": "TMP36"
                }
                },
                {
                "field_name": "battery_level",
                "protbuf_datatype": "int32",
                "unit": "%",
                "commercial_sensor":
                {
                    "uuid": "e5a1f7d8-2fa7-11ee-be56-0242ac120002",
                    "name": "Battery Level Sensor",
                    "alias": "Battery Sensor"
                }
                }
            ],
            "status": "in-use",
            "gitlab_url": "https://gitlab.example.com/sensor-nodes/temperature-sensor",
            "git_ref": "main",
            "board": {
              core: "AVR:ESP32",
              variant: "ESP32",
            },
            "uuid": id,
            // other fields...
        })
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  createNodeTemplate(nodeTemplate){
    let url = BASE_URL + '/node-templates'
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify(nodeTemplate),
    }
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  }
}