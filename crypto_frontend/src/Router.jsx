import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Appbar from './Appbar';
import Tugas1 from './Tugas1';
import Steganography from './Steganography';
import ECC from './ECC';
import Elgamal from './Elgamal';
import Pailier from './Pailier';

const Router= () => {
  return <BrowserRouter>
    <Switch>
      <Route exact path="/" component={Tugas1}/>
      <Route path="/steganography" component={Steganography}/>
      <Route path="/ecc" component={ECC}/>
      <Route path="/elgamal" component={Elgamal}/>
      <Route path="/pailier" component={Pailier} />
    </Switch>
  </BrowserRouter>
}

export default Router;