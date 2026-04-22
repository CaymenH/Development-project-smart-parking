import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st

cred = credentials.Certificate(  "/home/c2025778/Rpi_codes/smart-parking-edd43-firebase-adminsdk-fbsvc-236aa62756.json")
default_app = firebase_admin.initialize_app(cred, {
    'storageBucket': "smart-parking-edd43.firebasestorage.app"
})

database = firestore.client(app=default_app)
bucket = storage.bucket(app=default_app)


docs = database.collection("parking_bay2").stream()

for doc in docs:
     st.write(f"{doc.id} => {doc.to_dict()}")

import streamlit as st

docs = database.collection("parking_bay2").stream()

for doc in docs:
     st.write(f"{doc.id} => {doc.to_dict()}")
