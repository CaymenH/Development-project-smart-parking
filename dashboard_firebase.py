import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import time

# installing of firebase admin and linking to firestore
if not firebase_admin._apps:
    cred = credentials.Certificate("/home/c2025778/Rpi_codes/smart-parking-edd43-firebase-adminsdk-fbsvc-236aa62756.json")
    default_app = firebase_admin.initialize_app(cred, {
        'storageBucket': "smart-parking-edd43.firebasestorage.app"
    })
else:
    default_app = firebase_admin.get_app()

database = firestore.client(app=default_app)
bucket = storage.bucket(app=default_app)

bay_data = None
status_of_bay = None

st.title("Smart Parking Application Dashboard")

bay = st.selectbox("Select Parking Bay", ("Bay 1", "Bay 2", "Bay 3"))

bay_fix = bay.lower().replace(' ', '')
collection_name = database.collection(f"parking_{bay_fix}")


latest = collection_name.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
docs = list(latest.stream())
bay_data = docs[0].to_dict() if docs else None


if bay_data:
    status_of_bay = bay_data.get("bay_status")
else:
    st.warning("No data available for the selected bay.")

if status_of_bay == "bay 1 vacant":
    st.markdown(
    "<p style='font-size:40px;color:green;'>bay vacant</p>", 
    unsafe_allow_html=True)
elif status_of_bay == "bay 2 vacant":
    st.markdown(
    "<p style='font-size:40px;color:green;'>bay vacant</p>", 
    unsafe_allow_html=True)
elif status_of_bay == "bay 3 vacant":
    st.markdown(
        "<p style='font-size:40px;color:blue;'>bay vacant</p>", 
    unsafe_allow_html=True)
elif status_of_bay == "bay 1 occupied":
    st.markdown(
        "<p style='font-size:40px;color:red;'>bay occupied</p>", 
    unsafe_allow_html=True)
elif status_of_bay == "bay 2 occupied":
    st.markdown(
        "<p style='font-size:40px;color:red;'>bay occupied</p>", 
        unsafe_allow_html=True) 
elif status_of_bay == "bay 3 occupied":
    st.markdown(
    "<p style='font-size:40px;color:red;'>bay occupied</p>", 
    unsafe_allow_html=True)
elif status_of_bay == "ultrasonic not detecting":
    st.markdown(
        "<p style='font-size:40px;color:orange;'>ultrasonic not detecting</p>", 
        unsafe_allow_html=True
    )
elif status_of_bay == "magnetic not detecting":
    st.markdown(
        "<p style='font-size:40px;color:orange;'>magnetic not detecting</p>", 
        unsafe_allow_html=True
    )
    


time.sleep(3)
st.rerun()