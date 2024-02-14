import logo from "./logo.svg";
import "./App.css";

function App() {
  const SPOTIFY_CLIENT_ID = "-----------------------------";
  const REDIRECT_URI = "http://localhost:3000/spotifyRedirect";
  const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize";
  const RESPONSE_TYPE = "token";

  return (
    <div className="App">
      <header className="App-header">
        <a href={`http://localhost:8004/v1/auth/spotify/authorize`}>
          Login to Spotify
        </a>
      </header>
    </div>
  );
}

export default App;
