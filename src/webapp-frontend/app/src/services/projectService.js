import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
  getProjectsDTO: function () {
    let url = BASE_URL + '/projects/'
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

  getProject(id) {
    let url = BASE_URL + '/projects/' + id
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

  createProject: function (project) {
    let url = BASE_URL + '/projects/'
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(project),
    }
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },

  editProject: function (project) {
    let url = BASE_URL + '/projects/' + project.uuid
    const options = {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(project),
    }
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  },

  deleteProject(id) {
    let url = BASE_URL + '/projects/' + id
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
}