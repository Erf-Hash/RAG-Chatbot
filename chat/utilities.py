import json
from openai import OpenAI


def get_embedding(text: str):
    client = OpenAI(
        api_key="C9vpBLBZkAbvbvimiOogyxJ8bOiLRkv3",
        base_url="https://openai.torob.ir/v1",
    )

    text = text.replace("\n", " ")

    response = json.loads(
        client.embeddings.create(
            input=text, model="text-embedding-ada-002", encoding_format="float"
        )
    )
    return response["data"][0]['embedding']
