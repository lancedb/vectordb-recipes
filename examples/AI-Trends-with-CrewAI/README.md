[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/AI-Trends-with-CrewAI/CrewAI_AI_Trends.ipynb)



## AI Trends Searcher using CrewAI Agents
This example is about how to make an AI Trends Searcher using **CrewAI Agents** and their Tasks. But before diving into that, let's first understand what CrewAI is and how we can use it for these applications.

![alt text](<../../assets/crewai.png>)

### What is CrewAI?

CrewAI is an open-source framework that helps different AI agents work together to do tricky stuff. You can give each Agent its tasks and goals, manage what they do, and help them work together by sharing tasks. These are some unique features of CrewAI:

1. Role-based Agents: Define agents with specific roles, goals, and backgrounds to provide more context for answer generation.
2. Task Management: Use tools to dynamically define tasks and assign them to agents.
3. Inter-agent Delegation: Agents can share tasks to collaborate better.

#### LLM
This Example can use **OPENAI_GPT4** and **GEMINI_PRO** either of them as LLM.

#### Embedding Function
This Example uses **OpenEmbedding function** for OpenAI LLM and **LLamaFile Embedding function** for Gemini Pro LLM

[Read More in Blog](https://blog.lancedb.com/track-ai-trends-crewai-agents-rag/)