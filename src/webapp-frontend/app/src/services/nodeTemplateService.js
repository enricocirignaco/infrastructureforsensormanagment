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
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },
  
  deleteNodeTemplate(id) {
    let url = BASE_URL + '/node-templates/' + id
    const options = {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    return fetch(url, options)
      .then(response => response.ok ? null : response.json().then(errorData => Promise.reject(errorData)))
  },

  editNodeTemplate(nodeTemplate){
    let url = BASE_URL + '/node-templates/' + nodeTemplate.uuid
    const options = {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify(nodeTemplate),
    }
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