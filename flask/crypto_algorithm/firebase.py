import pyrebase

config = {
  "apiKey": "AIzaSyB3-OsGCo0Agyk07yrq-H3XjomFMVeCREk",
  "authDomain": "steganography-b23a1.firebaseapp.com",
  "projectId": "steganography-b23a1",
  "storageBucket": "steganography-b23a1.appspot.com",
  "messagingSenderId": "291176171311",
  "appId": "1:291176171311:web:9acbcd076536848dad03da",
  "measurementId": "G-XKJ2JYGVN6",
  "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()



# path_on_cloud = "tubes5/test.txt"
# path_local = "tubes5/signature/test_download.txt"

# #download
# storage.child(path_on_cloud).download(path_local)

# #upload
# # storage.child("tubes5/test_upload.txt").put(path_local)

