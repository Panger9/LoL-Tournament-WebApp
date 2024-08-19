import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button, Box, Input, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Playerinfo from './PlayerInfo';

function RegisterDialog() {

  const [phase1, setPhase1] = useState(true)
  const [phase2, setPhase2] = useState(false)
  const [phase3, setPhase3] = useState(false)

  const [error1, setError1] = useState(false);
  const [error2, setError2] = useState(false);
  const [error3, setError3] = useState(false);

  const [isPending, setIsPending] = useState(false)

  const [inputSumName, setInputSumName] = useState('')
  const [inputTagLine, setInputTagLine] = useState('')

  const [accountInfo, setAccountInfo] = useState({})

  const Navigate = useNavigate()

  const [wantedIconId, setWantedIconId] = useState(Math.floor(Math.random() * 8) + 1)

  const handleClose = () => {
    Navigate('/turniere')
  }

  const getPlayerInfo1 = async () => {

    setIsPending(true)
    setError1(false)
    const sanitizedTagLine = inputTagLine.replace(/^#/, ''); // Entferne das Hash-Symbol, falls vorhanden
    const res = await fetch(`/lolturnier/riot/get-playerinfo_important/${inputSumName}/${sanitizedTagLine}`)
    if (res.ok) {
      setPhase1(false)
      setPhase2(true)
      setIsPending(false)
      const data = await res.json()
      setAccountInfo(data)
      if(data.profileIconId === wantedIconId){
        setWantedIconId(wantedIconId + 1)
      }
      console.log(data)
    }
    else {
      setError1('Dein Account wurde nicht gefunden. Bitte Probiere es erneut.')
      setIsPending(false)
    }
  }

  const registerPlayer = async () => {

    setIsPending(true)
    setError2(false)

    const iconChangedRes = await fetch('/lolturnier/riot/has-icon-changed', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({oldIconId: accountInfo.profileIconId, wantedIconId: wantedIconId, puuid: accountInfo.puuid})
    })
    const iconChanged = await iconChangedRes.json()

    if (iconChanged) {
      try {

        //Überprüfen, ob die gegebene puuid bereits in der Datenbank existiert. Wenn nicht (404), dann wird ein neuer User angelegt. Falls doch, wird der token vom bestehenden user im Browser abgelegt
        const res1 = await fetch(`/lolturnier/user-by-puuid/${accountInfo.puuid}`)

        if (res1.status === 404) {

          let user = {
            id: 0, puuid: accountInfo.puuid, token: 'fill', gameName: accountInfo.gameName, tagLine: accountInfo.tagLine,
            profileIconId: accountInfo.profileIconId, summonerLevel: accountInfo.summonerLevel, tier: accountInfo.tier, rank: accountInfo.rank
          }

          const res = await fetch(`/lolturnier/user`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(user)
          })

          const data = await res.json()
          localStorage.removeItem('tournament_token')
          localStorage.setItem('tournament_token', data.token)
        }
        else {
          const data = await res1.json()
          localStorage.removeItem('tournament_token')
          localStorage.setItem('tournament_token', data.token)

        }
        setPhase2(false)
        setPhase3(true)

      }
      catch {
        setError2('Änderung des Icons erkannt. Anlegen des Users jedoch fehlgeschlagen')
      }
      finally {
        setIsPending(false)
      }
    }
    else {
      setError2('Keine Änderung des Icons erkannt.')
      setIsPending(false)
    }
  }

  return (
    <Dialog open={true} >
      <Box sx={{ padding: "10px" }}>
        <DialogTitle>Verknüpfe deinen League of Legends Account</DialogTitle>
        <DialogContent>
          {phase1 ?
            <Box sx={{ display: "flex", flexDirection: "column", gap: "15px" }}>
              <Typography>
                Schritt 1: Gib deinen Namen und deinen hashtag ein
              </Typography>
              {error1 &&
                <Typography variant='body2' color="error.secondary">
                  <b>{error1}</b>
                </Typography>
              }
              <TextField
                type='text'
                variant="filled"
                label="Summoner Name"
                value={inputSumName}
                onChange={(e) => setInputSumName(e.target.value)}
              />
              <TextField
                type='text'
                variant="filled"
                label="Tag Line"
                value={inputTagLine}
                onChange={(e) => setInputTagLine(e.target.value)}
              />
            </Box>


            : ''}
          {phase2 ?
            <Box sx={{ display: "flex", flexDirection: "column", gap: "15px" }}>

              <Typography>
                Dein Profil wurde gefunden!
              </Typography>
              <Playerinfo name={accountInfo.gameName} tag={accountInfo.tagLine} tier={accountInfo.tier ? accountInfo.tier : 'UNRANKED'} rank={accountInfo.rank ? accountInfo.rank : ''} level={accountInfo.summonerLevel} profileIconId={accountInfo.profileIconId}></Playerinfo>
              <Box sx={{display:"flex", flexDirection:"row", gap:"20px"}}>
              <Typography>
                Um zu beweisen, dass es auch wirklich dir gehört, <b>ändere nun dein Profilbild</b> zu dem Icon, das dir rechts angezeigt wird, und bestätige, sobald du dies getan hast.
                
              </Typography>
              <Box
                component="img"
                sx={{
                  height: "80px",
                  width:"80px",
                  borderRadius: "13px"
                }}
                alt="Profile Pic"
                src={`https://ddragon.leagueoflegends.com/cdn/14.14.1/img/profileicon/${wantedIconId}.png`}
              />
              </Box>
              {error2 &&
                <Typography color="error.secondary">
                  <b>{error2}</b>
                </Typography>
              }
            </Box>
            : ''}
          {phase3 ?
            <Typography>
              Account erfolgreich verknüpft!
            </Typography>
            : ''}

        </DialogContent>

        <DialogActions>
          {phase1 ?
            <>
              <Button disabled={isPending} variant='contained' onClick={handleClose} color="error">
                Abbrechen
              </Button>
              <Button disabled={isPending} variant='contained' onClick={getPlayerInfo1} color="success">
                Bestätigen
              </Button>
            </> : ''
          }
          {phase2 ?
            <>
              <Button disabled={isPending} variant='contained' onClick={handleClose} color="error">
                Abbrechen
              </Button>
              <Button disabled={isPending} variant='contained' onClick={registerPlayer} color="success">
                Verifizieren
              </Button>
            </> : ''
          }
          {phase3 ?
            <>
              <Button disabled={isPending} variant='contained' onClick={() => { setPhase3(false); Navigate('/turniere'); window.location.reload() }} color="success">
                Bestätigen
              </Button>
            </> : ''
          }
        </DialogActions>
      </Box>
    </Dialog>
  );
}

export default RegisterDialog;