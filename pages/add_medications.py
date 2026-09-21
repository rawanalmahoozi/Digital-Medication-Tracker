import streamlit as st
import internal_functions as int_func

if st.button("Show a tip"):
  st.info(int_func.get_random_willness_tip())


if st.toggle("Add a medication"):

  name = st.text_input("Medication Name", key="med_name")

  if st.button("Fetch info"):
      info = int_func.get_medication_info(name)
      if info:
          st.session_state["ingredients"] = info["ingredient"]
          st.info("Found it. Ingredients filled from RxNorm.")
      else:
          st.info("Not found. Please enter manually.")

  with st.form("Adding Medication", clear_on_submit=True):
    expiry_date = st.date_input("Expiration Date", format="DD/MM/YYYY")
    dosage = st.text_input("Enter dosage in hours:")
    ingredient = st.text_input("Enter the ingridents", key ='ingredients' )
    symptoms = st.text_input("Enter the symptoms that this medication is used for. Enter them separated by commas")
    quantity = st.number_input("How many pills or tablets are in the package?", min_value=1, step=1)
    usage =st.text_input("Usage Instructions")
    urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
    category = st.selectbox("Category", ["Prescription", "Over the Counter", "Supplement", "First Aid"])

      # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
      int_func.add_medications(name, expiry_date, ingredient, symptoms, dosage, quantity, usage, urgency, category)
      st.toast(":green[Medication added successfully!]", duration = 'short')
      

