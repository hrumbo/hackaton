from dotenv import load_dotenv
import os
import openai

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded correctly
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing! Check your .env file.")

# Use the updated OpenAI SDK method
client = openai.OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello, how are you?'}],
    max_tokens=50
)

print(response.choices[0].message.content)
