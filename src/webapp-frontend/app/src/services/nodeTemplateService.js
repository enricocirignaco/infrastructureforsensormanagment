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
}