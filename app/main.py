from fastapi import FastAPI

app = FastAPI(title="Finance Tracker", version="1.0.0")

@app.get("/")
def hello_api():
    return {"msg":"Hello FastAPI"}