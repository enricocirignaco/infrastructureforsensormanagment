import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
    getSensorNodesDTO: function() {
        let url = BASE_URL + '/sensor-nodes/'
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
     return fetch(url, options)
       .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    getSensorNodesByProject: function(projectId) {
        let url = BASE_URL + '/sensor-nodes/?project_uuid=' + projectId
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
     return fetch(url, options)
       .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    getSensorNodesByNodeTemplate: function(nodeTemplateId) {
        let url = BASE_URL + '/sensor-nodes/?node_template_uuid=' + nodeTemplateId
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
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
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    createSensorNode: function(sensorNode) {
        let url = BASE_URL + '/sensor-nodes/'
        const options = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                ...authStore.getAuthHeader(),
            },
            body: JSON.stringify(sensorNode),
        }
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
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
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
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
        return fetch(url, options)
            .then(response => response.ok ? null : response.json().then(errorData => Promise.reject(errorData)))
    },

}