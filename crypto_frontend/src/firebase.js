import firebase from 'firebase';

const firebaseConfig = {
  apiKey: "AIzaSyB3-OsGCo0Agyk07yrq-H3XjomFMVeCREk",
  authDomain: "steganography-b23a1.firebaseapp.com",
  projectId: "steganography-b23a1",
  storageBucket: "steganography-b23a1.appspot.com",
  messagingSenderId: "291176171311",
  appId: "1:291176171311:web:9acbcd076536848dad03da",
  measurementId: "G-XKJ2JYGVN6"
};

firebase.initializeApp(firebaseConfig);
var storage = firebase.storage();
export default storage;