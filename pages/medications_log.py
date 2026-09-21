import streamlit as st
import internal_functions as int_func
import pandas as pd

saved_ratings = int_func.load_ratings()
med_list = int_func.get_medication_list()

if st.toggle("Sort by highest compliance"):
    ratings = []
    for i in range(len(med_list)):
        name = med_list.iloc[i]["Medication Name"]
        ratings.append(saved_ratings.get(name, -1) + 1)
    med_list["Compliance (stars)"] = ratings
    med_list = med_list.sort_values("Compliance (stars)", ascending=False)

st.dataframe(med_list, hide_index=True)

expire_meds, refill_meds = int_func.flagging()

if expire_meds:
    st.warning("\n\n".join(expire_meds))

if refill_meds:
    st.info("\n\n".join(refill_meds))


st.title("Medication Daily Schedule 🗓️")
timed_meds, other_meds = int_func.daily_schedule()
all_meds = timed_meds + other_meds
all_meds = pd.DataFrame(all_meds)

for i in range(len(all_meds)): 
    row = all_meds.iloc[i]
    name = row['Medication Name']
    col1, col2, col3, col4 = st.columns(4)
    col1.write(name)
    col2.write(row['Dosage'])
    col3.write(row['Next Scheduled Intake'])
    rating = col4.feedback(options ='stars', key=f'feedback_{name}', default =saved_ratings.get(name))

    if (rating is not None) and (rating != saved_ratings.get(name)):
        int_func.save_rating(name,rating)
        st.rerun()

