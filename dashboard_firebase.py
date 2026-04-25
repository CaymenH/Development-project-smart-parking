import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import time

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

bay_fix = bay.lower().replace(' ', '')
collection_name = database.collection(f"parking_{bay_fix}")


latest = collection_name.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
for doc in latest.stream():
    st.header(f"Latest data for {bay}: {doc.to_dict()}")

st.markdown[":red[bay 1 occupied]"]
st.markdown[":red[bay 2 occupied]"]
st.markdown[":red[disabled bay 3 occupied]"]

st.markdown[":green[bay 1 vacant]"]
st.markdown[":green[bay 2 vacant]"]
st.markdown[":blue [ disabled bay 3 vacant]"]

st.markdown[":orange[ultrasonic not detecting]"]
st.markdown[":yellow[magnetic not detecting]"]
if st.button("Refresh Data"):
    st.rerun()

time.sleep(5)
st.rerun()

