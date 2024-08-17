import { Box, Typography, AppBar, Button, SvgIcon } from '@mui/material'
import Playerinfo from './PlayerInfo';
import { useLocation, Link, Navigate, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../App';
import ReigsterDialog from './RegisterDialog'
import CustomDialog from './CustomDialog';
import CachedIcon from '@mui/icons-material/Cached';
import PlayerinfoSmall from './PlayerInfoSmall';
import LogoutIcon from '@mui/icons-material/Logout';

const Header = () => {

  const location = useLocation();
  const { user, setUser } = useContext(UserContext)
  const Navigate = useNavigate()

  const [openDialog, setOpenDialog] = useState(false)
  const [loadingRefresh, setLoadingRefresh] = useState(false)

  const tabs = [
    { label: 'Browse', path: '/turniere' },
    { label: 'Meine Turniere', path: '/my-tournaments' },
    { label: 'Erstellen', path: '/create' },

  ];

  const handleDisconnectAccount = async () => {

    const res = await fetch(`/lolturnier/user-by-id/${user.user_id}`, {
      method: "DELETE"
    })
    localStorage.removeItem('tournament_token')
    Navigate('/turniere/')
    window.location.reload()

  }

  const handleRefresh = async () => {
    setLoadingRefresh(true)
    const res = await fetch(`/lolturnier/user-refresh/${user.user_id}`)
    const data = await res.json()

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
    setLoadingRefresh(false)
  }

  const buttonStyle = {
    textTransform: 'none',
    color: "primary.contrastText",
    borderRadius: "6px",
    padding: "2px",
    minWidth: "auto",
    width: "24px",
    height: "24px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  };

  return (

    <Box>
      <AppBar sx={{ display: "flex", flexDirection: "row", padding: "10px", justifyContent: "space-between", alignItems: "center" }}>
        <Box sx={{ display: "flex", gap: "20px", marginLeft: "20px" }}>
          {tabs.map(tab => (
            <Button
              key={tab.path}
              component={Link}
              to={tab.path}
              variant=''
              sx={{
                textTransform: 'none',
                color: "primary.contrastText",
                backgroundColor: location.pathname.startsWith(tab.path) ? 'rgba(255,255,255,0.2)' : 'transparent',
                padding: "20px 20px",
                height: "40px",
                borderRadius: "12px",
                fontSize: "18px",
                ':hover': { backgroundColor: 'rgba(255,255,255,0.1)' }
              }}
            >
              {tab.label}
            </Button>
          ))}
        </Box>

        <Box sx={{ display: "flex", gap: "10px", height: "fit-content", alignItems: "center" }}>

          {user.signedIn ?
            <Box sx={{ display: "flex", flexDirection: "row", height:"auto", gap:"10px"  }}>


              <Box sx={{display:"flex", flexDirection:"column", justifyContent:"space-evenly", flex:1}}>
                <Button sx={buttonStyle} variant='contained' onClick={() => handleRefresh(user.user_id)} ><SvgIcon sx={{ height: "28px", padding: "4px", animation: loadingRefresh ? "spin 2s linear infinite" : "none" }} component={CachedIcon}></SvgIcon></Button>
                <Button sx={buttonStyle} variant='contained' color='error' onClick={() => { setOpenDialog(true) }}><SvgIcon sx={{ height: "28px", padding: "4px" }} component={LogoutIcon}></SvgIcon></Button>
              </Box>


              {user.sumName ? <Box sx={{ maxWidth: "350px" }} ><Playerinfo name={user.sumName} tag={user.tagLine} tier={user.tier} level={user.level} profileIconId={user.profileIconId}></Playerinfo></Box> : ''}
            </Box> :

            <Link to='/register'>
              <Button sx={{
                padding: "20px 20px",
                height: "40px",
                borderRadius: "12px",
                fontSize: "14px",
                marginRight: "20px"
                }} 
                
                variant='contained' >
                Sign in
              </Button>
            </Link>

          }

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