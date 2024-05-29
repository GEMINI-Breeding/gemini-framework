const isLocal = process.env.GEMINI_IS_LOCAL;
const apiHost = isLocal ? 'localhost' : process.env.REST_API_HOST || 'localhost';
const apiPort = process.env.REST_API_PORT || 5000;

export const apiSettings = {
    apiPort,
    apiHost,
    apiEndpoint: `http://${apiHost}:${apiPort}/api/`
};
