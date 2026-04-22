import streamlit as st


docs = database.collection("parking_bay1").stream()

for doc in docs:
    st.write(f"{doc.id} => {doc.to_dict()}")