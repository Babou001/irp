import streamlit as st
import requests
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

st.page_link("streamlit_pages/home.py", label="Home", icon="🏠")
st.header("Dataset PDF Documents :file_folder:")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Indexation en cours..."):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
        }
        try:
            r = requests.post(f"{FASTAPI_URL}/upload", files=files, timeout=120)
            if r.ok:
                st.success(f" {r.json().get('message', 'Indexed')} ({uploaded_file.name})")
            else:
                st.error(f"Erreur d'indexation : {r.text}")
        except Exception as e:
            st.error(f"Impossible d'appeler l'API /upload : {e}")
