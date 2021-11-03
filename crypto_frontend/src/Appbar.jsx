import React from "react";
import {
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  Button,
} from '@material-ui/core';

import { Link } from 'react-router-dom';


// import MailIcon from '@material-ui/icons/MailIcon';
// import InboxIcon from '@material-ui/icons/InboxIcon';
import styles from './App.module.css';


function App() {
  return (
<>
      <AppBar className={styles.appBar} position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu" >
          </IconButton>
          <Typography variant="h6">
            Kriptografi
          </Typography>
          
          <Button component={Link} to="/">
              Tugas 1 + Rc4
          </Button>

          <Button component={Link} to="/steganography">
              Steganography
          </Button>
          <Button component={Link} to="/rsa">
              RSA
          </Button>
          <Button component={Link} to="/pailier">
              Pailier
          </Button>
          <Button component={Link} to="/elgamal">
              Elgamal
          </Button>
          <Button component={Link} to="/ecc">
              ECC
          </Button>
          
        </Toolbar>
      </AppBar>
</>
  );
}

export default App;
