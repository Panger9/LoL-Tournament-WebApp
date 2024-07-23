import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { useEffect } from 'react';
import theme from './theme.js';
import Turnier from './pages/Turnier.js';
import Header from './components/Header.js'
import TurnierDetails from './pages/TurnierDetails.js';
import TurnierAdd from './pages/TurnierAdd.js';


function App() {



  return (
    <ThemeProvider theme={theme}>
      <Header></Header>
      <Router>
        <Routes>
          <Route path={'/'} element={<Turnier/>}/>
          <Route path={'/create'} element={<TurnierAdd/>}/>
          <Route path={'/:TurnierId'} element={<TurnierDetails/>}/>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
