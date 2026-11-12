from rag import ask

while True:
    q = input("You: ")
    if q.lower() in ("exit", "quit"):
        break
    print("Bot:", ask(q), "\n")