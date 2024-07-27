import {Box, Typography, AppBar, Button} from '@mui/material'
import Playerinfo from './PlayerInfo';
import { useLocation, Link } from 'react-router-dom';

const Header = () => {

  const location = useLocation();

  const tabs = [
    { label: 'Browse', path: '/turniere'},
    { label: 'Erstellen', path: '/create'},
    { label: 'Meine Turniere', path: '/MeineTurniere' },
  ];


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

      <Playerinfo name='Sir Panger' tag="EUW" tier="diamond 1" level="442"></Playerinfo>
      </AppBar>
      
    </Box>

    );

}
 
export default Header;