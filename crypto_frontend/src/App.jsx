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
} from '@material-ui/core';

import CssBaseline from "@material-ui/core/CssBaseline";
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Tugas1 from './Tugas1';
import { Link as RouterLink, MemoryRouter as Router2 } from 'react-router-dom';

import Router from "./Router";
// import MailIcon from '@material-ui/icons/MailIcon';
// import InboxIcon from '@material-ui/icons/InboxIcon';
import styles from './App.module.css';
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import firebase from "firebase";

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
    <ThemeProvider theme={darkTheme}>
      <StylesProvider injectFirst>
        <CssBaseline />
      <Router/>
      </StylesProvider>
    </ThemeProvider>
  );
}

export default App;
