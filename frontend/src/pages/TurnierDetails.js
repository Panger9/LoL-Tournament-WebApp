import {Box, Typography, Button, Dialog, Grid, Paper} from '@mui/material'
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Playerinfo from '../components/PlayerInfo'

const TurnierDetails = () => {

  let { TurnierId } = useParams();
  const [turnier, setTurnier] = useState('')
  const [isPending, setIsPending] = useState(false)

  useEffect (() => {

    const fetchTurnier = async () => {
      const res = await fetch(`/lolturnier/user-by-team-and-turnier/${TurnierId}`)
      const data = await res.json()
      setTurnier(data)
    }

    fetchTurnier()

  },[])





  return ( 
    <Grid container  spacing={2} gap={5}>
      {isPending && 'Daten werden geladen'}
      {turnier && turnier.map((team, teamIndex) => (
        <Paper item key={teamIndex} sx={{padding:"20px 50px", backgroundColor:"#141414", display:"flex", flexDirection:"column", gap:"15px", borderRadius:"18px"}}>
          Team {teamIndex + 1}
          {team.map((user, userIndex) => (
            <Box key={userIndex}>
              <Playerinfo name={user.gameName} tag={user.tagLine} tier={user.tier} level={user.summonerLevel} profileIconId={user.profileIconId}></Playerinfo>
            </Box>
          ))}
          <Button variant='contained' sx={{boxShadow:"none", ':hover':{boxShadow:"none"}, ':focus':{boxShadow:"none"}}}>Team beitreten</Button>
        </Paper>
      ))}
    </Grid>
);
}
 
export default TurnierDetails;