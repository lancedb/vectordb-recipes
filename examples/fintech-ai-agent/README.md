# Fintech AI Agent

In this tutorial, we'll develop an intelligent system to process loan and insurance queries using AI agents.

1. **Extract Loan Intent**: Use LLM to classify user queries for loan intent (e.g., home improvement, medical) and predict eligibility with a RandomForest model.
2. **Generate Insurance Claims**: Simulate realistic auto insurance claim queries using synthetic data generation pipeline.
3. **Perform Semantic Search**: Leverage LanceDB with sentence embeddings for semantic similarity search to evaluate insurance claim approvals.
4. **Route Queries**: Implement a Kernel Agent to classify and route queries to either a Loan Agent or an Insurance Agent.

Future enhancements could include adding more sophisticated intent classification or integrating real-time data for loan and insurance predictions.

## Setup Instructions

1. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required packages:
   ```bash
   pip install pandas joblib pyarrow sentence-transformers lancedb mistralai scikit-learn
   ```

2. **Prepare Data**:
   - The notebook downloads `credit_risk_dataset.csv` from Google Drive automatically for loan modeling.
   - Insurance claim queries are generated dynamically within the notebook and saved as `auto_insurance_claims.csv`.

3. **Set API Keys**:
   - Add your Mistral API key to the environment variable `MISTRAL_API_KEY` or use the default provided in the code.
   - Add your Hugging Face token as `hf_token` in the notebook for the SentenceTransformer model (default provided: `hf_xxxxxx`).

4. **Run the Notebook**:
   Open the `fintech-ai-agent.ipynb` notebook in Jupyter or Google Colab and execute the cells sequentially.

## Learn More: Blog

For a detailed explanation of how this system works, check out a hypothetical blog post (you can replace this link with an actual one if you write it):

[Read the Blog Post](https://blog.lancedb.com/fintech-ai-agent/)

## Google Colab

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/fintech-ai-agent/fintech-ai-agent.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
