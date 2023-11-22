# LLM Pre-training Data loading with Lance
![GPT](https://raw.githubusercontent.com/tanaymeh/vectordb-recipes/add_llm_pretraining_example/examples/llm-pretraining-dataloading/gpt_model_architecture.png)

In this example, we will Pre-train a GPT model from scratch on the TinyStories dataset. For the complex task of memory-efficient data loading, we will be using lance.

If you are running the scripts, it is important that you must first run the `data_prep.py` script (and only once) and then run the `train.py` script.

If you are following the Kaggle Walkthrough, you don't need to run any script in advance. Instead, just fork Kaggle notebook and run it.

Link to the Kaggle walkthrough: [GPT from scratch using Lightning ⚡️ and Lance 🎯](https://www.kaggle.com/code/heyytanay/gpt-from-scratch-using-lightning-and-lance)


### Running python script
```shell
pip install -r requirements.txt

python data_prep.py
python train.py
```

### Running the notebook locally
```shell
pip install -r requirements.txt
pip install -q ipython

ipython train.ipynb
```