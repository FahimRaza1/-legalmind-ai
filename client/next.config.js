/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'http://backend:8000/:path*', // 'backend' is the service name in docker-compose
      },
    ];
  },
};

export default nextConfig;
