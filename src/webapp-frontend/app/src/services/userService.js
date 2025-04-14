import { useTextStore } from "@/stores/textStore"
const BASE_URL = useTextStore().restApiBaseUrl

import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()

export default {
  getUser: function (userId) {
    let url = BASE_URL + '/users/' + userId
    const options = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    // return fetch(url, options)
    //     .then(response => response.ok ? response.json() : Promise.reject(response));
    // }
    return new Promise((resolve) => {
      resolve({
        email: 'user@example.com',
        full_name: 'John Doe',
        uuid: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        role: 'Researcher',
      })
    })
  },
  patchUserPassword: function (userId, currentPassword, newPassword) {
    let url = BASE_URL + '/users/' + userId
    const options = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
      }),
    }
    // return fetch(url, options)
    //     .then(response => response.ok ? response.json() : Promise.reject(response));
    // }
    return new Promise((resolve) => {
      resolve(
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRvZUBleGFtcGxlLmNvbSIsImZ1bGxfbmFtZSI6IkpvaG4gRG9lIiwidXVpZCI6IjNmYTg1ZjY0LTU3MTctNDU2Mi1iM2ZjLTJjOTYzZjY2YWZhNiIsInJvbGUiOiJBZG1pbiJ9.VsAmTMl6Bzn_V7sqT4k77e2lTjGpNxn2zgYHhUrExJE',
      )
    })
  },
  postUser: function (user) {
    let url = BASE_URL + '/users'
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify(user),
    }
    // return fetch(url, options)
    //     .then(response => response.ok ? response.json() : Promise.reject(response));
    // }
    console.log('user:', user)
    return new Promise((resolve) => {
      resolve(user)
    })
  },
}
