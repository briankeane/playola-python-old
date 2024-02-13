
// import './ArtistList.css';
import React, { useEffect, useState } from "react";
import { Link, generatePath, useParams } from "react-router-dom";
import axios from "axios";


function ArtistDetail() {
    const [artists, setArtists] = useState([]);
    const [shortTermSongs, setShortTermSongs] = useState([]);

    const { artistId } = useParams();
    
    const fetchArtists = async () => {
        const result = await axios.get(`http://localhost:8004/v1/artists/${artistId}/shortTermTracks`, { mode: 'no-cors' });
        console.log(result);
        setShortTermSongs(result.data);
  }
  useEffect(() => {
    fetchArtists();
  }, []);
//   fetchArtists();

  return (
    <div className="ArtistDetail">

       {artists.map(({ id, spotify_display_name }) => (
        <div className="artist-list-item" key={id}>
            <h1>1</h1>
         
        </div>
      ))}
    </div>
  );
}

export default ArtistDetail;
