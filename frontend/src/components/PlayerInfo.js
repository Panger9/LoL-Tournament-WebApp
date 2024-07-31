import { Box, SvgIcon, Typography } from "@mui/material";
import RankMean from "./RankMean";
import { Link, useNavigate } from "react-router-dom";
import LaunchOutlinedIcon from '@mui/icons-material/LaunchOutlined';

const Playerinfo = ({ name, tag, level, tier, rank, profileIconId }) => {

  const Navigate = useNavigate()

  return (


    <Box sx={{ display: "flex", flexDirection: "row", gap: "15px", alignContent: "center", backgroundColor: "rgb(0,0,0,0.4)", padding: "10px 25px 10px 15px", borderRadius: "20px", maxWidth:"fill-content" }}>

      <Box
        component="img"
        sx={{
          height: "46px",
          borderRadius: "13px"
        }}
        alt="Profile Pic"
        src={`https://ddragon.leagueoflegends.com/cdn/14.14.1/img/profileicon/${profileIconId}.png`}
      />

      <Box sx={{ display: "flex", flexDirection: "column", width: "500px" }}>
        <Box sx={{ display: "flex", flexDirection: "row", justifyContent: "space-between", gap: "5px", alignItems:"center" }}>
            <a
            href={`https://www.op.gg/summoners/euw/${name}-${tag}`}
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: 'none', color: 'inherit' }}
            >
            <Typography sx={{':hover':{color:"rgba(215,215,255,0.7)"}}}>{name}</Typography>
            

            </a >
            <Typography>#{tag}</Typography>
        </Box>
        <Box sx={{ display: "flex", flexDirection: "row", justifyContent: "space-between", gap: "5px" }}>
          <Typography color="textSecondary" variant="body2">{level}</Typography>
          <Typography color="textSecondary" variant="body2">{tier ? tier + ' ' + rank: 'UNRANKED'}</Typography>
        </Box>
      </Box>
    </Box>
    

  );
}

export default Playerinfo;