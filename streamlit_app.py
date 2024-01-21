

import streamlit as st

from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Assuming you have already set the secrets in Streamlit using st.secrets["your_secret_name"]
service_account_type = st.secrets["type"]
project_id = st.secrets["project_id"]
private_key_id = st.secrets["private_key_id"]
private_key = st.secrets["private_key"]
client_email = st.secrets["client_email"]
client_id = st.secrets["client_id"]
auth_uri = st.secrets["auth_uri"]
token_uri = st.secrets["token_uri"]
auth_provider_x509_cert_url = st.secrets["auth_provider_x509_cert_url"]
client_x509_cert_url = st.secrets["client_x509_cert_url"]
universe_domain = st.secrets["universe_domain"]

# Create a JSON object
json_data = {
    "type": service_account_type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}
# Create a credentials.Certificate object
cred = credentials.Certificate(json_data)
if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

def main():
    # Initialize session state
    if 'date_input' not in st.session_state:
        st.session_state.date_input = datetime.today()
        
    # page configuration 
    st.set_page_config(page_title="OpenAI", page_icon="🖖",layout="wide")
    
    # Streamlit UI
    st.title("Daily Tiffin Expense Tracker")

    
    
    
if __name__ == "__main__":
    main()



# 