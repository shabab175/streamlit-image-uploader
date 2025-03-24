import streamlit as st
import requests
import base64
from io import BytesIO

# GitHub Configuration
GITHUB_TOKEN = "your_github_token"  # Store this in Streamlit Secrets
GITHUB_REPO = "your_github_username/your_repo"
GITHUB_BRANCH = "main"
UPLOAD_PATH = "uploads/"  # Folder inside the repo

def upload_to_github(image, filename):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{UPLOAD_PATH}{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Convert image to base64
    img_bytes = image.getvalue()
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    
    data = {
        "message": f"Upload {filename}",
        "content": img_b64,
        "branch": GITHUB_BRANCH
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

# Authentication
USER_CREDENTIALS = {"admin": "password123"}  # Change for real use

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    st.title("Image Upload")
    uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption=uploaded_file.name)
            response = upload_to_github(uploaded_file, uploaded_file.name)
            if "content" in response:
                st.success(f"{uploaded_file.name} uploaded successfully")
            else:
                st.error("Upload failed")
