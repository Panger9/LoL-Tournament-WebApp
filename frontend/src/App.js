import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { useEffect, useState } from 'react';
import theme from './theme.js';
import Turnier from './pages/Turnier.js';
import Header from './components/Header.js'
import TurnierDetails from './pages/TurnierDetails.js';
import TurnierAdd from './pages/TurnierAdd.js';
import MeineTurniere from './pages/MeineTurniere.js';
import { Box } from '@mui/material';
import { createContext } from 'react';
import RegisterDialog from './components/RegisterDialog.js';

export const UserContext = createContext();

function App() {

  const [user, setUser] = useState({
    signedIn: null,
    user_id: '',
    sumName: '',
    tagLine: '',
    tier: '',
    level: '',
    profileIconId: '',
    token: ''
  })


  useEffect(() => {

    const autoLogin = async () => {

      const token = localStorage.getItem('tournament_token')
      const res = await fetch('/lolturnier/user-login/' + token)

      if (!res.ok){
        console.log('Kein user erkannt')
      }
      else {
        const data = await res.json()
        console.log(data)
        setUser((prevState) => ({
          ...prevState,
          user_id: data.user_id,
          sumName: data.gameName,
          tagLine: data.tagLine,
          tier: data.tier,
          rank: data.rank,
          level: data.summonerLevel,
          profileIconId: data.profileIconId,
          signedIn: true,
          token: token
        }))
      }
    }
    autoLogin()
  },[])




  return (
    <UserContext.Provider value={user}>
    <Router>
      <Box sx={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems:"center"
      }}>

        <Header sx={{}}></Header>

        <Box sx={{marginTop:"100px", width:"80%"}}>
          <Routes>
            <Route path={'/turniere'} element={<Turnier />} />
            <Route path={'/create'} element={<TurnierAdd />} />
            <Route path={'/turniere/:TurnierId'} element={<TurnierDetails />} />
            <Route path={'/my-tournaments'} element={<MeineTurniere />} />
            <Route path={'/register'} element={<RegisterDialog />} />
          </Routes>
        </Box>

      </Box>
    </Router>
    </UserContext.Provider>

  );
}

export default App;
