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
    print(f"{doc.id} => {doc.to_dict()}")

st.write("smart parking application")

main_page = st.Page("main_page.py", title="Select your bay")
bay_1 = st.Page("bay_1.py", title="parking bay 1 info")
bay_2 = st.Page("bay_2.py", title="parking bay 2 info")
bay_3 = st.Page("bay_3.py", title="parking bay 3 info")

pg = st.navigation([main_page, bay_1, bay_2, bay_3])
pg.run()