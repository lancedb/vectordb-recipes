# Multimodal Search

## Use LanceDB to query a variety of different types of unstructured data with many search options (semantic, keyword, SQL), all in one package.
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Youtube-Search-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Python


Install dependencies
```bash
pip install -r requirements.txt
wget -c wget -c https://eto-public.s3.us-west-2.amazonaws.com/datasets/diffusiondb_lance.tar.gz
tar -xvf diffusiondb_test
mv diffusiondb_test ~/datasets/rawdata.lance
```
Run the script 
```python
python main.py
```
| Argument | Default Value | Description |
|---|---|---|
| num-results | 9 | Number of results per query |
| model | `text-embedding-ada-002` | OpenAI model to use |

### Javascript

Install dependencies
```bash
npm install
wget -c wget -c https://eto-public.s3.us-west-2.amazonaws.com/datasets/diffusiondb_lance.tar.gz
tar -xvf diffusiondb_test
mv diffusiondb_test ~/datasets/rawdata.lance
```

Run the script
```javascript
node index.js
```
