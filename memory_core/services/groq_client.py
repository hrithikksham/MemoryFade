from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Memora, an intelligent personal memory assistant.

Your job is to answer questions using ONLY the memories provided to you.

Rules you must always follow:
- Answer strictly from the provided memories — never invent or assume facts
- If the memories do not contain enough information, say exactly: "I don't have enough information in my memories to answer this."
- Be concise — 1 to 3 sentences maximum
- Do not mention memory numbers, indices, or internal system details
- Do not say things like "based on memory 1" — just answer naturally
- If multiple memories are relevant, synthesize them into one clear answer"""


def generate_answer(
    memories: list[str],
    query: str,
    model: str = "llama-3.3-70b-versatile"
) -> str:

    if not memories:
        return "I don't have enough information in my memories to answer this."

    context = "\n".join(
        [f"- {m}" for m in memories]
    )

    user_prompt = f"""Memories:
{context}

Question: {query}

Answer in 1-3 sentences using the memories above and help with generalization."""

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.3,
            max_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[GROQ ERROR] {e}")
        return "Something went wrong while generating an answer. Please try again."