import { Box, Typography } from "@mui/material";
import RankMean from "./RankMean";

const Playerinfo = ({ name, tag, level, tier, profileIconId }) => {

  return (

    <Box sx={{ display: "flex", flexDirection: "row", gap:"15px", alignContent:"center", backgroundColor:"rgb(0,0,0,0.4)", maxWidth:"fit-content", padding:"10px 25px 10px 15px", borderRadius:"20px" }}>

      <Box
        component="img"
        sx={{
          height: "46px",
          borderRadius: "13px"
        }}
        alt="Profile Pic"
        src={`https://ddragon.leagueoflegends.com/cdn/14.14.1/img/profileicon/${profileIconId}.png`}
      />

      <Box sx={{ display: "flex", flexDirection: "column" }}>
        <Box sx={{ display: "flex", flexDirection: "row", justifyContent: "space-between", gap: "5px" }}>
          <Typography>{name}</Typography>
          <Typography>#{tag}</Typography>
        </Box>
        <Box sx={{ display: "flex", flexDirection: "row", justifyContent: "space-between", gap: "5px" }}>
          <Typography color="textSecondary" variant="body2">{level}</Typography>
          <Typography color="textSecondary" variant="body2">{tier ? tier : 'unranked'}</Typography>
        </Box>
      </Box>
    </Box>

  );
}

export default Playerinfo;