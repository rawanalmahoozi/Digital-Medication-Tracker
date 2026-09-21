import streamlit as st
import requests
#from IPython.display import JSON
#from dotenv import load_dotenv
import os
from openai import OpenAI

st.title('Digital :red[Medication] Tracker', icon = '⚕️', text_alignment = 'center')

add_page = st.Page("pages/add_medications.py", title="Add Medication")
search_page = st.Page("pages/medications_search.py", title="Search for Medication")
medicatoin_intake = st.Page("pages/medications_intake.py", title="Medication Intake")
medicatoin_advisior = st.Page("pages/medication_advisior.py", title="Medication Advisior")
list_page = st.Page("pages/medications_log.py", title="View Medication List")

pg = st.navigation([ add_page, search_page, medicatoin_intake, medicatoin_advisior, list_page])
pg.run()




