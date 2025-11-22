import streamlit as st
from pathlib import Path
from langchain_cohere.sql_agent.agent import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="SQL Databases Query Bot Using LangChain", page_icon="🦜🔗")
st.title("🦜🔗 SQL Databases Query Bot Using LangChain")

LOCAL_DB="USE_LOCALDB"
MYSQL_DB="USE_MYSQLDBS"

radio_options=['Use Sqlite3 Database Student.db', 'Connect to MySQL DBs']

selected_option = st.sidebar.radio(label="select the DB which you want to query", options=radio_options)

if selected_option==radio_options[1]:
    db_uri=MYSQL_DB
    mysql_host=st.text_input('Provide MySQL host to connect to')
    mysql_database=st.text_input('MySQL Database')
    mysql_user=st.text_input('MySQL User Name')
    mysql_password=st.text_input('MySQL User Password', type="password")
else:
    db_uri=LOCAL_DB

groq_api_key=st.sidebar.text_input(label='GROQ_API_KEY', type='password')  

if not db_uri:
    st.info("please enter database information and uri")

if not groq_api_key:
    st.info("please enter your groq api key information")


#LLM Model
model = ChatGroq(groq_api_key = groq_api_key, model="llama-3.1-8b-instant", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_database=None, mysql_user=None, mysql_password=None):
    if db_uri==LOCAL_DB:
        db_filepath=(Path(__file__).parent/"student.db").absolute()
        print(db_filepath)
        creator = lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator))
    elif db_uri==MYSQL_DB:
        st.error("Please provide all MySQL connection details.")
        st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}"))
                      
if db_uri==MYSQL_DB:
    db=configure_db(db_uri,mysql_host,mysql_database,mysql_user,mysql_password)
else:
    db=configure_db(db_uri)    


#toolkit