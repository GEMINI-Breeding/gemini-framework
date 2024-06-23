const isLocal = process.env.GEMINI_IS_LOCAL === 'True'

const flaskConfig = {
    host: isLocal ? 'localhost' : process.env.REST_API_HOSTNAME,
    port: isLocal ? '5600' : process.env.REST_API_PORT,
    username: process.env.REST_API_ROOT_USER,
    password: process.env.REST_API_ROOT_PASSWORD,
    debug: process.env.REST_API_DEBUG === 'True',
    baseURL: ''
}

// Add Base URL to config
flaskConfig.baseURL = `http://${flaskConfig.host}:${flaskConfig.port}/api/`

module.exports = { isLocal, flaskConfig }