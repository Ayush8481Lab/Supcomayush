import os

# 🔥 THE VERCEL HACK: Redirect hidden files to the /tmp folder
# This fixes the 500 Error by bypassing Vercel's read-only file system
os.environ["HOME"] = "/tmp"

from fastapi import FastAPI
from spotapi import Song

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My Unofficial Spotify API is successfully running on Vercel!"}

@app.get("/search")
def search_spotify(q: str, limit: int = 10):
    try:
        # Initialize SpotAPI (It will now safely unpack in /tmp)
        song = Song()
        
        # Search Spotify using the unofficial method
        songs_data = song.query_songs(q, limit=limit)
        
        # Extract the deep nested list of tracks
        tracks = songs_data["data"]["searchV2"]["tracksV2"]["items"]
        
        # Clean up the results
        results = []
        for item in tracks:
            track_data = item['item']['data']
            
            # Extract track name
            track_name = track_data.get('name', 'Unknown')
            
            # Extract artist name safely
            artist_name = "Unknown"
            try:
                artist_name = track_data['artists']['items'][0]['profile']['name']
            except:
                pass # If it fails to find an artist, just leave it as Unknown
                
            results.append({
                "song": track_name,
                "artist": artist_name
            })
            
        return {"search_query": q, "results": results}
        
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}
