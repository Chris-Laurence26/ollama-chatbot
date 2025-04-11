from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

# FastAPI server
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.get("/ask")
def ask_question(q: str):
    """
    Handles GET requests from Flutter and Tkinter.
    Sends the user's question to Ollama and returns a response.
    """
    data = {
        "model": "mistral",  # Change to any Ollama model
        "prompt": q,
        "stream": False
    }
    
    response = requests.post(OLLAMA_API_URL, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get a response from Ollama."}

# Tkinter GUI for local testing
import tkinter as tk
from tkinter import simpledialog, messagebox

def tkinter_app():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    while True:
        user_input = simpledialog.askstring("Ollama Chat", "Ask a question:")
        
        if user_input is None:  # User canceled
            break
        
        response = requests.get(f"http://localhost:8000/ask?q={user_input}")
        
        if response.status_code == 200:
            answer = response.json().get("response", "No response")
        else:
            answer = "Error: Could not fetch response."
        
        messagebox.showinfo("Response", answer)

# Run Tkinter in a separate thread (optional)
if __name__ == "__main__":
    import threading
    threading.Thread(target=tkinter_app).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
