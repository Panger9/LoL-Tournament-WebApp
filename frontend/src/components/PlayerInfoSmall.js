import React, { useContext, useState } from 'react';
import { Box, Typography, Menu, MenuItem } from '@mui/material';
import Suppicon from '../images/Suppicon.png';
import Adcicon from '../images/ADC icon.png';
import Jglicon from '../images/JUngle icon.png';
import Midicon from '../images/Mid Icon.png';
import Topicon from '../images/Topicon.png';
import Fillicon from '../images/icon-position-unselected.png'
import { UserContext } from '../App';

const roleIcons = {
  top: Topicon,
  jgl: Jglicon,
  mid: Midicon,
  adc: Adcicon,
  sup: Suppicon,
  fill: Fillicon
};

const PlayerinfoSmall = ({ name, tag, level, tier, rank, profileIconId, role, team_id }) => {

  const user = useContext(UserContext)

  const [anchorEl, setAnchorEl] = useState(null);
  const [currentRole, setCurrentRole] = useState(role);
  const correctIcon = roleIcons[currentRole] || '';

  const handleClick = (event) => {
    if(user.sumName === name && user.tagLine === tag){
      setAnchorEl(event.currentTarget);
    }
    
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleRoleChange = async (newRole) => {
    setCurrentRole(newRole);
    await fetch(`/lolturnier/user-team`, {
      method:"PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({user_id: user.user_id, team_id: team_id, role: newRole })
    })
    handleClose();

  };


  return (
    <Box sx={{ display: "flex", flexDirection: "row", gap: "15px", alignContent: "center", backgroundColor: "rgb(0,0,0,0.4)", padding: "10px 25px 10px 15px", borderRadius: "20px", maxWidth: "fit-content" }}>
      <Box sx={{ position: "relative" }}>
        <Box
          component="img"
          sx={{
            height: "32px",
            borderRadius: "13px",
          }}
          alt="Profile Pic"
          src={`https://ddragon.leagueoflegends.com/cdn/14.14.1/img/profileicon/${profileIconId}.png`}
        />
        <Typography sx={{ fontSize: "11px", position: "absolute", bottom: "0px", left: "1px", backgroundColor: "rgba(0,0,0,0.4)", padding: "0px 5px", borderRadius: "10px" }} color="textSecondary" variant="body2">{level}</Typography>
      </Box>
      <Box sx={{ display: "flex", flexDirection: "row", width: "500px", alignItems: "center", gap: "10px", justifyContent: "space-between" }}>
        <a
          href={`https://www.op.gg/summoners/euw/${name}-${tag}`}
          target="_blank"
          rel="noopener noreferrer"
          style={{ textDecoration: 'none', color: 'inherit' }}
        >
          <Typography sx={{ ':hover': { color: "rgba(215,215,255,0.7)" } }}>{name}</Typography>
        </a>
        <Typography color="textSecondary" variant="body2">{tier ? tier + ' ' + rank : 'UNRANKED'}</Typography>
        <Box >
          <Box
            component="img"
            sx={{
              height: "24px",
              
              borderRadius: "2px",
              cursor: user.sumName === name && user.tagLine === tag ? "pointer" : "default",
              ":hover":{
                scale: user.sumName === name && user.tagLine === tag ? "1.10" : ""
              },
              transition:"0.2s"
            }}
            src={correctIcon}
            onClick={handleClick}
          />
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            
          >
            {Object.keys(roleIcons).map((roleKey) => (
              <MenuItem key={roleKey} variant="body2" onClick={() => handleRoleChange(roleKey)}>
                <Box
                  component="img"
                  sx={{
                    height: "24px",
                    borderRadius: "13px",
                    marginRight: "10px"
                  }}
                  src={roleIcons[roleKey]}
                />
                <Typography variant="body2">{roleKey}</Typography>
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Box>
    </Box>
  );
}

export default PlayerinfoSmall;