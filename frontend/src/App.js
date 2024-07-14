import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { useEffect } from 'react';
import theme from './theme.js';
import Turnier from './pages/Turnier.js';

function App() {

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          <Route path={'/'} element={<Turnier/>}/>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
