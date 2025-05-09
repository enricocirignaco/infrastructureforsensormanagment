import { useTextStore } from "@/stores/textStore"
const BASE_URL = useTextStore().restApiBaseUrl

import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()

export default {
  patchUserPassword: function (userId, currentPassword, newPassword) {
    let url = BASE_URL + '/users/' + userId
    const options = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
      }),
    }
    return fetch(url, options)
        .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)));
  },
  
  postUser: function (user) {
    let url = BASE_URL + '/users/'
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...authStore.getAuthHeader(),
      },
      body: JSON.stringify(user),
    }
    return fetch(url, options)
        .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)));
  },
}
