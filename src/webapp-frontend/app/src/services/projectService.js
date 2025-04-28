import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()


export default {
  getProjectsDTO: function () {
    let url = BASE_URL + '/projects'
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
        resolve([
            {
                id: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                name: 'Internet of Soils',
                short_name: 'IoS',
                state: 'Active',
            },
            {
                id: '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                name: 'Another Project',
                short_name: 'MuC',
                state: 'Inactive',
            },
        ])
      })
  },
  getProject(id) {
    let url = BASE_URL + '/projects/' + id
    const options = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
  //   return fetch(url, options)
  //     .then(response => response.ok ? response.json() : Promise.reject(response));
  // }
    return new Promise((resolve) => {
        resolve({
          id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          name: "Internet of Soils",
          short_name: "IoS",
          description: "A research project focused on soil monitoring using IoT sensors.",
          external_props: [
            {
              name: "GitHub Repository",
              url: "https://github.com/example/internet-of-soils",
              type: "Misc"
            },
            {
              name: "Project Website",
              url: "https://internetofsoils.example.org",
              type: "Website"
            }
          ],
          state: "Active",
          sensor_nodes: [
            {
              id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              name: "Node 1",
              type: "Temperature Sensor",
              location: "Stadt Bern",
              status: "Active"
            },
            {
              id: "3fa85f64-5717-4562-b3fc-2c963f66afa7",
              name: "Node 2",
              type: "Humidity Sensor",
              location: "Stadt Bern",
              status: "Inactive"
            },
            {
              id: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
              name: "Node 3",
              type: "Soil Moisture Sensor",
              location: "Stadt Bern",
              status: "Active"
            },
            {
              id: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
              name: "Node 4",
              type: "Light Sensor",
              location: "Stadt Bern",
              status: "Inactive"
            },
          ],
          logbook: [
            {
              type: "created",
              date: "2024-03-15T08:45:00Z",
              user: {
                email: "alice.researcher@example.com",
                full_name: "Alice Researcher",
                role: "Researcher",
                uuid: "bba1f5aa-2b22-4f42-98ab-56f871414ffc"
              }
            },
            {
              type: "updated",
              date: "2024-03-20T14:12:00Z",
              user: {
                email: "bob.technician@example.com",
                full_name: "Bob Technician",
                role: "Technician",
                uuid: "f21a6ea7-0dfb-4d39-86c9-4cbe17d82388"
              }
            },
            {
              type: "updated",
              date: "2024-04-01T09:30:00Z",
              user: {
                email: "carol.manager@example.com",
                full_name: "Carol Manager",
                role: "Project Manager",
                uuid: "9a2152e5-03e9-4eb2-bef3-4e6dfcb7dfbb"
              }
            },
            {
              type: "updated",
              date: "2024-04-10T16:45:00Z",
              user: {
                email: "alice.researcher@example.com",
                full_name: "Alice Researcher",
                role: "Researcher",
                uuid: "bba1f5aa-2b22-4f42-98ab-56f871414ffc"
              }
            },
            {
              type: "updated",
              date: "2024-04-22T11:05:00Z",
              user: {
                email: "bob.technician@example.com",
                full_name: "Bob Technician",
                role: "Technician",
                uuid: "f21a6ea7-0dfb-4d39-86c9-4cbe17d82388"
              }
            }
          ]
        })
      })
  },
  createProject: function (project) {
    let url = BASE_URL + '/projects'
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(project),
    }
    // return fetch(url, options)
    //   .then(response => response.ok ? response.json() : Promise.reject(response));
    return new Promise((resolve) => {
        resolve({
            id: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            name: 'Internet of Soils',
            short_name: 'IoS',
            state: 'Active',
        })
      })
  },
  editProject: function (project) {
    let url = BASE_URL + '/projects/' + project.id
    const options = {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(project),
    }
    // return fetch(url, options)
    //   .then(response => response.ok ? response.json() : Promise.reject(response));
    return new Promise((resolve) => {
        resolve({
            id: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            name: 'Internet of Soils',
            short_name: 'IoS',
            state: 'Active',
        })
      })
  },
  deleteProject(id) {
    let url = BASE_URL + '/projects/' + id
    const options = {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        ...authStore.getAuthHeader(),
      },
    }
    // return fetch(url, options)
    //   .then(response => response.ok ? response.json() : Promise.reject(response));
    return new Promise((resolve) => {
        resolve(true)
      })
  }
}