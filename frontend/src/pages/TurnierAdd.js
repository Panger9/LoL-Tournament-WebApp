import { Box, Typography, Button, TextField, FormControl, MenuItem, InputLabel, Select } from '@mui/material';
import { useEffect, useState, useContext } from 'react';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format } from 'date-fns';
import { de, it } from 'date-fns/locale';
import { UserContext } from '../App';
import enGB from 'date-fns/esm/locale/en-GB/index';
import { deDE } from '@mui/x-date-pickers/locales';
import deAT from 'date-fns/locale/de-AT';
import { useNavigate } from 'react-router-dom';

const TurnierAdd = () => {
  const user = useContext(UserContext);

  const [turnierGröße, setTurniergröße] = useState('');
  const [turnierName, setTurnierName] = useState('');
  const [turnierOwner, setTurnierOwner] = useState(0);
  const [turnierStartdate, setTurnierStartdate] = useState(null);

  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  const Navigate = useNavigate()

  const handleSubmit = async (e) => {

    setLoading(true)
    setError(false)
    e.preventDefault();

    const formattedDate = turnierStartdate ? format(turnierStartdate, 'dd.MM.yyyy/HH:mm', { locale: de }) : null;
    const turnierData = {
      id: 0,
      name: turnierName,
      team_size: turnierGröße,
      turnier_owner: user.user_id,
      start_date: formattedDate,
    };

    const res = await fetch(`/lolturnier/turnier`, {
      method:"POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(turnierData)
    })
    if (!res.ok){
      setError('Turnier-Erstellung fehlerhaft. Bitte überprüfe, ob alle Eingaben inklusive Datum vorhanden sind!')
      setLoading(false)
        }
    else {
      setLoading(false)
      Navigate('/turniere')
    }

    // Hier kannst du die API-Aufruf-Funktion hinzufügen
  };

  return (
    <Box>
      <form onSubmit={handleSubmit} style={{display:"flex", flexDirection:"column", gap:"15px"}}>
        <TextField
          required
          label="Turniername"
          type="text"
          value={turnierName}
          onChange={(e) => setTurnierName(e.target.value)}
        />
        <FormControl fullWidth required>
          <InputLabel id="demo-simple-select-label">Turniergröße</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={turnierGröße}
            label="Turniergröße"
            onChange={(e) => setTurniergröße(e.target.value)}
          >
            <MenuItem value={4}>4 Teams</MenuItem>
            <MenuItem value={8}>8 Teams</MenuItem>
            <MenuItem value={16}>16 Teams</MenuItem>
            <MenuItem value={32}>32 Teams</MenuItem>
            <MenuItem value={64}>64 Teams</MenuItem>
          </Select>
        </FormControl>
        <LocalizationProvider dateAdapter={AdapterDateFns} locale={deDE} required>
          <DateTimePicker
            required
            label="Turnier Startdatum und -zeit"
            value={turnierStartdate}
            onChange={(newValue) => setTurnierStartdate(newValue)}
            ampm={false} // Hier wird das 24-Stunden-Format aktiviert
            inputFormat="dd.MM.yyyy HH:mm"
            mask="__.__.____ __:__"
            slotProps={{ textField: (params) => <TextField {...params} required /> }}
          />
        </LocalizationProvider>
        {error && <Typography color='error'>{error}</Typography>}
        <Button type="submit" variant='contained' disabled={!user.signedIn}>{loading ? 'lädt...' : 'Submit'}</Button>
      </form>
    </Box>
  );
};

export default TurnierAdd;