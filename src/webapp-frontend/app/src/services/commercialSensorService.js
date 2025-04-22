import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
    getCommercialSensorsDTO: function() {
        let url = BASE_URL + '/commercial-sensors'
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
            resolve([
                {
                    id: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                    name: 'DHT22',
                    alias: 'Temperature and Humidity Sensor',
                },
                {
                    id: '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                    name: 'BME280',
                    alias: 'Temperature, Humidity and Pressure Sensor',
                },
                {
                    id: '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                    name: 'DS18B20',
                    alias: 'Water Temperature Sensor',
                },
                {
                    id: '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                    name: 'SHT31',
                    alias: 'Temperature and Humidity Sensor',
                },
                {
                    id: '3fa85f64-5717-4562-b3fc-2c963f66afaa',
                    name: 'CCS811',
                    alias: 'Air Quality Sensor',
                },
            ])
          })
    },
    getCommercialSensor(sensorId) {
        let url = BASE_URL + '/commercial-sensors/' + sensorId
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
                id: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                name: 'DHT22',
                alias: 'Temperature and Humidity Sensor',
                description: 'The DHT22 is a low-cost digital temperature and humidity sensor.',
                external_props: [
                    {
                        name: 'Datasheet',
                        url: 'https://www.adafruit.com/product/385',
                        type: 'Datasheet',
                    },
                    {
                        name: 'Distrelec',
                        url: 'https://www.distrelec.ch/en/dht22-temperature-humidity-sensor-1-pcs-adafruit/300001',
                        type: 'Webshop',
                    },
                    {
                        name: 'Arduino Tutorial',
                        url: 'https://learn.adafruit.com/dht/overview',
                        type: 'Tutorial',
                    },
                ],
                sensor_props: [
                    {
                        name: 'Temperature',
                        unit: '°C',
                        precision: '0.1',
                        range: '-40 to 80',
                    },
                    {
                        name: 'Humidity',
                        unit: '%',
                        precision: '0.1',
                        range: '0 to 100',
                    },
                ],
            })
        })
    },

    deleteCommercialSensor(sensorId) {
        let url = BASE_URL + '/commercial-sensors/' + sensorId
        const options = {
            method: 'DELETE',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
        // return fetch(url, options)
        //     .then(response => response.ok ? response.json() : Promise.reject(response));
        // }
        return new Promise((resolve) => {
            resolve(true)
        })
    }

}
