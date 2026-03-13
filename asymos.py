import pyautogui
import base64
import requests
from PIL import Image
import io

OLLAMA_URL = "http://localhost:11434/api/generate"

def screenshot():
    img = pyautogui.screenshot()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def ask_agent(image_bytes):

    img_base64 = base64.b64encode(image_bytes).decode()

    prompt = """
You are controlling a computer.
Look at the screenshot and decide ONE action.

Return JSON only.

Actions:
click(x,y)
type(text)
wait()

Example:
{"action":"click","x":500,"y":400}
"""

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2-vision",
            "prompt": prompt,
            "images": [img_base64],
            "stream": False
        }
    )

    return r.json()["response"]

def execute(action):

    import json
    a = json.loads(action)

    if a["action"] == "click":
        pyautogui.click(a["x"], a["y"])

    if a["action"] == "type":
        pyautogui.write(a["text"])

    if a["action"] == "wait":
        pyautogui.sleep(2)

while True:

    img = screenshot()
    decision = ask_agent(img)

    print("Agent:", decision)

    execute(decision)