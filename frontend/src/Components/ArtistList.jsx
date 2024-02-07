
// import './ArtistList.css';
import React, { useEffect, useState } from "react";
import { Link, generatePath } from "react-router-dom";
import axios from "axios";


function ArtistList() {
    const [artists, setArtists] = useState([]);
    
    const fetchArtists = async () => {
        const result = await axios.get("http://localhost:8004/v1/artists", { mode: 'no-cors' });
        console.log(result);
        setArtists(result.data);
  }
  useEffect(() => {
    fetchArtists();
  }, []);
//   fetchArtists();

  return (
    <div className="ArtistList">
        <h1>Hi</h1>
       {artists.map(({ id, spotify_display_name }) => (
        <div className="artist-list-item" key={id}>
            <h1>1</h1>
          <Link to={generatePath(`/artists/:id`, { id })}>{spotify_display_name}</Link>
        </div>
      ))}
    </div>
  );
}

export default ArtistList;
