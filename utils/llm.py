import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv(
    "GROQ_API_KEY"
)

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)

def create_prompt(
        context,
        question,
        chat_history
):

    prompt = f"""
You are an AI Research Assistant.

Use ONLY the provided context to answer.

You are also given previous conversation history.

Use the conversation history to understand follow-up questions.

Examples:

User: What is the title?
Assistant: Attention Is All You Need.

User: Who are its authors?

Here "its" refers to
"Attention Is All You Need".

Previous Conversation:
{chat_history}

Document Context:
{context}

Current Question:
{question}

If the answer cannot be found
in the context, say:

"I could not find this information in the uploaded papers."

Answer:
"""

    return prompt


def generate_answer(
        context,
        question,
        chat_history
):

    prompt = create_prompt(
        context,
        question,
        chat_history
    )

    response = llm.invoke(prompt)

    return response.content