import json
import sys

import anthropic

from . import memory as mem
from .prompt import MEMORY_UPDATE, SYSTEM

MODEL = "claude-opus-5-5"
client = anthropic.Anthropic()


def update_memory(memory: dict, messages: list) -> dict:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=messages
        + [{"role": "user", "content": MEMORY_UPDATE.format(memory=json.dumps(memory))}],
    )
    text = resp.content[0].text
    try:
        return json.loads(text[text.index("{") : text.rindex("}") + 1])
    except ValueError:
        return memory  # keep old memory rather than corrupt it


def main() -> None:
    memory = mem.load()
    system = SYSTEM.format(memory=json.dumps(memory, indent=2))
    messages: list = []
    print("Your coach is here. Type 'quit' to end the session.\n")

    # Let the coach open the conversation (follow-ups from last time included).
    messages.append({"role": "user", "content": "[session start: greet me and open the session]"})
    while True:
        print("Coach: ", end="", flush=True)
        reply = ""
        with client.messages.stream(
            model=MODEL, max_tokens=1500, system=system, messages=messages
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
                reply += chunk
        print("\n")
        messages.append({"role": "assistant", "content": reply})

        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            user = "quit"
        print()
        if user.lower() in {"quit", "exit"}:
            break
        messages.append({"role": "user", "content": user or "(no reply)"})

    if len(messages) > 2:
        print("Saving what I learned...")
        mem.save(update_memory(memory, messages))


if __name__ == "__main__":
    sys.exit(main())
