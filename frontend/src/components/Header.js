import {Box, Typography, AppBar, Button, SvgIcon} from '@mui/material'
import Playerinfo from './PlayerInfo';
import { useLocation, Link, Navigate, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../App';
import ReigsterDialog from './RegisterDialog'
import CustomDialog from './CustomDialog';
import CachedIcon from '@mui/icons-material/Cached';

const Header = () => {

  const location = useLocation();
  const {user, setUser} = useContext(UserContext)
  const Navigate = useNavigate()

  const [openDialog, setOpenDialog] = useState(false)

  const tabs = [
    { label: 'Browse', path: '/turniere'},
    { label: 'Meine Turniere', path: '/my-tournaments' },
    { label: 'Erstellen', path: '/create'},

  ];

  const handleDisconnectAccount = async () => {

    const res = await fetch(`/lolturnier/user-by-id/${user.user_id}`, {
      method: "DELETE"
    })
    localStorage.removeItem('tournament_token')
    Navigate('/turniere')
    window.location.reload()

  }

  const handleRefresh = async () => {
    const res = await fetch(`/lolturnier/user-refresh/${user.user_id}`)
    const data  = await res.json()

    setUser((prevState) => ({
      ...prevState,
      user_id: data.id,
      puuid: data.puuid,
      sumName: data.gameName,
      tagLine: data.tagLine,
      tier: data.tier,
      rank: data.rank,
      level: data.summonerLevel,
      profileIconId: data.profileIconId,
      signedIn: true,
      token: data.token
    }))
  }

  return (

    <Box>
      <AppBar sx={{display:"flex", flexDirection:"row", padding:"10px", justifyContent:"space-between"}}>
        <Box sx={{display:"flex", gap:"10px"}}>
      {tabs.map(tab => (
        <Button
          key={tab.path}
          component={Link}
          to={tab.path}
          sx={{
            textTransform: 'none',
            color:"primary.contrastText",
            backgroundColor: location.pathname.startsWith(tab.path) ? 'rgba(255,255,255,0.2)' : 'transparent',
            
            ':hover': { backgroundColor: 'rgba(255,255,255,0.1)'}
          }}
        >
          {tab.label}
        </Button>
      ))}
      </Box>

      <Box sx={{display:"flex", gap:"10px"}}>
        <Button variant='contained' onClick={() => handleRefresh(user.user_id)} ><SvgIcon component={CachedIcon}></SvgIcon></Button>
        {user.signedIn ? 
        <Button variant='contained' onClick={() => {setOpenDialog(true)}}>Verbindung trennen</Button>
        : 
        <Link to='/register'>
          <Button variant='contained'>Registrieren</Button>
        </Link>

        }
        {user.sumName ? <Box sx={{width:"300px"}}><Playerinfo name={user.sumName} tag={user.tagLine} tier={user.tier} level={user.level} profileIconId={user.profileIconId}></Playerinfo></Box> : ''}
      </Box>
      </AppBar>

      <CustomDialog
        open={openDialog}
        message="ACHTUNG: Damit werden sämtliche Einträge aus Teams und Turnieren gelöscht"
        title="Verbindung trennen"
        handleAccept={handleDisconnectAccount}
        handleClose={() => setOpenDialog(false)}
        type="NoInfo"
      />
      
    </Box>

    );

}
 
export default Header;