import streamlit as st

docs = database.collection("parking_bay2").stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
