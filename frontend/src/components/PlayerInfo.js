import { Box, Typography } from "@mui/material";
import RankMean from "./RankMean";

const Playerinfo = ({name, tag, level, tier}) => {

  console.log(RankMean(['challenger', 'diamond 2']))

  return ( 

    <Box sx={{display:"flex", flexDirection:"column"}}>
      <Box sx={{display:"flex", flexDirection:"row", justifyContent:"space-between", gap:"5px"}}>
        <Typography>{name}</Typography>
        <Typography>#{tag}</Typography>
      </Box>
      <Box sx={{display:"flex", flexDirection:"row", justifyContent:"space-evenly", gap:"5px"}}>
        <Typography color="textSecondary" variant="body2">{level}</Typography>
        <Typography color="textSecondary" variant="body2">{tier}</Typography>
      </Box>
    </Box>

   );
}
 
export default Playerinfo;