import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, are you alive?"}],
        max_tokens=50,
    )
    print("✅ API key is working!")
    print("Bot says:", response.choices[0].message.content)
except Exception as e:
    print("❌ API call failed:", e)

