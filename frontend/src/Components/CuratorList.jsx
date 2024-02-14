// import './CuratorList.css';
import React, { useEffect, useState } from "react";
import { Link, generatePath } from "react-router-dom";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Button from "@mui/material/Button";
import axios from "axios";

function CuratorList() {
  const [curators, setCurators] = useState([]);

  const fetchCurators = async () => {
    const result = await axios.get("http://localhost:8004/v1/curators", {
      mode: "no-cors",
    });
    console.log(result);
    setCurators(result.data);
  };

  useEffect(() => {
    fetchCurators();
  }, []);

  function curatorItem(curator) {
    return (
      <ListItem alignItems="flex-start">
        <Button
          component={Link}
          to={`/curators/${curator.id}`}
          variant="outlined"
          href="#outlined-buttons"
        >
          {curator.spotify_display_name}
        </Button>
      </ListItem>
    );
  }
  var curatorListItems = curators.map((curator) => curatorItem(curator));
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {curatorListItems}
    </List>
  );
}

export default CuratorList;
