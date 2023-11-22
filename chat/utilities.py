from openai import OpenAI


def get_embedding(text: str):
    client = OpenAI(
        api_key="C9vpBLBZkAbvbvimiOogyxJ8bOiLRkv3",
        base_url="https://openai.torob.ir/v1",
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
        api_key="C9vpBLBZkAbvbvimiOogyxJ8bOiLRkv3",
        base_url="https://openai.torob.ir/v1",
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
            temperature=1
        )

    return title.choices[0].message.content
