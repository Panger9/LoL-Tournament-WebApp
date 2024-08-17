import {Box, Typography, Button, Dialog, Grid, Paper, Card, Snackbar} from '@mui/material'
import { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext } from '../App';
import PlayerinfoSmall from '../components/PlayerInfoSmall';
import LinearProgress from '@mui/material/LinearProgress';
import { useGet } from '../components/useFetch';

const TurnierDetails = () => {

  let { TurnierId } = useParams();
  const {user} = useContext(UserContext)

  const [reload, setReload] = useState(false)
  const [open, setOpen] = useState(false);
  const {data: turnier, isPending, error} = useGet(`/lolturnier/user-by-team-and-turnier/${TurnierId}`, [reload] )
  

  const joinTeam = async (user_id, team_id, turnier_id) => {
    const res = await fetch(`/lolturnier/user-team-turnier/${user_id}/${team_id}/${turnier_id}`,{
      method:"POST",
    })
    setReload(!reload)
    
  }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

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
        if(turnier[teamIndex][i].puuid === user.puuid){
          isInTeam = true
        }
      } else {
        console.log('Team oder Spielerinformationen sind nicht verfügbar.');
      }
    }
    return isInTeam
  }

  async function copyToClip() {
    let url = window.location.href
    await navigator.clipboard.writeText(url);
    setOpen(true)
  } 

  return ( 
    <>
    {isPending && <LinearProgress></LinearProgress>}
    {error && <Typography color="error" >{error}</Typography>}
    

    {turnier && 
    <Box sx={{display:"flex", marginBottom:"20px"}}>
      <Button variant='contained' onClick={copyToClip}>Invite Link</Button>
      <Snackbar
        open={open}
        autoHideDuration={3000}
        onClose={handleClose}
        message="Link erfolgreich kopiert"
      />
    </Box>
    }
    


    <Grid container spacing={3}  >
    
      {(turnier && user) && turnier.map((team, teamIndex) => (
        <Grid item xs={12} sm={6} lg={3} xl={1.5} key={teamIndex} >
          <Box sx={{backgroundColor:"#171717", borderRadius:"18px", display:"flex", flexDirection:"column", padding:"20px"}}>
          <Typography variant='h5'>Team {teamIndex + 1} ({team[0].mean_rank} )</Typography>
          <Box sx={{display:"flex", flexDirection:"column", gap:"7px", margin:"20px 0px", width:"100%"}}>
          {team.slice(1).map((user, userIndex) => (
          <>
          <PlayerinfoSmall name={user.gameName} tag={user.tagLine} tier={user.tier} level={user.summonerLevel} profileIconId={user.profileIconId} rank={user.rank} role={user.role} team_id={team[0].team_id}></PlayerinfoSmall>
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
    </>
);
}
 
export default TurnierDetails;