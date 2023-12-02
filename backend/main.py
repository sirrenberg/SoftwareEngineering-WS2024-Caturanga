from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient
from flee_adapter import adapter

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/run_simulation")
def run_simulation():
    return adapter.Adapter().run_simulation()


