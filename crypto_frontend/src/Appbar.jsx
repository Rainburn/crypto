import React, {} from "react";
import { createTheme, ThemeProvider, StylesProvider } from '@material-ui/core/styles';
import {
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  Drawer,
  Divider,
  List,
  ListItem,
  ListItemText,
  Link,
  Button,
} from '@material-ui/core';

import CssBaseline from "@material-ui/core/CssBaseline";
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Tugas1 from './Tugas1';
import { Link as RouterLink, MemoryRouter as Router } from 'react-router-dom';


// import MailIcon from '@material-ui/icons/MailIcon';
// import InboxIcon from '@material-ui/icons/InboxIcon';
import styles from './App.module.css';

const LinkBehavior = React.forwardRef((props, ref) => (
  <RouterLink ref={ref} to="/tugas1" {...props} />
));

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
        main: "#5ab8c0"
      }
    }
  })

  return (
<>
      <AppBar className={styles.appBar} position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
          </IconButton>
          <Typography variant="h6">
            Kriptografi
          </Typography>
          
          <Link to="/tugas1">
            <Button>
                Tugas 1 + Rc4
            </Button>
          </Link>
          <Link to="/steganography">
            <Button>
                Steganography
            </Button>
          </Link>
        </Toolbar>
      </AppBar>
</>
  );
}

export default App;
