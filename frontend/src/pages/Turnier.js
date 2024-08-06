import { Box, Typography } from '@mui/material';
import TurnierListe from '../components/TurnierListe';
import { useGet } from '../components/useFetch';
import LinearProgress from '@mui/material/LinearProgress';

const Turnier = () => {


  const { data, isPending, error } = useGet(`/lolturnier/turnier-with-slots`)


  return (

    <Box>
      {isPending && <LinearProgress />}
      {error && <Typography color="error" >{error}</Typography>}
      <TurnierListe liste={data}></TurnierListe>
    </Box>

  );
}

export default Turnier;