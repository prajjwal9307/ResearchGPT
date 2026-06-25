import os
import json

SESSIONS_DIR = "sessions"

os.makedirs(
    SESSIONS_DIR,
    exist_ok=True
)


def get_saved_sessions():

    sessions = []

    for file in os.listdir(
            SESSIONS_DIR):

        if file.endswith(".json"):

            sessions.append(
                file.replace(".json", "")
            )

    return sessions


def save_chat_history(
        session_name,
        messages
):

    path = os.path.join(
        SESSIONS_DIR,
        f"{session_name}.json"
    )

    with open(path, "w") as f:

        json.dump(
            messages,
            f,
            indent=4
        )


def load_chat_history(
        session_name
):

    path = os.path.join(
        SESSIONS_DIR,
        f"{session_name}.json"
    )

    if os.path.exists(path):

        with open(path, "r") as f:

            return json.load(f)

    return []

def delete_session(session_name):
    file_path = f"sessions/{session_name}.json"

    if os.path.exists(file_path):
        os.remove(file_path)