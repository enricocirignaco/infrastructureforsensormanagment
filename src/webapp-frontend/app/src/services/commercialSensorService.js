import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
    getCommercialSensorsDTO: function() {
        let url = BASE_URL + '/commercial-sensors/'
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
    getCommercialSensor(sensorId) {
        let url = BASE_URL + '/commercial-sensors/' + sensorId
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
    deleteCommercialSensor(sensorId) {
        let url = BASE_URL + '/commercial-sensors/' + sensorId
        const options = {
            method: 'DELETE',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
                'Content-Type': 'application/json',
            },
        }
        return fetch(url, options)
            .then(response => response.ok ? null : response.json().then(errorData => Promise.reject(errorData)))
    },
    editCommercialSensor(sensor) {
        let url = BASE_URL + '/commercial-sensors/' + sensor.uuid
        const options = {
            method: 'PUT',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sensor),
        }
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    createCommercialSensor(sensor) {
        let url = BASE_URL + '/commercial-sensors/'
        const options = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sensor),
        }
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    }

}
