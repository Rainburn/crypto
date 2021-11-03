import React, {} from "react";
import { createTheme, ThemeProvider, StylesProvider } from '@material-ui/core/styles';

import CssBaseline from "@material-ui/core/CssBaseline";

import Router from "./Router";
// import MailIcon from '@material-ui/icons/MailIcon';
// import InboxIcon from '@material-ui/icons/InboxIcon';


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
