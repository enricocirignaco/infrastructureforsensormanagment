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
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: 'Basic ' + btoa(user.username + ':' + user.password),
      },
    }
    // TODO
    // return fetch(url, options)
    //     .then(response => response.ok ? response.json() : Promise.reject(response));
    // }
    return new Promise((resolve) => {
      resolve(
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRvZUBleGFtcGxlLmNvbSIsImZ1bGxfbmFtZSI6IkpvaG4gRG9lIiwidXVpZCI6IjNmYTg1ZjY0LTU3MTctNDU2Mi1iM2ZjLTJjOTYzZjY2YWZhNiIsInJvbGUiOiJBZG1pbiJ9.VsAmTMl6Bzn_V7sqT4k77e2lTjGpNxn2zgYHhUrExJE',
      )
    })
  },
}
