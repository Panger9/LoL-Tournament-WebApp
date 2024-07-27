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

export const Context = createContext();

function App() {

  const [signedIn, setSignedIn] = useState(null);
  const [sumName, setSumName] = useState('')
  const [tagLine, setTagline] = useState('')
  const [tier, setTier] = useState('')
  const [rank, setRank] = useState('')
  const [level, setLevel] = useState('')
  const [iconId, setIconId] = useState('')


  return (
    <Context.Provider value={[signedIn, setSignedIn, sumName, setSumName, tagLine, setTagline, tier, setTier,
      rank, setRank, level, setLevel, iconId, setIconId ]}>
    <Router>
      <Box sx={{
        cursor: "url(/frontend/src/images/cursor.png), auto",
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}>

        <Header sx={{}}></Header>

        <Box sx={{marginTop:"100px", width:"80%"}}>
          <Routes>
            <Route path={'/turniere'} element={<Turnier />} />
            <Route path={'/create'} element={<TurnierAdd />} />
            <Route path={'/turniere/:TurnierId'} element={<TurnierDetails />} />
            <Route path={'/my-tournaments'} element={<MeineTurniere />} />
          </Routes>
        </Box>

      </Box>
    </Router>
    </Context.Provider>

  );
}

export default App;
