/** @type {import('next').NextConfig} */
const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: '/api/:path*',
                destination:
                    process.env.NODE_ENV === 'development'
                        ? `http://localhost:${process.env.REST_API_PORT}/api/:path*`
                        : `https://${process.env.REST_API_HOST}:${process.env.REST_API_PORT}/api/:path*`
            }
        ]
    }
};

export default nextConfig;