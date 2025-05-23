import { useTextStore } from "@/stores/textStore"
import { useAuthStore } from "@/stores/authStore"
const BASE_URL = useTextStore().restApiBaseUrl
const authStore = useAuthStore()

export default {
    buildFirmware: function(sensorId) {
        let url = BASE_URL + '/compilation/build/' + sensorId
        const options = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
                'Content-Type': 'application/json',
            },
        }
        // return Promise.resolve({
        //     job_id: "123e4567-e89b-12d3-a456-426614174000",
        //     status: "pending",
        //     message: "Building process started in background",
        //     timestamp: "2021-10-10T10:10:10Z"
        // });
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    getBuildJobStatus: function(jobId) {
        let url = BASE_URL + '/compilation/job/' + jobId + '/status'
        const options = {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                ...authStore.getAuthHeader(),
            },
        }
        // return Promise.resolve({
        //     "status": "success",
        //     "message": "Building process in progress"
        //     });
        return fetch(url, options)
            .then(response => response.ok ? response.json() : Promise.reject(response));
    },
    getBuildArtifact: function(jobId, binOnly = true, getSourceCode = false, getLogs = false, isDownload = false) {
        let url = BASE_URL + '/compilation/job/' +jobId + '/artifacts?bin_only=' + binOnly + '&get_source_code=' + getSourceCode +'&get_logs=' + getLogs + '&is_download=' + isDownload
        const options = {
            method: 'GET',
            headers: {
               Accept: 'application/octet-stream, application/zip, application/json',
                ...authStore.getAuthHeader(),
            },
        }
        // return Promise.resolve(new Blob([""], { type: "application/octet-stream" }));
        return fetch(url, options)
            .then(response => response.ok ? response : Promise.reject(response));
    }
}