import React, {useState} from "react";
import {
  Button, 
  IconButton, 
  Typography, 
  TextField,
  Container,
  Box,
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
    el.value = text.replace(/ /g,' ');
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
        "algorithm": "8",
        //TODO: Ini harusnya diganti sama public key nya
        "e": document.getElementById("e").value,
        "n": document.getElementById("n").value,
        "text": document.getElementById("plaintext").value
      }
    }
    
    axios.post(`http://127.0.0.1:5000/result`, data)
        .then(res => {
          const result = res.data;
          // setResultText(result);
          console.log("Result");
          console.log(result);
          setResultText(result.cipher);
        })
  }
  
  const handleSubmitDecrypt = (event) => {
    event.preventDefault();
    let data;
    
    data = {
      "data": {
        "action": "decrypt",
        "algorithm": "8",
        //TODO: Ini harusnya diganti sama private key nya
        "d": document.getElementById("d").value,
        "n": document.getElementById("n").value,
        "text": document.getElementById("ciphertext").value
      }
    }
    
    axios.post(`http://127.0.0.1:5000/result`, data)
    .then(res => {
      const result = res.data;
      console.log("Plainteks: ");
      console.log(result);
      setResultText(result.plain);
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
            <TextField 
              required 
              id="n"
              label="N" 
              multiline
              focused
            />
          </Box>
          <Box p={1} flexGrow={1}>
            <TextField 
              required 
              id="d"
              label="D" 
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