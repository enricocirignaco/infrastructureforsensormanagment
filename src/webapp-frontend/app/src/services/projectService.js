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
        })
      })
  }
}