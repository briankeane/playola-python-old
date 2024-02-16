import { useEffect, useState } from "react";
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

interface Track {
    id: string
    name: string
    artists: [Artist]
    popularity: number
}

interface Artist {
    name: string
}

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
  const [importantTracks, setImportantTracks] = useState<Track[]>([]);

  const { curatorId } = useParams();

  useEffect(() => {
    const fetchCurators = async () => {
      const result = await axios.get(
        `${import.meta.env.VITE_BACKEND_BASE_URL}v1/curators/${curatorId}/importantTracks`
      );
      console.log(result);
      setImportantTracks(result.data);
    };
    fetchCurators();
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
