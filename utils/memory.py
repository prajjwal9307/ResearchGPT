def get_chat_history(messages, k=5):
    """
    Return last k messages as text.
    """

    history = []

    recent_messages = messages[-k:]

    for msg in recent_messages:

        role = msg["role"]

        if role == "user":
            history.append(
                f"User: {msg['content']}"
            )

        else:
            history.append(
                f"Assistant: {msg['content']}"
            )

    return "\n".join(history)