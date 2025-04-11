
// TODO
const BASE_URL = 'https://your-api-url.com/login'

export default {
    getAuthToken: function (user) {
        let url = BASE_URL + '/token';
        // check if user is specified
        if (user == null) {
            return Promise.reject('user is mandatory');
        }
        const options = {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': 'Basic ' + btoa(user.username + ':' + user.password)
            }
        };
        // TODO
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
        // }
        return new Promise((resolve) => {resolve('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJ1dWlkIjoiM2ZhODVmNjQtNTcxNy00NTYyLWIzZmMtMmM5NjNmNjZhZmE2In0.ywmpquYsSdIxNttr8kKbxmzklZtisgaLD42LIvbaPGg')});
    }
}
