import { createTheme } from "@mui/material";

const theme = createTheme({
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
        background: {
            default: '#121212', // Stilvolleres, tiefes Schwarz für moderne Web-Apps
            paper: '#000000', // Schwarz auch für Elemente, die auf dem Hintergrund hervorstechen sollen
        },
        text: {
            primary: "#ffffff", // Weißer Text für den Hauptinhalt
            secondary: "#d1d1d1", // Helles Grau für sekundären Text, bietet einen sanften Kontrast
        },
    },
    breakpoints: {
        values: {
            xs: 0,
            sm: 600,
            md: 960,
            lg: 1280,
            xl: 1920,
        },
    },
});

export default theme;