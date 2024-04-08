# Vector embedding search using TransformersJS
![image](https://github.com/lancedb/vectordb-recipes/assets/43097991/41c1dea3-ad28-42c1-969f-a81146f202e9)


### Set credentials
if you would like to set api key through an environment variable:
```
export LANCEDB_API_KEY="sk_..."
```

replace the following lines in index.js with your project slug and api key"
```
db_url: "db://your-project-slug-name"
api_key: "sk_..."
region: "us-east-1"
```

### Setup
Install node dependencies
```javascript
npm install
```

### Javascript
Run the script
```javascript
node index.js
```