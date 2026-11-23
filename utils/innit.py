import requests
import threading
import asyncio
import base64
from pystyle import *
import random
from datetime import datetime
import os
import time

def logo():
    l = """                             
                 _____ _____ _____ _____ _ _ _ _____ 
                |     |  |  |  _  |   __| | | |     |
                |   --|     |     |   __| | | |  |  |
                |_____|__|__|__|__|_____|_____|_____|              
    """
    c = Colorate.Horizontal(Colors.blue_to_purple, l)
    print(c)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def current_time():
    return datetime.now().strftime("%H:%M:%S")

b = Colors.dark_blue
r = Colors.red
g = Colors.green
y = Colors.yellow
w = Colors.white

API = "https://discord.com/api/v10"
CDN = "https://cdn.discordapp.com"
USER_AGENT = "DiscordBot (https://github.com/ChaewoCloner, 2.0)"

def load_token():
    with open('token.txt') as f:
        return f.readline().strip()

def get_headers(json_body=False):
    h = {"Authorization": load_token(), "User-Agent": USER_AGENT}
    if json_body:
        h["Content-Type"] = "application/json"
    return h

def api(method, path, max_retries=5, **kwargs):
    headers = kwargs.pop("headers", None) or get_headers(json_body="json" in kwargs)
    url = path if path.startswith("http") else f"{API}{path}"
    response = None
    for _ in range(max_retries):
        response = requests.request(method, url, headers=headers, timeout=30, **kwargs)
        if response.status_code != 429:
            return response
        try:
            retry_after = float(response.json().get("retry_after", 1))
        except Exception:
            retry_after = float(response.headers.get("Retry-After", 1))
        print(f"                {b}[{w}{current_time()}{b}]{w} {y}[x]{w} Rate-limited. Retrying after {retry_after:.1f} seconds")
        time.sleep(retry_after + 0.1)
    return response
