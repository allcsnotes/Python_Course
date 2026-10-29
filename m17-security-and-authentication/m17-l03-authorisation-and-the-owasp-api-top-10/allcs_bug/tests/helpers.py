from app.tokens import make_token


def login_as(student):
    return {"Authorization": f"Bearer {make_token(student.id)}"}
