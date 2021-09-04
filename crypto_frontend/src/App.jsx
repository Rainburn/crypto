import React from "react";
import { createTheme, ThemeProvider, StylesProvider } from '@material-ui/core/styles';
import {
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  TextField,
  Container,
  Icon,
} from '@material-ui/core';
import CssBaseline from "@material-ui/core/CssBaseline";
import LockOpenIcon from '@material-ui/icons/LockOpen';
import styles from './App.module.css';


function App() {

  const baseTheme = createTheme({
    typography: {
      fontFamily: "'Work Sans', sans-serif",
      fontSize: 14,
      fontFamilySecondary: "'Roboto Condensed', sans-serif"
    }
  })
  
  const darkTheme = createTheme({
    ...baseTheme,
    palette: {
      type: "dark",
      primary: {
        main: "#5ab8c0"
      },
      secondary: {
        main: "#310d3a"
      }
    }
  })
  
  return (
    <ThemeProvider theme={darkTheme}>
      <StylesProvider injectFirst>
        <CssBaseline />
    
      <AppBar className={styles.appBar} position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
          </IconButton>
          <Typography variant="h6" ß>
            Kriptografi
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md">
        <Icon edge="end" color="inherit" aria-label="menu" size="medium">
            <LockOpenIcon/>
          </Icon>
        <form noValidate autoComplete="off">
        <TextField required id="text" label="Plain/Cipher Text" fullWidth />
        <TextField required id="key" label="Key" fullWidth />
        <Button className={styles.button}>Encrypt</Button>
        </form>
      </Container>
      </StylesProvider>
    </ThemeProvider>
  );
}

export default App;
