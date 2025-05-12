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
          location: {
            latitude: 41.5579215778042,
            longitude: 12.63427734375,
            altitude: 100.0,
            postalcode: "12345"
          },
          configurables: [
            {
              name: "sampling_interval1",
              type: "UserDefined",
              value: "60"
            },
            {
              name: "sampling_interval2",
              type: "SystemDefined",
              value: "halihalo"
            }
          ],
          state: "Prepared",
          node_template_uuid: "53158b25-a93f-432a-9f41-e7dff5d2d0bb",
          project_uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          ttn_device_link: "https://example.com/",
          last_timeseries: {
            timestamp: "2025-05-11T12:24:19.797Z",
            fields: [
              {
                field_name: "temperature",
                protobuf_datatype: "float",
                unit: "°C",
                value: "22.3"
              },
              {
                field_name: "humidity",
                protobuf_datatype: "float",
                unit: "%",
                value: "55"
              }
            ]
          },
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
          ]
        })
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    createSensorNode: function(sensorNode) {
        let url = BASE_URL + '/sensor-nodes'
        const options = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                ...authStore.getAuthHeader(),
            },
            body: JSON.stringify(sensorNode),
        }
        return Promise.resolve({
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          name: "the best node",
          description: "A node template for monitoring ambient temperature using digital sensors.",
          location: {
            latitude: 60.0,
            longitude: 24.0,
            altitude: 100.0,
            postalcode: "12345"
          },
          configurables: [
            {
              name: "sampling_interval",
              type: "UserDefined",
              value: "60"
            },
            {
              name: "sampling_interval",
              type: "SystemDefined",
              value: "halihalo"
            }
          ],
          state: "Prepared",
          node_template_uuid: "53158b25-a93f-432a-9f41-e7dff5d2d0bb",
          project_uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          ttn_device_link: "https://example.com/",
          logbook: [
            {
              type: "Created",
              date: "2024-01-10T12:30:00Z",
              user: {
                uuid: "user-uuid-1",
                full_name: "Alice Example",
                email: "some"
              }
              }
              ],
        })
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    editSensorNode(sensorNode) {
        let url = BASE_URL + '/sensor-nodes/' + sensorNode.uuid
        const options = {
            method: 'PUT',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                ...authStore.getAuthHeader(),
            },
            body: JSON.stringify(sensorNode),
        }
        return Promise.resolve({
          uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          name: "the best node",
          description: "A node template for monitoring ambient temperature using digital sensors.",
          location: {
            latitude: 60.0,
            longitude: 24.0,
            altitude: 100.0,
            postalcode: "12345"
          },
          configurables: [
            {
              name: "sampling_interval",
              type: "UserDefined",
              value: "60"
            },
            {
              name: "sampling_interval",
              type: "SystemDefined",
              value: "halihalo"
            }
          ],
          state: "Prepared",
          node_template_uuid: "53158b25-a93f-432a-9f41-e7dff5d2d0bb",
          project_uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          ttn_device_link: "https://example.com/",
          logbook: [
            {
              type: "Created",
              date: "2024-01-10T12:30:00Z",
              user: {
                uuid: "user-uuid-1",
                full_name: "Alice Example",
                email: "some"
              }
              }
              ],
        })
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    deleteSensorNode: function(id) {
        let url = BASE_URL + '/sensor-nodes/' + id
        const options = {
            method: 'DELETE',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
        return Promise.resolve(true)
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
    },

}