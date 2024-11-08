from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

db = get_db()
collections = ["social_data", "notes"]

# just in case collection does not exist, create
for value in collections:
    try:
        db.create_collection(value)
    except:
        pass

social_data_collection = db.get_collection("social_data")
notes_collection = db.get_collection("notes")