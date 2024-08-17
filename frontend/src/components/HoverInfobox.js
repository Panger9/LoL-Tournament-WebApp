import { Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const HoverInfobox = () => {

  const Navigate = useNavigate()

  return ( 
    <Box onClick={() => Navigate('/register')} sx={{
      backgroundColor:"error.main", 
      position:"fixed", 
      bottom:"50px", 
      padding:"12px 20px", 
      boxShadow:"0px 5px 10px rgba(0,0,0)", 
      borderRadius:"3px", 
      ":hover":{cursor:"pointer", scale:"1.02", backgroundColor:"#ee6565"}, 
      ":active":{backgroundColor:"#732a2a", },
      transition:"0.15s "
      }}
      >
      <Typography variant="body2" color="#ffffff" >Du musst einen League of Legends Account verknüpfen, um Turnieren beizutreten und welche zu erstellen</Typography>
    </Box>
   );
}
 
export default HoverInfobox;