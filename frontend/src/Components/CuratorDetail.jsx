// import './ArtistList.css';
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import axios from "axios";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

function CuratorDetail() {
  const [importantTracks, setImportantTracks] = useState([]);

  const { curatorId } = useParams();

  useEffect(() => {
    const fetchArtists = async () => {
      const result = await axios.get(
        `http://localhost:8004/v1/curators/${curatorId}/importantTracks`,
        { mode: "no-cors" }
      );
      console.log(result);
      setImportantTracks(result.data);
    };
    fetchArtists();
  }, [curatorId]);

  return (
    <div className="CuratorDetail">
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 700 }} aria-label="customized table">
          <TableHead>
            <TableRow>
              <StyledTableCell>Title</StyledTableCell>
              <StyledTableCell align="right">Artist</StyledTableCell>
              <StyledTableCell align="right">Popularity</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {importantTracks.map((track) => (
              <StyledTableRow key={track.id}>
                <StyledTableCell component="th" scope="row">
                  {track.name}
                </StyledTableCell>
                <StyledTableCell align="right">
                  {track.artists[0].name}
                </StyledTableCell>
                <StyledTableCell align="right">
                  {track.popularity}
                </StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default CuratorDetail;