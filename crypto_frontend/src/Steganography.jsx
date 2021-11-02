import React, {useEffect, useState} from "react";
import Layout from './Layout';
import {Button, Container, Box, Typography} from '@material-ui/core';
import styles from './App.module.css' 
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import VideocamIcon from '@material-ui/icons/Videocam';
import storage from './firebase';


const Steganography= () => {
  const [image , setImage] = useState('');
  const upload = ()=>{
    if(image == null) {
      alert("something wrong");
      return;
    }
      
    storage.ref(`/images/${image.name}`).put(image)
    .on("state_changed" , alert("success") , alert);
  }
  
  useEffect(()=>{
    console.log(image);
  },[image])
  
  return <Layout>
    <div className={styles.container}>
      <Container  maxWidth="md">
        
      <Box p={1} flexGrow={1}>
        <Typography variant="h5" gutterBottom gutterTop>
          Embedding
        </Typography>
      
      <form>
      <input
        accept="image/png, image/bmp"
        className={styles.input}
        id="contained-button-file"
        type="file"
        onChange={ (e) => {setImage(e.target.files[0])}}
      />
      <label htmlFor="contained-button-file">
        <IconButton color="primary" aria-label="upload picture" component="span">
          <PhotoCamera />
        </IconButton>
      </label>
      </form>
      
      <form>
      <input
        accept="audio/*,video/*,image/*"
        className={styles.input}
        id="contained-button-file"
        type="file"
      />
      <label htmlFor="contained-button-file">
        <IconButton color="primary" aria-label="upload picture" component="span">
          <VideocamIcon />
        </IconButton>
      </label>
      </form>
      
      
      </Box>
      <Button onClick={upload} variant="contained" color="primary">
        Embed
      </Button>
      <Box p={1} flexGrow={1}>
        <Typography variant="h5" gutterBottom gutterTop>
          Extraction
        </Typography>
        <input
        accept="image/png, image/bmp"
        className={styles.input}
        id="contained-button-file"
        type="file"
      />
      <label htmlFor="contained-button-file">
        <IconButton color="primary" aria-label="upload picture" component="span">
          <PhotoCamera />
        </IconButton>
      </label>
      
      <input
        accept="audio/*,video/*,image/*"
        className={styles.input}
        id="contained-button-file"
        type="file"
      />
      <label htmlFor="contained-button-file">
        <IconButton color="primary" aria-label="upload picture" component="span">
          <VideocamIcon />
        </IconButton>
      </label>
      </Box>
      <Button variant="contained" color="primary" component="span">
          Extract
      </Button>
      </Container>
    </div>
  </Layout>
}

export default Steganography;