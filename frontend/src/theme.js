import { createTheme } from "@mui/material";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const theme = createTheme({
    components: {
        MuiSvgIcon: {
          styleOverrides: {
            root: {
              '@keyframes spin': {
                '0%': { transform: 'rotate(0deg)' },
                '100%': { transform: 'rotate(360deg)' },
              },
              '&.spin': {
                animation: 'spin 2s linear infinite',
              },
            },
          },
        },
      },
    palette: {
        mode: 'dark', // Setzt den Theme-Modus auf "dark"
        primary: {
            main: "#3a506b", // Ein tiefes Blau für primäre Aktionen
            contrastText: "#ffffff", // Weißer Text für Kontrast auf tiefem Blau
        },
        secondary: {
            main: "#b3404a", // Ein gedämpftes Rot für sekundäre Aktionen
            contrastText: "#ffffff", // Weißer Text für Kontrast auf gedämpftem Rot
        },
        error: {
            main: "#9e3c3c",
            secondary: "#e23e3e"
        },
        success: {
            main: "#498953"
        },
        background: {
            default: '#121212', // Stilvolleres, tiefes Schwarz für moderne Web-Apps
            paper: '#000000', // Schwarz auch für Elemente, die auf dem Hintergrund hervorstechen sollen
        },
        text: {
            primary: "#F8F8F8", // Weißer Text für den Hauptinhalt
            secondary: "rgba(255,255,255,0.65)", // Helles Grau für sekundären Text, bietet einen sanften Kontrast
        },
    },

    
    breakpoints: {
        values: {
            xs: 0,
            sm: 600,
            md: 960,
            lg: 1280,
            xl: 3220,
        },
    },
});

export default theme;