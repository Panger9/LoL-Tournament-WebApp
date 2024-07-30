import {Box, Typography, Button, Dialog, Grid, Paper} from '@mui/material'
import { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import Playerinfo from '../components/PlayerInfo'
import { UserContext } from '../App';

const TurnierDetails = () => {

  let { TurnierId } = useParams();

  const [turnier, setTurnier] = useState('')
  const [isPending, setIsPending] = useState(false)
  const [reload, setReload] = useState(false)

  const user = useContext(UserContext)

  useEffect (() => {

    const fetchTurnier = async () => {
      const res = await fetch(`/lolturnier/user-by-team-and-turnier/${TurnierId}`)
      const data = await res.json()
      setTurnier(data)
    }

    fetchTurnier()

  },[reload])

  const joinTeam = async (user_id, team_id, turnier_id) => {
    const res = await fetch(`/lolturnier/user-team-turnier/${user_id}/${team_id}/${turnier_id}`,{
      method:"POST",
    })
    setReload(!reload)
  }

  return ( 
    <Grid container  spacing={2} gap={5}>
      {isPending && 'Daten werden geladen'}
      {turnier && turnier.map((team, teamIndex) => (
        <Paper item key={teamIndex} sx={{padding:"20px 50px", backgroundColor:"#141414", display:"flex", flexDirection:"column", gap:"15px", borderRadius:"18px"}}>
          Team {teamIndex + 1}
          {team.slice(1).map((user, userIndex) => (
            <Box key={userIndex}>
              <Playerinfo name={user.gameName} tag={user.tagLine} tier={user.tier} level={user.summonerLevel} profileIconId={user.profileIconId}></Playerinfo>
            </Box>
          ))}
 
          <Button onClick={() => joinTeam(user.user_id, team[0].team_id, TurnierId )} variant='contained' sx={{boxShadow:"none", ':hover':{boxShadow:"none"}, ':focus':{boxShadow:"none"}}}>Team beitreten</Button>
        </Paper>
      ))}
    </Grid>
);
}
 
export default TurnierDetails;