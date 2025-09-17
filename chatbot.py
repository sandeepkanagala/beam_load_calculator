import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your-groq-api-key"

client = Groq(api_key=GROQ_API_KEY)

def structural_chatbot_response(user_query):
    prompt = f"""
You are a helpful structural engineering assistant.
User asked: "{user_query}"

Answer clearly with explanations related to structural load analysis, beam behavior, material advice, or design checks.
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a structural engineering assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1000
    )
    return response.choices[0].message.content
