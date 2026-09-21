import streamlit as st
import internal_functions as int_func

with st.form("search for medications", clear_on_submit=True,  enter_to_submit=True, border=True, width="stretch"):
    search_keyword = st.text_input("Search by active ingredient or symptom")
    submitted = st.form_submit_button("Search", icon = "🔍")


if submitted:
    results_query = int_func.search_medications(search_keyword)
    st.write(results_query)
