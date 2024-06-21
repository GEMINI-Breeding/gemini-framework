/** @type {import('next').NextConfig} */

const flaskConfig = require('./api.config.js')

const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: '/api/:path*',
                destination: `http://${flaskConfig.host}:${flaskConfig.port}/:path*`,
            },
        ]
    },
}

module.exports = nextConfig
