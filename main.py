from fastapi import FastAPI
from spotapi import Song

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My Spotify API is successfully running!"}

@app.get("/search")
def search_spotify(q: str, limit: int = 10):
    try:
        # Initialize SpotAPI
        song = Song()
        
        # Search Spotify using the user's query ('q')
        songs_data = song.query_songs(q, limit=limit)
        
        # Extract the list of tracks from Spotify's data
        tracks = songs_data["data"]["searchV2"]["tracksV2"]["items"]
        
        # Clean up the results so they look nice
        results =[]
        for item in tracks:
            track_name = item['item']['data']['name']
            results.append({"song_name": track_name})
            
        return {"search_query": q, "results": results}
        
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}
