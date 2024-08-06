import { Box, List, ListItem, Typography, ListItemButton } from "@mui/material";
import { useNavigate } from "react-router-dom";


const TurnierListe = ({liste}) => {

  const Navigate = useNavigate()



  return ( 

    <List >
      {liste && liste.map((e) => {

        return (
          <ListItemButton key={e.id} onClick={() => {Navigate(`/turniere/${e.id}`) }}>

            <Typography>Name: {e.name} </Typography>
            <Typography>Größe: {e.team_size}</Typography>
            <Typography>Owner: {e.turnier_owner}</Typography>
            <Typography>Slots: {e.slots}</Typography>
            <Typography>START: {e.start_date}</Typography>
            
          </ListItemButton>
        )
      })}
    </List>
   );
}
 
export default TurnierListe;