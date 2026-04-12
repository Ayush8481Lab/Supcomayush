import requests
from fastapi import FastAPI

app = FastAPI()

# 🔥 PASTE YOUR SPDC COOKIE VALUE HERE 🔥
SPDC_COOKIE = "AQDoKbfVs_vcCukgZ5ULE5OmH3KGLPYgBuIFgI2EDD2KtbLp_RyOmmXSgeK7vEXP9YNJ7qAsFdaQILEpA7Jr-plHWkftojOD7xjRnMinxnlvEMz5E0Bjzq1ID3ihwocTTHuC01cnPXrDso69eKPFU9-1nCKjyU4Y5GK8onmiutPhRnrvMmkZKssLkk-f6m4hTJ_oUW3jGLx5KKxgMeISmRuPGjEsqdORhofeWUMkf9FCdCW7ST7gpKkCyjYTlCkURkduBJhSpWbEfQ"

def get_token_with_spdc():
    """Uses your spdc cookie to generate a valid Spotify access token."""
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # We pass the spdc cookie here to prove we are a logged-in user
        "Cookie": f"spdc={SPDC_COOKIE}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("accessToken")
    else:
        raise Exception(f"Spotify rejected the cookie. Status: {response.status_code}")

@app.get("/")
def home():
    return {"message": "My Unofficial SPDC Cookie API is running perfectly on Vercel!"}

@app.get("/search")
def search_spotify(q: str, limit: int = 10):
    try:
        # 1. Get the token silently using your cookie
        token = get_token_with_spdc()
        
        # 2. Use the token to search Spotify!
        url = f"https://api.spotify.com/v1/search?q={q}&type=track&limit={limit}"
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # 3. Format the results beautifully
        tracks = data.get("tracks", {}).get("items",[])
        
        results =[]
        for item in tracks:
            results.append({
                "song_name": item["name"],
                "artist": item["artists"][0]["name"],
                "spotify_url": item["external_urls"]["spotify"]
            })
            
        return {"search_query": q, "results": results}
        
    except Exception as e:
        return {"error": "Failed to search", "details": str(e)}
