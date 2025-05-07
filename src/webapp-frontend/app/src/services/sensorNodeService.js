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
            node_template: {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                name: "the best template",
                hardware_type: "avr:esp32",
                status: "in-use",
            },
            status: "archived",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            name: "IoS temp node",
            node_template: {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                name: "IoS temp template",
                hardware_type: "arduino:uno",
                status: "in-use",
            },
            status: "active",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            name: "the best node 3",
            node_template: {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                name: "the best template 3",
                hardware_type: "esp:esp32",
                status: "in-use",
            },
            status: "inactive",
        },
        {
            uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            name: "the best node 4",
            node_template: {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                name: "the best template 4",
                hardware_type: "avr:esp32",
                status: "in-use",
            },
            status: "inactive",
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
            position:{
                latitude: 60.0,
                longitude: 24.0,
            },
            node_template: {},
            status: "archived",
            logbook: { },
            project_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        })
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
}