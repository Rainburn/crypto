import React, {useEffect, useState} from "react";
import {
  Button, 
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
  AppBar,
  Tabs, 
  Tab,
} from '@material-ui/core';
import styles from './App.module.css';
import axios from "axios";
import FileCopyIcon from '@material-ui/icons/FileCopy';
import GetAppIcon from '@material-ui/icons/GetApp';
import Layout from './Layout';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

const Tugas5 = () => {
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
  const [value, setValue] = React.useState(0);
  const [publicKey, setPublicKey] = useState('public');
  const [privateKey, setPrivateKey] = useState('private');
  
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  
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
    element.download = "key.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }
  
  const trimAlphabetic = (text) => {
    return text.replace(/[^A-Za-z]/g, '');
  }
  
  const handleSubmitGenerate = (event) => {
    event.preventDefault();
    
    let data;
    let text = document.getElementById("plain/ciphertext").value;
    
    if (method == '7') { // Method is RC4
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
          var resultText = "";
          var resLength = result.length

          var i = 0;
          while (i < resLength) {
            resultText += String.fromCharCode(result[i]);
            i++;
          }
          setResultText(resultText)
          
          if(res.data.table!=undefined){
            downloadCsv(res.data.table);
          }
        })
        
        return
    
      }
    

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
        
        if(res.data.table!==undefined){
          downloadCsv(res.data.table);
        }
      })
  }
  
  
  const handleSubmitSigning = (event) => {
    event.preventDefault();
  }
  
  const handleSubmitVerifying = (event) => {
    event.preventDefault();
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
  
  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }
  
  return <Layout><div className={styles.container}>
  <Container  maxWidth="md">
  <AppBar position="static">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Generate Key" {...a11yProps(0)} />
          <Tab label="Signing" {...a11yProps(1)} />
          <Tab label="Verifying" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        <form noValidate autoComplete="off" onSubmit={handleSubmitGenerate}>
          <Button type="submit" className={styles.button}>Generate Key</Button>
        </form>
        
        {publicKey !=='' && (
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <Typography id="result-label" variant="h5" gutterBottom gutterTop>
                    Public Key:
                </Typography>
                <Typography id="result" variant="h5" gutterBottom gutterTop>
                    {publicKey}
                </Typography>
              </Box>
              <Box p={1}>
                <IconButton aria-label="download" onClick={downloadTxtFile}>
                  <GetAppIcon />
                </IconButton>
                <IconButton aria-label="download" onClick={() => copyToClipboard(publicKey)}>
                  <FileCopyIcon />
                </IconButton>
              </Box>
          </Box>
        )}
        
        {privateKey !=='' && (
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <Typography id="result-label" variant="h5" gutterBottom gutterTop>
                    Private Key:
                </Typography>
                <Typography id="result" variant="h5" gutterBottom gutterTop>
                    {privateKey}
                </Typography>
              </Box>
              <Box p={1}>
                <IconButton aria-label="download" onClick={downloadTxtFile}>
                  <GetAppIcon />
                </IconButton>
                <IconButton aria-label="download" onClick={() => copyToClipboard(privateKey)}>
                  <FileCopyIcon />
                </IconButton>
              </Box>
          </Box>
        )}
      </TabPanel>
      <TabPanel value={value} index={1}>
        <form noValidate autoComplete="off" onSubmit={handleSubmitSigning}>
          <label class={styles.upload}>
          <input class={styles.button} type="file" onChange={(e) => readTxtFile(e)} />
            Upload File
          </label>
          <Button type="submit" className={styles.button}>Signing</Button>
        </form>
      </TabPanel>
      <TabPanel value={value} index={2}>
        <form noValidate autoComplete="off" onSubmit={handleSubmitVerifying}>
          <label class={styles.upload}>
          <input class={styles.button} type="file" onChange={(e) => readTxtFile(e)} />
            Upload File
          </label>
          <Button type="submit" className={styles.button}>Verifying</Button>
        </form>
      </TabPanel>
  </Container>
  
</div>
</Layout>
}

export default Tugas5;