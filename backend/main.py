import os
import csv

from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


