# 🌍 Swarm Style Travel Planner

A sophisticated travel planning assistant powered by multi-agent collaboration and vector search capabilities. This project demonstrates the power of specialized AI agents working together to provide comprehensive travel planning assistance.

## ✨ Key Features

- 🚀 **Multi-Agent Collaboration** – Specialized agents work together, seamlessly passing context to one another
- 🔧 **Customizable Handoff Tools** – Built-in mechanisms for smooth communication between agents
- 📂 **LanceDB for Data Retrieval** – High-performance vector search and full-text search for accurate and fast information retrieval
- 🌍 **Travel Agent Use Case** – Agents collaborate to handle different aspects of travel planning, ensuring efficient and context-aware responses

## 🛠 Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment tool (venv, conda, etc.)

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/swarm_style_planner.git
   cd swarm_style_planner
   ```

2. **Set up a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💡 How It Works

The Swarm Style Travel Planner uses a sophisticated multi-agent system where different specialized agents handle various aspects of travel planning:

1. **Flight Search Agent**: Handles flight-related queries and searches
2. **Hotel Search Agent**: Manages hotel and accommodation searches
3. **Coordination Agent**: Orchestrates communication between agents and maintains context

The system uses LanceDB for efficient vector search capabilities, allowing for semantic understanding of user queries and fast retrieval of relevant travel information.

## 🎯 Usage

1. Launch the application using `streamlit run app.py`
2. Enter your travel-related query in the chat interface
3. The system will automatically:
   - Parse your requirements
   - Route queries to appropriate specialized agents
   - Provide comprehensive travel suggestions
   - Maintain context throughout the conversation

Example queries:
- "Find me flights from New York to London next month"
- "I need a hotel in Paris near the Eiffel Tower"
- "Plan a week-long trip to Tokyo with flights and hotels"

## 🏗 Project Structure

```
swarm_style_planner/
├── app.py              # Main Streamlit application
├── models.py           # Data models for flights and hotels
├── travel_agent_swarm/ # Core swarm logic and agent definitions
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## 📦 Dependencies

- streamlit
- lancedb
- sentence-transformers
- pydantic
- langgraph
- torch

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Streamlit and LangGraph
- Uses LanceDB for vector search capabilities
- Powered by sentence-transformers for embeddings
