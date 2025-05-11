import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
    getSensorNodesDTO: function() {
        let url = BASE_URL + '/sensor-nodes'
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
    return Promise.resolve([
      {
        uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        name: "the best node",
        state: "Prepared",
        node_template: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          name: "the best template",
          board: {
            core: "avr",
            variant: "esp32"
          },
          state: "in-use"
        },
        project: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afaa",
          name: "Sample Project",
          short_name: "SP",
          state: "Active"
        }
      },
      {
        uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        name: "IoS temp node",
        state: "Active",
        node_template: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
          name: "IoS temp template",
          board: {
            core: "arduino",
            variant: "uno"
          },
          state: "in-use"
        },
        project: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afab",
          name: "IoS Monitoring",
          short_name: "IoSM",
          state: "Active"
        }
      },
      {
        uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
        name: "the best node 3",
        state: "Archived",
        node_template: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
          name: "the best template 3",
          board: {
            core: "esp",
            variant: "esp32"
          },
          state: "in-use"
        },
        project: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afac",
          name: "TempNet",
          short_name: "TN",
          state: "Inactive"
        }
      },
      {
        uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
        name: "the best node 4",
        state: "Inactive",
        node_template: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
          name: "the best template 4",
          board: {
            core: "avr",
            variant: "esp32"
          },
          state: "in-use"
        },
        project: {
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afad",
          name: "ForestNet",
          short_name: "FN",
          state: "Inactive"
        }
      }
    ])
     return fetch(url, options)
       .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    getSensorNode: function(id) {
        let url = BASE_URL + '/sensor-nodes/' + id
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
        return Promise.resolve({
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            name: "the best node",
            description: "A node template for monitoring ambient temperature using digital sensors.",
            position: {
              latitude: 60.0,
              longitude: 24.0,
            },
            node_template: {
              uuid: "template-1234-abcd",
              name: "Temperature Sensor Template",
              hardware_type: "Digital Sensor v2",
              gitlab_url: "https://gitlab.example.com/sensor-template",
              git_ref: "main",
              fields: [
                {
                  field_name: "temperature",
                  protbuf_datatype: "float",
                  unit: "°C",
                  commercial_sensor: "sensor-uuid-1"
                },
                {
                  field_name: "humidity",
                  protbuf_datatype: "float",
                  unit: "%",
                  commercial_sensor: "sensor-uuid-2"
                }
              ]
            },
            status: "inactive",
            logbook: [
              {
                type: "Created",
                date: "2024-01-10T12:30:00Z",
                user: {
                  uuid: "user-uuid-1",
                  full_name: "Alice Example",
                  email: "alice@example.com",
                  role: "Engineer"
                }
              },
              {
                type: "Updated",
                date: "2024-04-05T16:15:00Z",
                user: {
                  uuid: "user-uuid-2",
                  full_name: "Bob Example",
                  email: "bob@example.com",
                  role: "Researcher"
                }
              }
            ],
            project_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
          })
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
}