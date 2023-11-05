### Overview
The Autonomous HR Assistant (HRA) Chatbot is your personal HR chatbot designed to assist with HR-related queries. It utilizes open-source models, advanced embeddings, and the Langchain framework with tools and a React agent.

This chatbot is designed to help answer a wide range of HR-related questions, making it a valuable tool for both employees and HR professionals. If the chatbot is unable to provide an answer, it will respond with a "don't know."


![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/4a9cc0cf-576e-4301-bc95-f34a146db432)


### Data Sources
The HRA Chatbot is powered by two main data sources:

HR Policy Data: The HR policy data is generated using open-source models and serves as the knowledge base for answering policy-related questions.

Employee Data: Dummy employee data is used for demonstration purposes. You have the flexibility to replace this data with your organization's employee data.


Using LanceDB as Vectordb
To facilitate efficient document retrieval and similarity-based queries, we utilize LanceDB as the vectordb. LanceDB helps optimize the chatbot's performance by enabling fast and accurate information retrieval.

## Getting Started
Follow these steps to run the Autonomous HR Assistant Chatbot:

```
## main.py
## Change these files for custom data.I'm using aks desai  as a default user 
chatbot = HRChatbot("data/employee_info.csv", "data/hr_policy_sample.txt", "aks desai")

```

### Install Requirements
Use pip to install the necessary dependencies by running:

```
pip install -r requirements.txt
```
### Run the Code
following command to start the chatbot:

```
streamlit run main.py
```

The chatbot will be accessible through a web interface where you can input your HR-related queries.

### Customization
This codebase serves as a simple prototype. You have the freedom to extend and customize it according to your organization's specific requirements. You can integrate additional logic and data sources as needed to enhance the capabilities of your HR chatbot.

For more advanced use cases or for deploying the chatbot in a production environment, consider consulting with a software development team to ensure scalability, security, and performance.

