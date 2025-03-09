import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import requests

# Load environment variables from .env
load_dotenv()

# API Keys
OPENROUTER_API_KEY = "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"
HUGGINGFACE_API_KEY = "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"
GOOGLE_SAFE_BROWSING_API_KEY = "AIzaSyDS82GUOG9thmTO_D3Fo_jlJRsobzCZTEc"
YOUTUBE_API_KEY = "AIzaSyBxohklDc5VRKrA8IrxM450Jg2xfm2Qw8c"

app = FastAPI()

# ✅ AI Models Available
AI_MODELS = {
    "chatgpt": "openai/gpt-4-turbo",
    "gemini": "google/gemini-pro",
    "copilot": "microsoft/gpt-4-turbo",
    "claude": "anthropic/claude-3-opus",
    "deepseek": "deepseek-ai/deepseek-67b-chat",
    "dolphin": "cognitivecomputations/dolphin-2.5-mixtral",
    "llama": "meta-llama/llama-3-70b-instruct"
}

### ✅ AI AGGREGATION ENDPOINT (Selects Best Response)
@app.get("/ai-chat/")
def ai_chat(prompt: str):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    responses = {}

    for model_name, model_id in AI_MODELS.items():
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={"model": model_id, "messages": [{"role": "user", "content": prompt}]}
        )
        if response.status_code == 200:
            responses[model_name] = response.json()["choices"][0]["message"]["content"]

    if not responses:
        raise HTTPException(status_code=500, detail="AI Chat Failed")

    # ✅ Select the best response based on word count & clarity
    best_response = max(responses.values(), key=len)
    return {"response": best_response}


### ✅ AI-POWERED AUTO DEBUGGING FOR CODE GENERATION
@app.get("/debug-code/")
def debug_code(code: str):
    debug_prompt = f"Check this code for errors and optimize it:\n\n{code}\n\nFix bugs, optimize, and return correct output."
    
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={"model": "openai/gpt-4-turbo", "messages": [{"role": "user", "content": debug_prompt}]}
    )

    if response.status_code == 200:
        fixed_code = response.json()["choices"][0]["message"]["content"]
        return {"debugged_code": fixed_code}

    raise HTTPException(status_code=500, detail="Code Debugging Failed")


### ✅ GOOGLE SAFE BROWSING CHECK (For APK & File Safety)
@app.get("/check-url/")
def check_url(url: str):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {"clientId": "LordAI", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200 and "matches" in response.json():
        return {"status": "Unsafe"}
    return {"status": "Safe"}


### ✅ YOUTUBE VIDEO SEARCH & DOWNLOAD
@app.get("/youtube-search/")
def youtube_search(query: str):
    api_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="YouTube Search Failed")


@app.get("/youtube-download/")
def youtube_download(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return {"download_link": f"https://yt1s.com/api/ajaxSearch/index?url={video_url}"
