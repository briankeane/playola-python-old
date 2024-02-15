import "./App.css";

function App() {
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
