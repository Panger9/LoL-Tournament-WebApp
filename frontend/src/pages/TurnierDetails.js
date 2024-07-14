import {Box, Typography} from '@mui/material'
import { useEffect, useState } from 'react';

const TurnierDetails = () => {

  const [userList, setUserList] = useState([])

  useEffect(() => {
    fetch('/lolturnier/user')
    .then((res) => res.json())
    .then((data) => {
      setUserList(data)
    })
  }, [])

  return ( 
    <Typography color="textPrimary">
      {userList && userList.map((e) => {
        return (
          <Box>
            <Typography>Summoner Name: {e.sum_name} {e.tag_line}</Typography>
          </Box>
        )
      })}
    </Typography>
   );
}
 
export default TurnierDetails;