import streamlit as st
import internal_functions as int_func

st.subheader("Interaction & Safety Advisor 🤖")

if st.button("Check interactions"):
    count, prompt = int_func.build_medication_prompt()

    if count < 2:
        st.info("Add at least two medications to check for interactions.")
    else:
        answer = int_func.get_llm_response(prompt)
        if answer:
            st.write(answer)
            st.caption("AI-generated. Not medical advice. Confirm with a pharmacist.")
        else:
            st.error("Could not reach the AI service. Try again.")