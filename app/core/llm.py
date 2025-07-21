import openai
from app.core.config import GOOGLE_API_KEY

client = openai.OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

async def generate_gemini_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content 