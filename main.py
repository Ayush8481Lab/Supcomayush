from fastapi import FastAPI
import requests
import re

app = FastAPI()

def get_unofficial_token():
    """Scrapes the temporary guest token directly from Spotify's Web Player"""
    url = "https://open.spotify.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        # Search the raw HTML for the hidden access token
        match = re.search(r'"accessToken":"([^"]+)"', response.text)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None

@app.get("/")
def home():
    return {"message": "My Custom Unofficial Spotify API is successfully running on Vercel!"}

@app.get("/search")
def search_spotify(q: str, limit: int = 10):
    try:
        # 1. Get the unofficial guest token (No developer keys needed!)
        token = get_unofficial_token()
        if not token:
            return {"error": "Failed to generate unofficial Spotify token."}
            
        # 2. Use the guest token to search Spotify directly
        search_url = f"https://api.spotify.com/v1/search?q={q}&type=track&limit={limit}"
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(search_url, headers=headers)
        data = response.json()
        
        tracks = data.get("tracks", {}).get("items",[])
        
        # 3. Clean up the results so they look nice
        results =[]
        for item in tracks:
            results.append({
                "song_name": item["name"],
                "artist": item["artists"][0]["name"],
                "url": item["external_urls"]["spotify"]
            })
            
        return {"search_query": q, "results": results}
        
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}
