import {Box, Typography, Button, Dialog} from '@mui/material'
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const TurnierDetails = () => {

  let { TurnierId } = useParams();
  const [turnier, setTurnier] = useState('')
  const [isPending, setIsPending] = useState(false)

  useEffect (() => {

    const fetchTurnier = async () => {
      const res = await fetch('/lolturnier/turnier-by-id/' + TurnierId)
      const data = await res.json()
      setTurnier(data)
    }

    fetchTurnier()

  },[])



  return ( 
    <Box >
      {isPending && 'Daten werden geladen'}
      {turnier && 
        <Box key={turnier.id}>
          <p>Id: {turnier.id}</p>
          <p>Name: {turnier.name}</p>
          <p>Teamgröße: {turnier.team_size}</p>
        </Box>
      }
    </Box>
   );
}
 
export default TurnierDetails;