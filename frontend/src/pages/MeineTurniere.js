import { Box, List, Typography, ListItem } from "@mui/material";
import { useEffect, useContext, useState } from "react";
import { UserContext } from '../App';

const MeineTurniere = () => {

  const user = useContext(UserContext)
  const [turnierList, setTurnierList] = useState([])

  useEffect(() => {

    const fetchMeineTurniere = async () => {
      const res = await fetch(`/lolturnier/user-turnier-by-user-id/${user.user_id}`)
      const data = await res.json()
      setTurnierList(data)
    }

  },[])

  return ( 
    <Box> 
      {turnierList.map((turnier) => (
        <List>
          <ListItem>{turnier.name}</ListItem>
          <ListItem>{turnier.team_size}</ListItem>
        </List>
      ))}
      
    </Box>
   );
}
 
export default MeineTurniere;