import streamlit as st
import pandas as pd 
import internal_functions as int_func

meds = pd.read_csv('medications.csv')
pattern = r'(\d+)'
filterded_meds = meds['dosage'].str.contains(pattern, case=False, na=False)
results = meds[filterded_meds]
medication_list = "\n\n".join(results['name'].tolist())

for name, dosage, quantity in zip(results['name'], results['dosage'], results['quantity']): 
    submitted = st.button(f'I took my {name}', key=f'{name}_take_button')
    if submitted: 
        int_func.log_medication_intake(name, quantity)
        st.toast(f":green[Medication {name} taken successfully!]", duration = 'short')

intake_results = int_func.medication_intake_calculation(medication_list)

st.warning(intake_results, icon="⚠️") 



