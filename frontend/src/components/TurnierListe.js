import { Box, List, ListItem, Typography, ListItemButton } from "@mui/material";
import { useNavigate } from "react-router-dom";


const TurnierListe = ({liste}) => {

  const Navigate = useNavigate()



  return ( 

    <List >
      {liste && liste.map((e) => {

        return (
          <ListItemButton onClick={() => {Navigate(`/turniere/${e.id}`)}}>

            <Typography>Turnier-Info: {e.name} {e.team_size} {e.slots}</Typography>
            
          </ListItemButton>
        )
      })}
    </List>
   );
}
 
export default TurnierListe;