import React, {useEffect, useState} from "react";
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
  Switch,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from '@material-ui/core';
import axios from "axios";
import CssBaseline from "@material-ui/core/CssBaseline";
import GetAppIcon from '@material-ui/icons/GetApp';
import FileCopyIcon from '@material-ui/icons/FileCopy';
import styles from './App.module.css';

function App() {
  const [method, setMethod] = useState('1');
  const [crypt, setCrypt] = useState('Encrypt');
  const [is5, setis5] = useState(false);
  const [requestText, setRequestText] = useState('');
  const [keyText, setKeyText] = useState('')
  const [resultText, setResultText] = useState('');
  const [mkeyText,setMKeyText] = useState(0);
  const [isShowMKey, setIsShowMKey] = useState(false);
  const [table,setTable] = useState();
  const [isShowDecrypt, setIsShowDecrypt] = useState(false);
  
  const copyToClipboard = (text) => {
    const el = document.createElement('textarea');
    el.value = text.replace(/ /g,'');
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
  }
  
  const downloadCsv = (rows) => {
    let csvContent = "data:text/csv;charset=utf-8," 
    + rows.map(e => e.join(",")).join("\n");
    
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "my_data.csv");
    document.body.appendChild(link); // Required for FF

    link.click();
  }
  
  const readCsvFile = (e) => {
    e.preventDefault()
    let csvStr;
    const reader = new FileReader()
    reader.onload = async (e) => { 
      const text = (e.target.result)
      csvStr = text;
      
      const array = []
      csvStr.split("\n").forEach((value)=>{
        const arr = value.split(",");
        array.push(arr)
      })
      
      setTable(array);
    };
    reader.readAsText(e.target.files[0])
    
    
  }
  
  const readTxtFile = async (e) => {
    e.preventDefault()
    const reader = new FileReader()
    reader.onload = async (e) => { 
      const text = (e.target.result)
      var s = document.getElementById("plain/ciphertext");
      s.value = text;
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
  
  const trimAlphabetic = (text) => {
    return text.replace(/[^A-Za-z]/g, '');
  }
  
  const handleSubmit = (event) => {
    event.preventDefault();
    
    let data;
    let text = document.getElementById("plain/ciphertext").value;
    
    
    // If method chosen is Vigenere Base 26 or Playfair
    if(method!='4' && method!='5'){
      text = trimAlphabetic(text);
    }
    
    data = {
      "data": {
        "action" : crypt.toLowerCase(),
        "algorithm": method,
        "text": text,
        "key": document.getElementById("key").value
      }
    };
    
    if(isShowDecrypt){
      data = {
        "data": {
          "action" : crypt.toLowerCase(),
          "algorithm": method,
          "text": text,
          "key": document.getElementById("key").value,
          "table": table,
        }
      };
    }
    
    if(isShowMKey){
      data = {
        "data": {
          "action" : crypt.toLowerCase(),
          "algorithm": method,
          "text": document.getElementById("plain/ciphertext").value,
          "m": mkeyText,
          "b": Number.parseInt(document.getElementById("key").value),
        }
      };
    }
    
    axios.post(`http://127.0.0.1:5000/result`, data)
      .then(res => {
        const result = crypt.toLowerCase() === 'encrypt' ? res.data.cipher: res.data.plain;
        setResultText(result.toUpperCase())
        
        if(res.data.table!=undefined){
          downloadCsv(res.data.table);
        }
      })
  }
  
  useEffect(()=>{
    if(crypt.toLowerCase()==='decrypt' && method==='2'){
      setIsShowDecrypt(true);
    }
    else{
      setIsShowDecrypt(false);
    }
  }, [crypt,method])
  
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
    const changeShowMKey = event.target.value == '6' ? true : false;
    setIsShowMKey(changeShowMKey);
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
      <div className={styles.container}>
        <Container  maxWidth="md">
          <form noValidate autoComplete="off" onSubmit={handleSubmit}>
            <Box display="flex" flexDirection="row" >
                <Box p={1} flexGrow={1}>
                  <TextField 
                    required 
                    id="plain/ciphertext"
                    label="Plain/Cipher Text" 
                    multiline
                    fullWidth 
                    focused
                    // value={requestText}
                    // onChange={(e)=> setRequestText(e.target.value)}
                  />
                </Box>
                <Box p={1}>
                  <IconButton aria-label="download" onClick={() => copyToClipboard(requestText)}>
                    <FileCopyIcon />
                  </IconButton>
                </Box>
            </Box>
            
            <label class={styles.upload}>
            <input class={styles.button} type="file" onChange={(e) => readTxtFile(e)} />
            Upload File
            </label>
            
              
            
            {isShowMKey && (
              <div>
              <FormControl className={styles.full}>
                <InputLabel id="m-key-label">M Key</InputLabel>
                  <Select
                    labelId="m-key-label"
                    id="m-key-select-lable"
                    value={mkeyText}
                    autoWidth
                    onChange={(event) => setMKeyText(event.target.value)}
                  >
                    <MenuItem value={1}>1</MenuItem>
                    <MenuItem value={3}>3</MenuItem>
                    <MenuItem value={5}>5</MenuItem>
                    <MenuItem value={7}>7</MenuItem>
                    <MenuItem value={9}>9</MenuItem>
                    <MenuItem value={11}>11</MenuItem>
                    <MenuItem value={15}>15</MenuItem>
                    <MenuItem value={17}>17</MenuItem>
                    <MenuItem value={19}>19</MenuItem>
                    <MenuItem value={21}>21</MenuItem>
                    <MenuItem value={23}>23</MenuItem>
                    <MenuItem value={25}>25</MenuItem>
                  </Select>
                </FormControl>
              </div>) }
              
            <TextField 
              required 
              id="key" 
              type={isShowMKey ? 'number' : 'string'}
              label={isShowMKey ? 'B Key' : 'Key'}
              fullWidth 
              multiline 
              focused
              // value={keyText}
              // onChange={(e)=> setKeyText(e.target.value)}
            />
            
            {isShowDecrypt && (
            <label class={styles.upload}>
            <input class={styles.button} type="file" onChange={(e) => readCsvFile(e)} />
              Upload Csv File
            </label>
            )}
  
            
            {resultText !=='' && (
            <Box display="flex" flexDirection="row" >
                <Box p={1} flexGrow={1}>
                  <Typography id="result-label" variant="h5" gutterBottom gutterTop>
                      Result:
                  </Typography>
                  <Typography id="result" variant="h5" gutterBottom gutterTop>
                      {resultText}
                  </Typography>
                  <FormControlLabel
              control={<Switch
                checked={is5}
                onChange={onSwitchChange}
                name="is5"
                color="primary"
              />}
              label="5 chunks"
            />
                </Box>
                <Box p={1}>
                  <IconButton aria-label="download" onClick={downloadTxtFile}>
                    <GetAppIcon />
                  </IconButton>
                  <IconButton aria-label="download" onClick={() => copyToClipboard(resultText)}>
                    <FileCopyIcon />
                  </IconButton>
                </Box>
            </Box>
            )}
            
              <Box display="flex" flexDirection="row" p={2} m={4} bgcolor="background.paper">
                <Box p={1} flexGrow={1}>
                  <Typography variant="h5" gutterBottom gutterTop>
                    Cipher Method
                  </Typography>
                  <RadioGroup aria-label="method" name="Method" value={method} onChange={onMethodChange}>
                    <FormControlLabel value="1" control={<Radio />} label="Vigenere Standard" />
                    <FormControlLabel value="2" control={<Radio />} label="Full Vigenere" />
                    <FormControlLabel value="3" control={<Radio />} label="Auto Key Vigenere" />
                    <FormControlLabel value="4" control={<Radio />} label="Extended Vigenere" />
                    <FormControlLabel value="5" control={<Radio />} label="Playfair" />
                    <FormControlLabel value="6" control={<Radio />} label="Affine" />
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
      </div>
      </StylesProvider>
    </ThemeProvider>
  );
}

export default App;
