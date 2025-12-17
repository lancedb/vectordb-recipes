# 🍳 Multimodal Recipe Agent

A complete AI-powered recipe search application that understands both text and images using LanceDB, PydanticAI, and Streamlit.

## Features

### Colab Tutorial
- **Interactive Learning**: Step-by-step notebook with sample recipes
- **Core Concepts**: Learn multimodal agent development
- **No Setup Required**: Run directly in your browser

### Full Demo Application
- **Semantic Recipe Search**: Find recipes by describing what you want to cook
- **Visual Recipe Discovery**: Upload a photo to find similar recipes
- **Conversational Interface**: Chat with an AI agent about cooking
- **Multimodal Storage**: Recipe text, images, and vectors stored together in LanceDB
- **Production Ready**: Complete with error handling and logging

## Quick Start

### Option 1: Interactive Tutorial (Google Colab)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1pxavAGoXa-KSh_4HxNpvP2AjHPcIRpbq?usp=sharing)

**Perfect for learning!** This Colab notebook provides a step-by-step tutorial with sample data. No setup required - just click and start learning about multimodal agents.

### Option 2: Full Demo Application (Local Setup)

#### 1. Download and Setup

```bash
# Download the tutorial files from GitHub
# Extract all files to a folder named 'multimodal-recipe-agent'
# Navigate to the folder
cd multimodal-recipe-agent
```

#### 2. Install Dependencies

```bash
uv sync
```

#### 3. Download and Import Full Dataset

**First, download the dataset:**
1. Visit [Kaggle Recipe Dataset](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images)
2. Download the dataset and extract it to your `multimodal-recipe-agent` folder
3. Ensure the `recipes.csv` file is in the `data/` directory

**Then run the import script:**
```bash
uv run python import.py
```

This will:
- Process the downloaded recipe dataset from Kaggle
- Generate text and image embeddings for thousands of recipes
- Store everything in a LanceDB database

#### 4. Run the Complete Application

**Streamlit Chat App:**
```bash
uv run streamlit run app.py
```

**Jupyter Notebook Tutorial:**
```bash
uv run jupyter notebook multimodal-recipe-agent.ipynb
```

## Project Structure

```
multimodal-recipe-agent/
├── multimodal-recipe-agent.ipynb  # Interactive tutorial
├── agent.py                       # PydanticAI agent implementation
├── app.py                         # Streamlit chat interface
├── import.py                      # Data import and processing
├── pyproject.toml                 # Modern Python project configuration
├── uv.lock                        # Locked dependency versions
├── README.md                      # This file
└── data/                          # Generated data directory (created after import)
    ├── recipes.csv               # Recipe dataset
    ├── images/                   # Recipe images
    └── recipes.lance             # LanceDB database
```

## Download Instructions

1. **Download the tutorial files** from the GitHub repository
2. **Extract all files** to a folder named `multimodal-recipe-agent`
3. **Ensure all files are in the same directory** - this is important for imports to work
4. **Navigate to the folder** in your terminal before running commands

## Usage

### Text Search
- Ask questions like "Find me healthy pasta recipes with chicken"
- Search by ingredients: "What can I make with eggs, flour, and milk?"

### Image Search
- Upload a photo of a dish in the Streamlit sidebar
- The AI will find similar recipes based on visual similarity

### Chat Interface
- Have a conversation with the recipe assistant
- Ask follow-up questions about ingredients or cooking methods
- Get detailed recipe information with images

## Key Technologies

- **LanceDB**: Multimodal vector database for efficient storage and retrieval
- **PydanticAI**: Modern AI agent framework with type safety
- **Sentence Transformers**: Text embeddings for semantic search
- **CLIP**: Vision-language model for image understanding
- **Streamlit**: Interactive web application framework

## Requirements

- Python 3.8+
- CUDA (optional, for GPU acceleration)

## How It Works

1. **Data Import**: `import.py` processes recipe data, generates embeddings, and stores everything in LanceDB
2. **AI Agent**: `agent.py` creates a PydanticAI agent with tools for searching recipes
3. **Web Interface**: `app.py` provides a Streamlit chat interface for interacting with the agent
4. **Tutorial**: `multimodal-recipe-agent.ipynb` walks through the implementation step-by-step

## Development

This project demonstrates:
- Building AI agents with multimodal capabilities
- Using LanceDB for vector storage and retrieval
- Creating custom tools for PydanticAI agents
- Building conversational interfaces with Streamlit
- Handling both text and image inputs in a single agent

## License

This project is part of the LanceDB tutorials and follows the same license terms.
