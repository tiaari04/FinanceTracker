from fastapi import FastAPI
from .crud import router

app = FastAPI(title="Finance Tracker", version="1.0.0")
app.include_router(router)    

@app.get("/")
def hello_api():
    return {"msg":"Welcome to the Finance Tracker API"}