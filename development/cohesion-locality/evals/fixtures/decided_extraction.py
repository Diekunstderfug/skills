def create_user(data):
    if not data.get("email") or "@" not in data["email"]:
        raise ValueError("invalid email")
    ...


def update_user(data):
    if not data.get("email") or "@" not in data["email"]:
        raise ValueError("invalid email")
    ...
