
// TODO
const BASE_URL = 'https://your-api-url.com/login'

import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()


export default {
    getUser: function (userId) {
        let url = BASE_URL + '/users/' + userId;
        const options = {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                ...authStore.getAuthHeader()
            }
        };
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
        // }
        return new Promise((resolve) => {
        resolve({
            email: 'user@example.com',
            full_name: 'John Doe',
            uuid: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            role: 'Researcher'

        })})
    },
    patchUserPassword: function (userId, currentPassword, newPassword) {
        let url = BASE_URL + '/users/' + userId;
        const options = {
            method: 'PATCH',
            headers: {
                'Accept': 'application/json',
                ...authStore.getAuthHeader()
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        };
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
        // }
        return new Promise((resolve) => {resolve('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJ1dWlkIjoiM2ZhODVmNjQtNTcxNy00NTYyLWIzZmMtMmM5NjNmNjZhZmE2In0.ywmpquYsSdIxNttr8kKbxmzklZtisgaLD42LIvbaPGg')});
    },
    postUser: function (user) {
        let url = BASE_URL + '/users';
        const options = {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                ...authStore.getAuthHeader()
            },
            body: JSON.stringify(user)
        };
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
        // }
        return new Promise((resolve) => {
        resolve({
            email: 'user@example.com',
            full_name: 'John Doe',
            uuid: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            role: 'Researcher'

        })})
    },
}
