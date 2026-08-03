![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Simple LLM App with LCEL

<br>

---
## Deployment on Render

https://lab-llmchain-lcel.onrender.com


<br>

---


## Some problems I run on this LAB with Langsmith: 

1. I setup my Langsmith/Langchain account for EU, so many things changed in order to reach Langsmith:  


```python
import os
from google.colab import userdata

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = userdata.get('LANGCHAIN_API_KEY')  # the NEW rotated key
os.environ["LANGSMITH_PROJECT"] = "Ironhack First app"

# also set legacy names in case an older SDK version still checks these
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGSMITH_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = "Ironhack First app"

os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')


### --------- ###
### --------- ###
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-3.5-turbo")

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="My tailor is rich"),
]

model.invoke(messages)


```


---

2. Also,  LangServe has been deprecated since Nov 18, 2024, and LangChain recommends using LangGraph Platform instead for new projects. And the GitHub repo itself was archived by the owner on May 5, 2026, making it read-only — meaning it's no longer maintained at all, even for community bug fixes going forward. If you're following an older tutorial (like the LangChain quickstart), it's worth knowing this part is now legacy.

Hence, decision to host on Render: https://lab-llmchain-lcel.onrender.com

<br>

---

---

## Getting Started

Follow the instructions provided in the notebook.

Read the instructions for each cell and provide your answers. Make sure to test your answers in each cell and save. Jupyter Notebook should automatically save your work progress. But it's a good idea to periodically save your work manually just in case.

## Deliverables

- Downloaded notebook with your responses to each of the exercises.


## Submission

- Upon completion, add your deliverables to git. 
- Then commit git and push your branch to the remote.
- Make a pull request and paste the PR link in the submission field in the Student Portal.

<br>

**Good luck!**
