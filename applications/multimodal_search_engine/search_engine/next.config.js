/** @type {import('next').NextConfig} */
module.exports = ({
    webpack(config) {
      config.externals.push({ vectordb: 'vectordb' })
      return config;
    }
  })