from openai import OpenAI
from ChatBot import settings
from pgvector.django import L2Distance


def chat(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    frequence_penalty: int | None = None,
    temperature: int | None = None,
):
    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model,
        frequency_penalty=0,
        temperature=temperature,
        n=1,
    )


def get_embedding(text: str):
    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    text = text.replace("\n", " ")

    response = client.embeddings.create(
        input=text, model="text-embedding-ada-002", encoding_format="float"
    )

    return response.data[0].embedding


def get_prompt(context: str, query: str) -> str:
    prompt = f"""Given a context try to answer the user's question with the data in the context.
    if you can't find the answer in the document do not try to make it up but instead simply answer 'I don't know'.
    context: {context}
    user's question: {query}
    """

    return prompt


def get_conversation_title(query: str):
    prompt = (
        f"""Generate a short conversation title for the given prompt.\nPrompt:{query}"""
    )

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    title = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-3.5-turbo",
        frequency_penalty=1,
        n=1,
        temperature=1,
    )

    return title.choices[0].message.content
