/** @type {import('next').NextConfig} */

const flaskConfig = require('./api.config.js').flaskConfig

const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: '/api/:path*',
                destination: `http://${flaskConfig.host}:${flaskConfig.port}/api/:path*`,
            },
        ]
    },
}

module.exports = nextConfig
