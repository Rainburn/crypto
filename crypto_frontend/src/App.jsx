import React, {useState} from "react";
import { createTheme, ThemeProvider, StylesProvider } from '@material-ui/core/styles';
import {
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  TextField,
  Container,
  Radio,
  RadioGroup,
  FormControlLabel,
  Box,
  Switch
} from '@material-ui/core';
import CssBaseline from "@material-ui/core/CssBaseline";
import GetAppIcon from '@material-ui/icons/GetApp';
import styles from './App.module.css';

function App() {
  const [method, setMethod] = useState('vigenere');
  const [crypt, setCrypt] = useState('Encrypt');
  const [is5, setis5] = useState(false);
  const [requestText, setRequestText] = useState('');
  const [keyText, setKeyText] = useState('')
  const [resultText, setResultText] = useState('haloyhaloyhaloyhaloy');
  
  
  const readTxtFile = async (e) => {
    e.preventDefault()
    const reader = new FileReader()
    reader.onload = async (e) => { 
      const text = (e.target.result)
      setRequestText(text);
    };
    reader.readAsText(e.target.files[0])
  }
  const downloadTxtFile = () => {
    const element = document.createElement("a");
    const file = new Blob([resultText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "cryptography.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }

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
  
  const handleSubmit = (event) => {
    event.preventDefault();
    downloadTxtFile();
    
  }
  
  const onRequestChange = (event) => {
    setRequestText(event.target.value);
    console.log('halo');
  }
  
  const onKeyChange = (event) => {
    setKeyText(event.target.value);
  }
  
  const onSwitchChange = (event) => {
    setis5(!is5);
    if(resultText==null){
      return;
    }
    let a = resultText;
    a =  is5 ? a.replace(/ /g,'') : a.split(/(.{5})/).filter(O=>O).join(" ");
    setResultText(a);
  }
  
  const onMethodChange = (event) => {
    setMethod(event.target.value);
  }

  const onCryptChange = (event) => {
    setCrypt(event.target.value);
  }
  return (
    <ThemeProvider theme={darkTheme}>
      <StylesProvider injectFirst>
        <CssBaseline />
    
      <AppBar className={styles.appBar} position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
          </IconButton>
          <Typography variant="h6">
            Kriptografi
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md">
        <form noValidate autoComplete="off" onSubmit={handleSubmit}>
          
          <TextField 
            required 
            multiline
            id="text" 
            label="Plain/Cipher Text"
            fullWidth 
            disabled={requestText!==''}
          />
          <input type="file" onChange={(e) => readTxtFile(e)} />
          <TextField required id="key" label="Key" fullWidth multiline />
          <FormControlLabel
            control={<Switch
              checked={is5}
              onChange={onSwitchChange}
              name="is5"
              color="primary"
            />}
            label="5 chunks"
          />
          
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <Typography id="result" variant="h5" gutterBottom gutterTop>
                    {resultText}
                </Typography>
              </Box>
              <Box p={1}>
              <IconButton aria-label="download" onClick={downloadTxtFile}>
                <GetAppIcon />
              </IconButton>
              </Box>
              
            </Box>
           
            <Box display="flex" flexDirection="row" p={2} m={4} bgcolor="background.paper">
              <Box p={1} flexGrow={1}>
                <Typography variant="h5" gutterBottom gutterTop>
                  Cipher Method
                </Typography>
                <RadioGroup aria-label="method" name="Method" value={method} onChange={(event)=> setMethod(event.target.value)}>
                  <FormControlLabel value="vigenere" control={<Radio />} label="Vigenere Standard" />
                  <FormControlLabel value="full_vigenere" control={<Radio />} label="Full Vigenere" />
                  <FormControlLabel value="autokey_vigenere" control={<Radio />} label="Auto Key Vigenere" />
                  <FormControlLabel value="extended_vigenere" control={<Radio />} label="Extended Vigenere" />
                  <FormControlLabel value="playfair" control={<Radio />} label="Playfair" />
                  <FormControlLabel value="affine" control={<Radio />} label="Affine" />
                </RadioGroup>
              </Box>
              <Box p={1} flexGrow={1}>
                <Typography variant="h5" gutterBottom gutterTop>
                   Encrypt/Decrypt
                </Typography>
                <RadioGroup aria-label="crypt" name="Cryption" value={crypt} onChange={(event)=>  setCrypt(event.target.value)}>
                  <FormControlLabel value="Encrypt" control={<Radio />} label="Encrypt" />
                  <FormControlLabel value="Decrypt" control={<Radio />} label="Decrypt" />
                </RadioGroup>
                <Button type="submit" className={styles.button}>{crypt}</Button>
              </Box>
              
            </Box>
        </form>
      </Container>
      </StylesProvider>
    </ThemeProvider>
  );
}

export default App;
