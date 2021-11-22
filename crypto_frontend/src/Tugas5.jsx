import React, {useState, useEffect} from "react";
import {
  Button, 
  IconButton, 
  Typography, 
  TextField,
  Container,
  Box,
  AppBar,
  Tabs, 
  Tab,
} from '@material-ui/core';
import styles from './App.module.css';
import axios from "axios";
import FileCopyIcon from '@material-ui/icons/FileCopy';
import GetAppIcon from '@material-ui/icons/GetApp';
import Layout from './Layout';
import storage from "./firebase";

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
  const [value, setValue] = React.useState(0);
  const [publicKey, setPublicKey] = useState('');
  const [privateKey, setPrivateKey] = useState('');
  const [n, setN] = useState('');
  const [file, setFile] = useState();
  const [outputFileName, setOutputFileName] = useState("output.txt");
  const [status, setStatus] = useState();
  const [verifyResult, setVerifyResult] = useState();
  
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  
  const uploadSigning = ()=>{
    if(file == null) {
      alert("Something wrong with uploading file");
      return;
    }
      
    storage.ref(`/tubes5/signing/input/${file.name}`).put(file)
    .on("state_changed" , alert("File succesfully uploaded") , alert);
  }
  
  const uploadVerifying = ()=>{
    if(file == null) {
      alert("Something wrong with uploading file");
      return;
    }
      
    storage.ref(`/tubes5/verifying/${file.name}`).put(file)
    .on("state_changed" , alert("File succesfully uploaded") , alert);
  }
  
  const download = (filename) => {
    storage.ref(`/tubes5/signing/output/${filename}`).getDownloadURL().then((url) => {
      console.log("url");
      console.log(url);
      
      const xhr = new XMLHttpRequest();
      xhr.responseType = 'blob';
      xhr.onload = (event) => {
        var a = document.createElement('a');
        a.href = window.URL.createObjectURL(xhr.response);
        a.download = outputFileName;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();                            //Simulates a click event
      };
      xhr.open('GET', url);
      xhr.send();
      console.log("finish download");
    })
  }
  
  const getFilename = (path) => {
    var startIndex = (path.indexOf('\\') >= 0 ? path.lastIndexOf('\\') : path.lastIndexOf('/'));
    var filename = path.substring(startIndex);
    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        filename = filename.substring(1);
    }
    return filename
  }

  
  const copyToClipboard = (text) => {
    const el = document.createElement('textarea');
    el.value = text.replace(/ /g,'');
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
  }
  
  const downloadTxtFile = (text) => {
    const element = document.createElement("a");
    const file = new Blob([text], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "key.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }
  
  const handleSubmitGenerate = (event) => {
    event.preventDefault();
    console.log("hit submit key");
    
    let data;
    
    
    data = {
      "data": {
        "algo_id": "8",
        "p": document.getElementById("p").value,
        "q": document.getElementById("q").value,
        "e": document.getElementById("e").value,
      }
    }
    
    axios.post(`http://127.0.0.1:5000/generate-keys`, data)
        .then(res => {
          const result = res.data;
          const public_key = result.public_key;
          const private_key = result.private_key;
          console.log(result);
          setPublicKey(public_key[0]);
          setPrivateKey(private_key[0]);
          setN(private_key[1]);
        })
  }
  
  
  const handleSubmitSigning = (event) => {
    
    event.preventDefault();
    uploadSigning();
    
    console.log("hit signing key");
    setStatus("SIGNING. Please Wait");
    
    let data;
    
    
    data = {
      "data": {
        "method": "signing",
        "d": document.getElementById("d").value,
        "n": document.getElementById("n").value,
        "filename": getFilename(document.getElementById("upload-signing").value),
        "output_filename": outputFileName,
      }
    }
    
    axios.post(`http://127.0.0.1:5000/sha`, data)
        .then(res => {
          const result = res.data;
          console.log(result);
          setStatus("COMPLETE");
          
        })
  }
  
  useEffect(()=> {
    console.log("Halo");
    console.log(verifyResult);
  },[verifyResult])
  
  const handleSubmitVerifying = (event) => {
    
    event.preventDefault();
    uploadVerifying();
    
    console.log("hit signing key");
    
    let data;
    
    
    data = {
      "data": {
        "method": "verifying",
        "e": document.getElementById("e").value,
        "n": document.getElementById("n").value,
        "filename": getFilename(document.getElementById("upload-verifying").value),
      }
    }
    
    axios.post(`http://127.0.0.1:5000/sha`, data)
        .then(res => {
          const result = res.data;
          console.log(result);
          setVerifyResult(result.result.toString());
        })
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
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <TextField 
                  required 
                  id="p"
                  label="P" 
                  multiline
                  focused
                />
              </Box>
              <Box p={1} flexGrow={1}>
                <TextField 
                  required 
                  id="q"
                  label="Q" 
                  multiline
                  focused
                />
              </Box>
              <Box p={1} flexGrow={1}>
                <TextField 
                  required 
                  id="e"
                  label="E" 
                  multiline
                  focused
                />
              </Box>
              <Box p={1} flexGrow={1}>
                <Button type="submit" className={styles.button}>Generate Key</Button>
              </Box>
          </Box>
        </form>
        
        {publicKey !=='' && (
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <Typography id="result-label" variant="h5" gutterBottom gutterTop>
                    Public Key (e):
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
                    Private Key (d):
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
        
        {n !=='' && (
          <Box display="flex" flexDirection="row" >
              <Box p={1} flexGrow={1}>
                <Typography id="result-label" variant="h5" gutterBottom gutterTop>
                    N:
                </Typography>
                <Typography id="result" variant="h5" gutterBottom gutterTop>
                    {n}
                </Typography>
              </Box>
              <Box p={1}>
                <IconButton aria-label="download" onClick={downloadTxtFile}>
                  <GetAppIcon />
                </IconButton>
                <IconButton aria-label="download" onClick={() => copyToClipboard(n)}>
                <FileCopyIcon />
                </IconButton>
              </Box>
          </Box>
        )}
      </TabPanel>
      <TabPanel value={value} index={1}>
        <form noValidate autoComplete="off" onSubmit={handleSubmitSigning}>
          <Box display="flex" flexDirection="row" >
            <Box p={1}>
              <TextField 
                required 
                id="d"
                label="D" 
                multiline
                focused
                value={privateKey}
                onChange={e => setPrivateKey(e.target.value)}
              />
            </Box>
            <Box p={1}>
              <TextField 
                required 
                id="n"
                label="N" 
                multiline
                focused
                value={n}
                onChange={e => setN(e.target.value)}
              />
            </Box>
            <Box p={1}>
              <TextField 
                required 
                id="output"
                label="Output" 
                multiline
                focused
                value={outputFileName}
                onChange={e => setOutputFileName(e.target.value)}
              />
            </Box>
            <label class={styles.upload}>
            <input id="upload-signing" class={styles.button} type="file" onChange={ (e) => {setFile(e.target.files[0])}} />
              Upload File
            </label>
            
          </Box>
          <Button type="submit" className={styles.button}>Signing</Button>
        </form>
        {status && <Typography id="result" variant="h5" gutterBottom gutterTop>
          Status of signing is {status}
        </Typography>}
        {status==="COMPLETE" &&
        <IconButton aria-label="download" onClick={() => download(outputFileName)}>
          <GetAppIcon />
        </IconButton>}
      </TabPanel>
      <TabPanel value={value} index={2}>
        <form noValidate autoComplete="off" onSubmit={handleSubmitVerifying}>
          <Box display="flex" flexDirection="row" >
            <Box p={1}>
              <TextField 
                required 
                id="e"
                label="E" 
                multiline
                focused
                value={publicKey}
                onChange={e => setPublicKey(e.target.value)}
              />
            </Box>
            <Box p={1}>
              <TextField 
                required 
                id="n"
                label="N" 
                multiline
                focused
                value={n}
                onChange={e => setN(e.target.value)}
              />
            </Box>
            <label class={styles.upload}>
            <input id="upload-verifying" class={styles.button} type="file" onChange={(e) => {setFile(e.target.files[0])}} />
              Upload File
            </label>
          </Box>
          <Button type="submit" className={styles.button}>Verifying</Button>
        </form>
        <Typography id="result" variant="h5" gutterBottom gutterTop>
          Result of verifying is {verifyResult}
        </Typography>
      </TabPanel>
  </Container>
  
</div>
</Layout>
}

export default Tugas5;