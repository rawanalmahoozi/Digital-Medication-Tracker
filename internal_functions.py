import streamlit as st
import pandas as pd
import os
from datetime import datetime as dt 
import requests
#from dotenv import load_dotenv
#from openai import OpenAI


def add_medications(name, expiry_date, ingredient, symptoms, dosage, quantity, usage, urgency, category):
    '''add_medications function will take the user input related to the new medication and add
       it to the medications.csv file. If the file does not exist, it will create one'''

    new_med = pd.DataFrame([{
        'name': name,
        'expiry_date': expiry_date,
        'ingredient': ingredient,
        'symptoms': symptoms,
        'dosage': dosage,
        'quantity': quantity,
        'usage': usage,
        'urgency': urgency, 
        'category': category
    }])

    if not os.path.exists('medications.csv') or os.path.getsize('medications.csv') == 0:
        new_med.to_csv('medications.csv', mode='a', header=True, index=False)
    else:
        new_med.to_csv('medications.csv', mode='a', header=False, index=False)


def search_medications(search_keyword):
    '''search_medications function will take the entered keyword and search for it in the medications file.
    it will check both the active ingredient and the symptoms columns for a match. If a match is found, it 
    return the names of the medications. also if the kewword is an active ingredient for more that one
    medication, it will display a warning to the user to consult their doctor if that is okay.'''

    med = pd.read_csv('medications.csv')
    search_keyword = search_keyword.strip()  # Remove space 

    the_filter = (med['ingredient'].str.contains(search_keyword, case=False, na=False)) | (med['symptoms'].str.contains(search_keyword, case=False, na=False))
    result = (med['name'][the_filter])

    if result.empty:
        return ("No medications found for the search keyword.")
    else:
        if med['ingredient'].str.contains(search_keyword, case=False, na=False).sum()  > 1: 
            st.warning("Multiple medications uses the same active ingredient. Please be aware of this and consult your doctor "
            "or pharmacist for more information." , icon="🚨")
        names = "\n\n".join(result.tolist())
        return ((f'search results for :blue[{search_keyword}] is: \n\n{names}'))


def log_medication_intake(med_name, med_quantity):
    '''log_medication_intake function will track when the user takes a medication and how many 
    pills are left in the package.'''

    if (os.path.exists('medications_intake.csv')) and (os.path.getsize('medications_intake.csv') > 0):
        intake_df = pd.read_csv('medications_intake.csv')
        intake_count = (intake_df['name'] == med_name).sum()
    else: 
        intake_count = 0

    remaining_quantity = med_quantity - intake_count

    new_med_intake = pd.DataFrame([{
        'name': med_name,
        'intake_time': dt.now(),
        'remaining_quantity': remaining_quantity - 1 
    }])
    if not os.path.exists('medications_intake.csv') or os.path.getsize('medications_intake.csv') == 0:
        new_med_intake.to_csv('medications_intake.csv', mode='a', header=True, index=False)
    else:
        new_med_intake.to_csv('medications_intake.csv', mode='a', header=False, index=False)


def medication_intake_calculation(medication_list):
    '''medication_intake_calculation function is gonna list the medications that the user should take now
    based on the last time they took the medication and the dosage frequency. It will return a list of medications or 
    a message that no medication intake is due.'''

    med_df = pd.read_csv('medications.csv')
    intake_df = pd.read_csv('medications_intake.csv')
    intake_df['intake_time'] = pd.to_datetime(intake_df['intake_time'])

    medication_list = medication_list.split("\n\n")
    intake_list = [] 
    for med_name in medication_list:
        #to remove any spaces:
        med_name = med_name.strip() 

        time_filter = intake_df['name'] == med_name
        dosage_filter = med_df['name'] == med_name

        pattern = r'(\d+)' 
        med_dosage_str = med_df[dosage_filter]['dosage']
        med_dosage_extracted = med_dosage_str.str.extract(pattern)
        if med_dosage_extracted.empty or pd.isna(med_dosage_extracted.iloc[0, 0]):
            continue

        med_dosage = int(med_dosage_extracted.iloc[0, 0])

        med_dosage_timedelta = pd.Timedelta(hours=med_dosage)
        if intake_df[time_filter].empty:
            continue

        last_med_intake = dt.now() - (intake_df[time_filter]['intake_time'].iloc[-1]) #to get the last intake time
        if last_med_intake >= med_dosage_timedelta: 
            intake_list.append(f':green[You can take your next dose of {med_name} now.]')

    if intake_list:
        return ("\n\n".join(intake_list))
    else: 
        return (f'No medication intake is due')


