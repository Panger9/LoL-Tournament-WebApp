import {Box, Typography, Button, Dialog, Grid, Paper, Card} from '@mui/material'
import { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext } from '../App';
import PlayerinfoSmall from '../components/PlayerInfoSmall';

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

  const leaveTeam = async (User_id, Team_id, Turnier_id) => {
    const res = await fetch(`/lolturnier/user-team-turnier/${User_id}/${Team_id}/${Turnier_id}`, {
      method:"DELETE"
    })
    setReload(!reload)

  }
  const isInTeam = (teamIndex) => {

    let isInTeam = false
    for(let i = 1; i < 7; i++){
      if (turnier[teamIndex] && turnier[teamIndex][i]) {
        if(turnier[teamIndex][i].gameName === user.sumName){
          isInTeam = true
        }
      } else {
        console.log('Team oder Spielerinformationen sind nicht verfügbar.');
      }
    }
    return isInTeam
  }

  return ( 
    <Grid container spacing={3}  >
      {isPending && 'Daten werden geladen'}
      {(turnier && user) && turnier.map((team, teamIndex) => (
        <Grid item xs={12} sm={6} lg={3} key={teamIndex} >
          <Box sx={{backgroundColor:"#171717", borderRadius:"18px", display:"flex", flexDirection:"column", padding:"20px"}}>
          <Typography variant='h5'>Team {teamIndex + 1} ({team[0].mean_rank} )</Typography>
          <Box sx={{display:"flex", flexDirection:"column", gap:"7px", margin:"20px 0px"}}>
          {team.slice(1).map((user, userIndex) => (
          <>
          <PlayerinfoSmall name={user.gameName} tag={user.tagLine} tier={user.tier} level={user.summonerLevel} profileIconId={user.profileIconId} rank={user.rank} role={user.role}></PlayerinfoSmall>
          </>
          ))}
          
          </Box>
          
          <Box sx={{display:"flex", gap:"10px", justifyContent:"center"}}>
          <Button onClick={() => joinTeam(user.user_id, team[0].team_id, TurnierId )} variant='contained' disabled={!user.signedIn}
          sx={{ borderRadius:"12px" ,width:"40%", boxShadow:"none", ':hover':{boxShadow:"none"}, ':focus':{boxShadow:"none"}}}>
            join
          </Button>

          <Button onClick={() => leaveTeam(user.user_id, team[0].team_id, TurnierId )} variant='contained' color='error' disabled={!isInTeam(teamIndex)}
          sx={{ borderRadius:"12px" ,width:"40%", boxShadow:"none", ':hover':{boxShadow:"none"}, ':focus':{boxShadow:"none"}}}>
            leave
          </Button>

          </Box>

          </Box>
        </Grid>
      ))}
    </Grid>
);
}
 
export default TurnierDetails;