import { Box, List, Typography, ListItem } from "@mui/material";
import { useEffect, useContext, useState } from "react";
import { UserContext } from '../App';
import { useGet } from '../components/useFetch'
import LinearProgress from '@mui/material/LinearProgress';
import TurnierListe from "../components/TurnierListe";

const MeineTurniere = () => {

  const {user} = useContext(UserContext)

  const {data, isPending, error} = useGet(`/lolturnier/turnier-by-user-id/${user.user_id}`)

  return ( 
    <Box>
      
      {isPending && <LinearProgress/>}
      {error && <Typography color="error" >{error}</Typography>}

      <TurnierListe liste={data}></TurnierListe>

      
    </Box>
    
   );
}
 
export default MeineTurniere;