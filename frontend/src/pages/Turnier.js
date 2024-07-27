import {Box, Typography} from '@mui/material'
import { useEffect, useState } from 'react';

const Turnier = () => {

  const [userList, setUserList] = useState([])

  useEffect(() => {
    fetch('/lolturnier/turnier')
    .then((res) => res.json())
    .then((data) => {
      setUserList(data)
    })
  }, [])

  return ( 
    <Box color="textPrimary">
      {userList && userList.map((e) => {
        return (
          <Box>
            <Typography>STANDARD TURNIERSEITE</Typography>
            <Typography>Turnier-Info: {e.name} {e.team_size}</Typography>
          </Box>
        )
      })}
    </Box>
   );
}
 
export default Turnier;