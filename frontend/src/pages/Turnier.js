import {Box, Typography} from '@mui/material'
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Turnier = () => {


  const Navigate = useNavigate()
  const [turniere, setturniere] = useState([])

  useEffect(() => {
    fetch('/lolturnier/turnier')
    .then((res) => res.json())
    .then((data) => {
      setturniere(data)
    })
  }, [])


  return ( 
    <Box color="textPrimary">
      {turniere && turniere.map((e) => {
        return (
          <Box onClick={() => {Navigate(`/turniere/${e.id}`)}}>

            <Typography>Turnier-Info: {e.name} {e.team_size}</Typography>
          </Box>
        )
      })}
    </Box>
   );
}
 
export default Turnier;