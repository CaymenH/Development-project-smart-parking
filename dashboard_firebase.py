import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st


if not firebase_admin._apps:
    cred = credentials.Certificate("/home/c2025778/Rpi_codes/smart-parking-edd43-firebase-adminsdk-fbsvc-236aa62756.json")
    default_app = firebase_admin.initialize_app(cred, {
        'storageBucket': "smart-parking-edd43.firebasestorage.app"
    })
else:
    default_app = firebase_admin.get_app()

database = firestore.client(app=default_app)
bucket = storage.bucket(app=default_app)


 

st.title("Smart Parking Application Dashboard")

bay = st.selectbox("Select Parking Bay", ("Bay 1", "Bay 2", "Bay 3"))

bay_docs = database.collection(f"parking_{bay.lower().replace(' ', '_')}").stream() 


for doc in bay_docs:
     st.write(f"{doc.id} => {doc.to_dict()}")


