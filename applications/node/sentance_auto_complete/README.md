# Real Time autocomplete suggestions using lanchain.js and LanceDB
#  upload your data source and start typeing your article and you will be suggested with relevent relea time  suggestions that will act as auto complete for your article sentance
# you can also switch between gpt models.

(https://github.com/lancedb/assets/blob/main/recipes/sentance_Auto_complete.gif)

# add your open_ai_key (run this command in your terminal)
 export OPENAI_API_KEY= your_key

# you will be required to add the api key in langChainProcessor.js file also
# node version  above 20 required
# to run only server use

npm install
npm run server
# command to run on your local machine

npm install
npm run dev
# To use your own data. go to src>Backend>dataSourceFiles and replace the .txt file or you can upload.

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
