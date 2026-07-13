import os
import sys

import requests


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "put-your-api-key-here")


def ask_bot(prompt, chat_history):
    headers = {"Content-Type": "application/json"}

    if OLLAMA_API_KEY and OLLAMA_API_KEY != "put-your-api-key-here":
        headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        headers=headers,
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI bot."},
                *chat_history,
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


def main():
    chat_history = []

    print("AI Bot using Ollama")
    print(f"Model: {OLLAMA_MODEL}")
    print("Type 'quit' to exit.")

    while True:
        prompt = input("\nYou: ").strip()

        if prompt.lower() in {"quit", "exit"}:
            print("Bot: Goodbye.")
            break

        if not prompt:
            continue

        try:
            reply = ask_bot(prompt, chat_history)
        except requests.RequestException as error:
            print(f"Error talking to Ollama: {error}", file=sys.stderr)
            continue

        print(f"Bot: {reply}")

        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
