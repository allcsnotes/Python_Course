import time

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def send_welcome_email(email: str):
    time.sleep(2)  # pretend to talk to the mail service
    print("email sent to", email, flush=True)


@app.post("/enrol", status_code=201)
def enrol(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome_email, email)
    return {"enrolled": email}
