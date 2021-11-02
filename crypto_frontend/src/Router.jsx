import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Appbar from './Appbar';
import Tugas1 from './Tugas1';
import Steganography from './Steganography';

const Router= () => {
  return <BrowserRouter>
    <Switch>
      <Route exact path="/" component={Tugas1}/>
      <Route path="/steganography" component={Steganography}/>
    </Switch>
  </BrowserRouter>
}

export default Router;