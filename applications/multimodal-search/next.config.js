/** @type {import('next').NextConfig} */
module.exports = ({
  webpack(config) {
    config.externals.push({ vectordb: 'vectordb' })
    config.resolve.fallback = {
      fs: false
  }
    return config;
  }
})
