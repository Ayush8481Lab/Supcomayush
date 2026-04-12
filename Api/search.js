// api/search.js

export default async function handler(req, res) {
  // Set CORS headers so you can call this API from any frontend
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');

  const { query } = req.query;

  // Check if the user provided a search term
  if (!query) {
    return res.status(400).json({ 
      error: 'Please provide a search query. Example: /api/search?query=starboy' 
    });
  }

  try {
    // 1. Unofficial Bypass: Fetch an anonymous temporary token used by the Web Player
    const tokenResponse = await fetch('https://open.spotify.com/get_access_token?reason=transport&productType=web_player');
    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.accessToken;

    if (!accessToken) {
      throw new Error("Failed to generate anonymous Spotify token.");
    }

    // 2. Search Spotify using the anonymous token (limit to top 5 results to be fast)
    const searchUrl = `https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=track&limit=5`;
    const searchResponse = await fetch(searchUrl, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    const searchData = await searchResponse.json();

    // 3. Format the data into exactly what you requested
    const formattedResults = searchData.tracks.items.map(track => ({
      title: track.name,
      artist: track.artists.map(artist => artist.name).join(', '), // Joins multiple artists if they exist
      banner_link: track.album.images[0]?.url || null, // Grabs the highest quality album art
      spotify_link: track.external_urls.spotify
    }));

    // 4. Send the successful response
    return res.status(200).json({
      success: true,
      query: query,
      results: formattedResults
    });

  } catch (error) {
    return res.status(500).json({ 
      success: false, 
      error: 'Internal Server Error', 
      details: error.message 
    });
  }
}
