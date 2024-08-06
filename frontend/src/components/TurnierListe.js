import { Box, Card, CardContent, Typography, Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import GroupsIcon from '@mui/icons-material/Groups';

const TurnierListe = ({ liste }) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ bgcolor: "#121212", color: "#fff", padding: 2 }}>
      <Grid container spacing={2}>
        {liste && liste.map((e) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={e.id}>
            <Card
              sx={{
                bgcolor: "#1e1e1e",
                color: "#fff",
                borderRadius: 2,
                boxShadow: 3,
                position: "relative",
                overflow: "hidden",
                '&:hover': {
                  boxShadow: 6,
                },
                cursor: "pointer",
                '&:before': {
                  content: '""',
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background: "rgba(255, 255, 255, 0.1)",
                  opacity: 0,
                  transition: "opacity 0.3s",
                },
                '&:hover:before': {
                  opacity: 1,
                }
              }}
              onClick={() => navigate(`/turniere/${e.id}`)}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {e.name}
                </Typography>
                <Grid container spacing={1} alignItems="center">
                  <Grid item>
                    <SportsEsportsIcon />
                  </Grid>
                  <Grid item>
                    <Typography variant="body2">
                      Teams: {e.team_size}
                    </Typography>
                  </Grid>
                </Grid>
                <Grid container spacing={1} alignItems="center" mt={1}>
                  <Grid item>
                    <PersonIcon />
                  </Grid>
                  <Grid item>
                    <Typography variant="body2">
                      Owner: {e.turnier_owner}
                    </Typography>
                  </Grid>
                </Grid>
                <Grid container spacing={1} alignItems="center" mt={1}>
                  <Grid item>
                    <GroupsIcon />
                  </Grid>
                  <Grid item>
                    <Typography variant="body2">
                      Slots: {e.slots}
                    </Typography>
                  </Grid>
                </Grid>
                <Grid container spacing={1} alignItems="center" mt={1}>
                  <Grid item>
                    <EventAvailableIcon />
                  </Grid>
                  <Grid item>
                    <Typography variant="body2">
                      {new Date(e.start_date).toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default TurnierListe;
