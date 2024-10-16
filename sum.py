

from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpcore import Origin

sum.add_middleware(
    CORSMiddleware,
    allow_origins=Origin,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and authentication credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Authorization)
)


app = FastAPI()

@app.get("/add")
def addNum(a,b):
    return  a+b