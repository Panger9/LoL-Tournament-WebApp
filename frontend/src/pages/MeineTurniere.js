import { Box, List, Typography, ListItem } from "@mui/material";
import { useEffect, useContext, useState } from "react";
import { UserContext } from '../App';
import TurnierListe from "../components/TurnierListe";

const MeineTurniere = () => {

  const user = useContext(UserContext)
  const [turnierList, setTurnierList] = useState([])

  useEffect(() => {

    const fetchMeineTurniere = async () => {
      const res = await fetch(`/lolturnier/turnier-by-user-id/${user.user_id}`)
      const data = await res.json()
      console.log(data)
      setTurnierList(data)
    }

    fetchMeineTurniere()
  },[])

  return ( 
    <TurnierListe liste={turnierList}></TurnierListe>
   );
}
 
export default MeineTurniere;