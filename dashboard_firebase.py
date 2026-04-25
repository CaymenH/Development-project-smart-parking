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
bay_data = None

latest = collection_name.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
for doc in latest.stream():
    st.header(f"Latest data for {bay}: {doc.to_dict()}")
    
    bay_data = doc.to_dict()


if bay_data:
    status_of_bay = bay_data.get("bay_status")



if status_of_bay == "vacant":
    st.markdown(":green[bay vacant]")
elif status_of_bay == "occupied":
    st.markdown(":red[bay occupied]")
elif status_of_bay == "disabled":
    st.markdown(":blue[disabled bay vacant]")
elif status_of_bay == "ultrasonic not detecting":
    st.markdown(":orange[ultrasonic not detecting]")
elif status_of_bay == "magnetic not detecting":
    st.markdown(":yellow[magnetic not detecting]")


time.sleep(5)
st.rerun()