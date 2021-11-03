import React, {useState} from "react";
import {
  Button, 
  IconButton, 
  Typography, 
  TextField,
  Container,
  FormControlLabel,
  Box,
  Switch,
} from '@material-ui/core';
import styles from './App.module.css';
import axios from "axios";
import FileCopyIcon from '@material-ui/icons/FileCopy';
import GetAppIcon from '@material-ui/icons/GetApp';
import Layout from './Layout';

const Elgamal = () => {
  const [requestText, setRequestText] = useState('');
  const [resultText, setResultText] = useState('');
  const [table,setTable] = useState();
  const [publicKey, setPublicKey] = useState([]);
  const [privateKey, setPrivateKey] = useState([]);
  
  const copyToClipboard = (text) => {
    const el = document.createElement('textarea');
    el.value = text.replace(/ /g,'');
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
  }
  
  const downloadTxtFile = () => {
    const element = document.createElement("a");
    const file = new Blob([resultText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "cryptography.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
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
  
  
  const handleSubmitKey = (event) => {
    event.preventDefault();
    console.log("hit submit key");
    
    let data;
    
    
    data = {
      "data": {
        "algo_id": "10",
        "p": document.getElementById("p").value,
        "g": document.getElementById("g").value,
        "x": document.getElementById("x").value,
        "k": document.getElementById("k").value,
      }
    }
    
    axios.post(`http://127.0.0.1:5000/generate-keys`, data)
        .then(res => {
          const result = res.data;
          const public_key = result.public_key;
          const private_key = result.private_key;
          
          setPublicKey(public_key);
          setPrivateKey(private_key);
        })
      
  }
  
  const handleSubmitEncrypt = (event) => {
    event.preventDefault();
    let data;
    
    data = {
      "data": {
        "action": "encrypt",
        "algorithm": "elgamal",
        //TODO: Ini harusnya diganti sama public key nya
        "p": document.getElementById("p").value,
        "g": document.getElementById("g").value,
        "x": document.getElementById("x").value,
        "k": document.getElementById("k").value,
        "plaintext": document.getElementById("plaintext").value
      }
    }
    
    axios.post(`http://127.0.0.1:5000/result`, data)
        .then(res => {
          const result = res.data;
          setResultText(result);
          console.log("Public Key:");
          console.log(result.public_key);
          console.log("Private Key: ")
          console.log(result.private_key);
        })
  }
  
  const handleSubmitDecrypt = (event) => {
    event.preventDefault();
    let data;
    
    data = {
      "data": {
        "action": "decrypt",
        "algorithm": "elgamal",
        //TODO: Ini harusnya diganti sama private key nya
        "p": document.getElementById("p").value,
        "g": document.getElementById("g").value,
        "x": document.getElementById("x").value,
        "k": document.getElementById("k").value,
        "text": document.getElementById("plaintext").value
      }
    }
    
    axios.post(`http://127.0.0.1:5000/generate-public-key`, data)
    .then(res => {
      const result = res.data;
      setResultText(result);
    })
  }
  
  return <Layout><div className={styles.container}>
  <Container  maxWidth="md">
    <form noValidate autoComplete="off" onSubmit={handleSubmitKey}>      
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
              id="g"
              label="G" 
              multiline
              focused
            />
          </Box>
          <Box p={1} flexGrow={1}>
            <TextField 
              required 
              id="x"
              label="X" 
              multiline
              focused
            />
          </Box>
          <Box p={1} flexGrow={1}>
            <TextField 
              required 
              id="k"
              label="K" 
              multiline
              focused
            />
          </Box>
          <Box p={1} flexGrow={1}>
            <Button type="submit" className={styles.button}>Generate Key</Button>
          </Box>
      </Box>
      </form>
      <form noValidate autoComplete="off" onSubmit={handleSubmitEncrypt}>    
      <Box display="flex" flexDirection="row" >
          <Box p={1} flexGrow={1}>
            <TextField 
              required 
              id="plaintext"
              label="Plain Text" 
              multiline
              fullWidth 
              focused
            />
            <Button type="submit" className={styles.button}>Encrypt</Button>
          </Box>
          <Box p={1}>
            <IconButton aria-label="download" onClick={() => copyToClipboard(requestText)}>
              <FileCopyIcon />
            </IconButton>
          </Box>
      </Box>     
      </form>
        
      
        
      {/* <TextField 
        required 
        id="key" 
        type={isShowMKey ? 'number' : 'string'}
        label={isShowMKey ? 'B Key' : 'Key'}
        fullWidth 
        multiline 
        focused
      /> */}
      <form noValidate autoComplete="off" onSubmit={handleSubmitDecrypt}>    
      <TextField 
        required 
        id="ciphertext"
        label="Cipher Text" 
        multiline
        fullWidth 
        focused
      />
      
      <label class={styles.upload}>
      <input class={styles.button} type="file" onChange={(e) => readTxtFile(e)} />
        Upload Key File
      </label>
      
      <Button type="submit" className={styles.button}>Decrypt</Button>
      </form>

      
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
  </Container>
  
</div>
</Layout>
}

export default Elgamal;