from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    print({"message": "Welcome to allcsvideos"})
