import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ["MODAL_PROXY_BASE_URL"],
    api_key="unused",
    default_headers={
        "Modal-Key": os.environ["MODAL_PROXY_TOKEN_ID"],
        "Modal-Secret": os.environ["MODAL_PROXY_TOKEN_SECRET"],
    },
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful and concise assistant.",
    }
]

print("Chatbot started. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not user_input:
        continue

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    stream = client.chat.completions.create(
        model="moonshotai/Kimi-K3",
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
        top_p=0.95,
        stream=True,
        extra_body={"reasoning_effort": "none"},
    )

    print("Assistant: ", end="", flush=True)

    answer_parts: list[str] = []

    for chunk in stream:
        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            answer_parts.append(content)

    print("\n")

    answer = "".join(answer_parts)

    if not answer:
        print("No response returned.\n")
        continue

    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )