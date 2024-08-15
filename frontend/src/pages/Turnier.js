import { Box, Typography, Button } from '@mui/material';
import TurnierListe from '../components/TurnierListe';
import { useGet } from '../components/useFetch';
import LinearProgress from '@mui/material/LinearProgress';

const Turnier = () => {


  const { data, isPending, error } = useGet(`/lolturnier/turnier-with-slots`)
  

  return (

    <Box>
      {isPending && <LinearProgress />}
      {error && <Typography color="error" >{error}</Typography>}
    
      {data ? data.length < 1 ? 'Es existieren noch keine Turniere' : <TurnierListe liste={data}></TurnierListe> : ''}

    </Box>

  );
}

export default Turnier;