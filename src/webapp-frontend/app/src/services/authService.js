import { useTextStore } from "@/stores/textStore"
const BASE_URL = useTextStore().restApiBaseUrl

export default {
  getAuthToken: function (user) {
    let url = BASE_URL + '/token'
    // check if user is specified
    if (user == null) {
      return Promise.reject('user is mandatory')
    }
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      // oauth2 request body
      body: new URLSearchParams({
        grant_type: 'password',
        username: user.username,
        password: user.password,
      }),
    }
    return fetch(url, options)
      .then(response => response.ok ? response.json() : response.json().then(errorData => Promise.reject(errorData)))
  }
}
