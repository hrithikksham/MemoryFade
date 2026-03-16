from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(memories: list[str], query: str) -> str:
    context = "\n".join([f"{i+1}. {m}" for i, m in enumerate(memories)])

    prompt = f"""Context memories:

{context}

Question:
{query}

Answer using the context provided."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

    