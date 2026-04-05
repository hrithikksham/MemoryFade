from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(
    memories: list[str],
    query: str,
    model: str = "llama-3.3-70b-versatile"  # updated from llama3-70b-8192
) -> str:

    if not memories:
        return "I don't have that memory yet."

    context = "\n".join(
        [f"{i+1}. {m}" for i, m in enumerate(memories)]
    )

    prompt = f"""
You are MemoryFade, a precise AI memory assistant.

Rules:
- Use ONLY the provided memories
- Do NOT make assumptions
- Do NOT hallucinate
- If information is missing, say:
  "I don't have that memory yet."

Memories:
{context}

Question:
{query}

Provide structured response:

Answer:
Memory References:
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()