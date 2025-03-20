from fastapi import FastAPI, HTTPException
import httpx
import asyncio

app = FastAPI()
LOCALHOST = "127.0.0.1:8000"

WINDOW_SIZE = 10  # window size as per instructions
number_window = []  # using sliding window technique for storing numbers

THIRD_PARTY_API = "http://20.244.56.144/test"

# api path mapping for correct id
ID_MAPPING = {
    "p": "primes",
    "e": "even",
    "f": "fibo",
    "r": "rand"
}

async def fetch_numbers(numberid: str):
    mapped_id = ID_MAPPING.get(numberid)  # convert 'p' → 'primes', etc.
    if not mapped_id:
        return []
    
    url = f"{THIRD_PARTY_API}/{mapped_id}"
    
    # Logging the API call
    print(f"Fetching from: {url}")

    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json().get("numbers", [])
    except (httpx.RequestError, httpx.TimeoutException):
        return []
    
    return []

@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    global number_window

    if numberid not in ID_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid number ID: Use 'p' 'f' 'e' or 'r'")

    prev_state = number_window.copy()  # save previous state before fetching

    # fetching numbers from the test server API
    new_numbers = await fetch_numbers(numberid)

    # add unique numbers and prevent duplicates
    for num in new_numbers:
        if num not in number_window:
            if len(number_window) >= WINDOW_SIZE:
                number_window.pop(0)  # remove the oldest number
            number_window.append(num)

    avg = round(sum(number_window) / len(number_window), 2) if number_window else 0.00

    return {
        "windowPrevState": prev_state,
        "windowCurrState": number_window,
        "numbers": new_numbers,
        "avg": avg
    }