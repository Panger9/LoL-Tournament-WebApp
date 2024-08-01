import {Box, Typography} from '@mui/material'
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TurnierListe from '../components/TurnierListe';

const Turnier = () => {


  const Navigate = useNavigate()
  const [turniere, setturniere] = useState([])

  useEffect(() => {
    fetch('/lolturnier/turnier-with-slots')
    .then((res) => res.json())
    .then((data) => {
      setturniere(data)
    })
  }, [])


  return ( 
    <TurnierListe liste={turniere}></TurnierListe>
   );
}
 
export default Turnier;