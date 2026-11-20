from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1/models", api_key="lm-studio")

try:
    client.models.list()
except Exception as e:
    print(f"An error occurred: {e}")