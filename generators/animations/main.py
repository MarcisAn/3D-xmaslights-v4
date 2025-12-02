# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from decimal import Decimal, InvalidOperation
from typing import Optional
import threading
import uvicorn
import os
import sys
from AnimationBuilder import AnimationBuilder
import requests

# --- CORS ---
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Counter + Decimal Append API")

# Configure CORS
# Edit this list to include the exact origins you want to allow.
# For local dev examples:
origins = [
    "*",
]

# Warning: allow_origins=["*"] will allow any origin (not safe for production when credentials are used).
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins
    allow_credentials=True,  # True if your frontend needs to send cookies/auth
    allow_methods=["*"],  # allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # allow all headers (or list specific headers)
)

# Internal state
_counter_lock = threading.Lock()
_counter = 0  # in-memory counter

_file_lock = threading.Lock()
DEFAULT_FILE_PATH = "numbers.txt"
# Ensure file exists
open(DEFAULT_FILE_PATH, "a").close()


class DecimalItem(BaseModel):
    # Accept decimal as a string or numeric in JSON, pydantic will coerce.
    value: Decimal
    file_path: Optional[str] = None  # optional override of file path


@app.post("/nextlight")
def nextlight():
    """
    Increment the internal counter by 1 and return the new count.
    """
    global _counter
    with _counter_lock:
        _counter += 1
        new_count = _counter

    color_bytes = []
    for led in range(400):
        if led == new_count:
            color_bytes.append(255)
            color_bytes.append(255)
            color_bytes.append(255)

        else:
            color_bytes.append(0)
            color_bytes.append(0)
            color_bytes.append(0)

    print(len(color_bytes))
    req = requests.post(
        "https://ledserver.andersons-m.lv/animationIsGenerated",
        # "http://localhost:3000/animationIsGenerated",
        data=bytearray(color_bytes),
    )
    print(req.status_code)

    return {"count": new_count}


@app.post("/appenddecimal")
def append_decimal(item: DecimalItem):
    """
    Append the provided decimal value to a text file as a new line.
    JSON body example:
        { "value": "1.2345" }
    Optionally provide "file_path" to append to a different file.
    """
    # Validate decimal more strictly (pydantic already parses, but guard anyway)
    try:
        # Ensure Decimal is valid (pydantic parsed it)
        dec_value = Decimal(item.value)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid decimal value: {exc}")

    file_path = item.file_path or DEFAULT_FILE_PATH
    # Create directory if necessary
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

    line = format(
        dec_value, "f"
    )  # plain string representation (no scientific notation)
    # Append thread-safe
    try:
        with _file_lock:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to append to file: {exc}")

    return {"appended": line, "file": file_path}


@app.get("/count")
def get_count():
    """
    Return the current counter value without incrementing.
    """
    with _counter_lock:
        return {"count": _counter}


if __name__ == "__main__":
    color_bytes = []
    for led in range(400):
        if led == 0:
            color_bytes.append(255)
            color_bytes.append(255)
            color_bytes.append(255)

        else:
            color_bytes.append(0)
            color_bytes.append(0)
            color_bytes.append(0)

    print(len(color_bytes))
    req = requests.post(
        "https://ledserver.andersons-m.lv/animationIsGenerated",
        # "http://localhost:3000/animationIsGenerated",
        data=bytearray(color_bytes),
    )
    print(req.status_code)
    # Development server; in production use uvicorn/gunicorn as you prefer.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
