let apiConfig = require('../../api.config.js')

async function getExperiments() {
    const response = await fetch(`${apiConfig.API_URL}/experiments`)
    if (!response.ok) {
        throw new Error('Failed to fetch experiments')
    }
    return response.json()
}

export const experimentsAPI = {
    getExperiments
}