def get_medication_list():
    '''The get medication list will be vewing all the medications the user takes in a dataframe style'''

    med_df = pd.read_csv('medications.csv')
    med_intake_df = pd.read_csv('medications_intake.csv')

    if med_df.empty:
        return "No medications found in the system."
    
    
    else: 
        scheduled_intake = []
        for i in range(len(med_df)): 
            name = med_df['name'].iloc[i]
            dosage = med_df['dosage'].iloc[i]
            med_intake = med_intake_df[med_intake_df['name'] == name]

            if "Every" in dosage:
                if med_intake.empty: 
                    scheduled_intake.append("No intake records found.")
                    continue

                dosage_hours = int(dosage.split()[1])
                last_intake = pd.to_datetime(med_intake['intake_time'].iloc[-1])
                next_intake = last_intake + pd.Timedelta(hours=dosage_hours)

                hours_str = str(next_intake.hour).zfill(2)
                min_str = str(next_intake.minute).zfill(2)
                scheduled_intake.append(f'{hours_str}:{min_str}')
            else: 
                scheduled_intake.append("As Needed")
            
            

    medication_list_df = pd.DataFrame({
        'Medication Name': med_df['name'],
        'Dosage': med_df['dosage'],
        'Next Scheduled Intake': scheduled_intake})

    return medication_list_df

def flagging ():
    '''The flagging will be checking for medu=ications that will expire soon, has already expired and also medications that needs refill'''
    med_df = pd.read_csv('medications.csv')
    med_intake_df = pd.read_csv('medications_intake.csv')

    expired_meds = []
    refill_meds = []

    for med_name, med_expiry, med_qty in zip(med_df['name'], med_df['expiry_date'], med_df['quantity']):

        today = dt.now()
        med_expiry = pd.to_datetime(med_expiry, dayfirst=True)
        is_expire = med_expiry - today 
        is_expire = is_expire.days

        if (is_expire <= 30) and (is_expire > 0): 
            expired_meds.append(f'{med_name} expieres in :orange[{is_expire}] days')

        if is_expire <= 0:
            expired_meds.append(f'{med_name} :red[already expiered]')

        med_intake = med_intake_df[med_intake_df['name'] == med_name]
        if med_intake.empty: 
            continue

        remaining_pills = med_intake['remaining_quantity'].iloc[-1] 
        need_refill = (remaining_pills/med_qty) * 100         

        if need_refill <= 25: 
            refill_meds.append(f'less than 25% of {med_name} is remaining please consider a refill')

    return expired_meds, refill_meds


def daily_schedule(): 
    '''This function will list the medications but this time it will sort them based on the time 
    they should be taken at '''
    meds_list= get_medication_list()
    timed_meds = []
    other_meds = []

    for i in range(len(meds_list)):
        if ':' in meds_list['Next Scheduled Intake'].iloc[i]:
            timed_meds.append(meds_list.iloc[i])
        else: 
            other_meds.append(meds_list.iloc[i])

    timed_meds = sorted(timed_meds, key=lambda row: row['Next Scheduled Intake'])

    return timed_meds, other_meds


def get_medication_info(name):
    '''This function is used for the API data fetching'''

    url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={name}&search=2"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    ids = response.json()["idGroup"].get("rxnormId")
    if not ids:
        return None

    url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{ids[0]}/related.json?tty=IN"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    groups = response.json()["relatedGroup"].get("conceptGroup", [])
    names = []
    for group in groups:
        for concept in group.get("conceptProperties", []):
            names.append(concept["name"])

    if names:
        return {"ingredient": ", ".join(names)}
    return None



#load_dotenv('.env')
#open_api_key = os.getenv('API_KEY')
open_api_key = st.secrets['API_KEY']
if not open_api_key:
    raise RuntimeError("API_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1", # putting what we want 
    api_key= open_api_key #open api key is my key
)

def get_llm_response(prompt):
    '''This is the function that will be used for the LLM'''
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medication interaction and safety advisor. The user will give you "
                    "a list of their current medications. Summarize any potential drug-interaction "
                    "warnings between them, and explain any medical terms in plain language be precise and keep it as "
                    "short and simple as you can. don't explain too much make it max five lines."
                    "Only discuss the medications listed. If you are not sure about an interaction, "
                    "say so instead of guessing. and end by recommending they confirm with a doctor or pharmacist."
                )
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response

def build_medication_prompt():
    '''The LLM is supposed to give help based on the medication's ingringredients, so this function will take all meds
    and it's ingredients and feeds it to the LLM'''
    meds = pd.read_csv("medications.csv")

    lines = []
    for i in range(len(meds)):
        row = meds.iloc[i] 
        lines.append(f"- {row['name']} (ingredients: {row['ingredient']})")

    prompt = "My current medications:\n" + "\n".join(lines)
    return len(meds), prompt


def get_random_willness_tip(): 
    '''Used to generate a random wellness tip from the database'''
    tips = pd.read_csv("wellness_tips.csv")
    return tips["content"].sample(1).iloc[0]


def load_ratings(): 
    '''This function is used to load the ratings from the csv to the frontend'''
    if not os.path.exists("compliance.csv"):
        return {}

    df = pd.read_csv("compliance.csv")
    ratings = {}

    for i in range(len(df)): 
        name = df.loc[i,"Medication Name"]
        ratings[name] = int (df.loc[i, "Rating"])
    return ratings

def save_rating(name,rating): 
    '''The function will automatically take and save the ratings for each rated medication'''
    ratings = load_ratings()
    ratings[name] = rating
    df = pd.DataFrame({"Medication Name": list(ratings.keys()), 
                       "Rating" : list(ratings.values())})

    df.to_csv("compliance.csv", index=False)
    