# 💊 Digital Medication Tracker
[Medication.app](https://medicationtracking.streamlit.app/)
[Medication.video](https://drive.google.com/file/d/1KJheUtv6Ss0XtQAxIXrXUVkyr_dHQQg3/view?usp=sharing)

A multi-page Streamlit application for managing personal medications, adding new meds, tracking intake, checking ingridentnts interactions with an AI advisor and monitoring compliance and refill/expiry status.

## Overview

This app helps a user keep track of the medications they take. It stores medication details, ingredients, and intake history in local CSV files, it combines two external services to make the experience smarter:

- **NIH RxNorm API** — automatically looks up the active ingredients of a medication by name when it's added.
- **LLM (via OpenRouter)** — reviews the user's full medication list and summarizes potential drug interactions and safety notes in plain language.

The app is built as a Streamlit multi-page app, with each page handling one part of the workflow.

## Features

- **Add Medication** — enter a medication's name, expiry date, ingredients, symptoms it treats, dosage frequency, quantity, usage instructions, urgency and category(Prescription, OTC, Supplement or First Aid). Ingredients can be auto-filled from RxNorm API or entered manually if the lookup fails. Also shows a random wellness tip.
- **Search for Medication** — search the saved medications by active ingredient or symptom. It warns the user if more than one medication shares the same active ingredient.
- **Medication Intake** — log each time a dose is taken, tracks remaining quantity and tells the user which medications are due for their next dose based on the dosage frequancy column.
- **Medication Advisor** — sends the current medication list (with ingredients) to an LLM to flag possible interactions and explain them simply.
- **View Medication List** — a dashboard showing:
  - all medications with their dosage and next scheduled intake time
  - warnings for medications that are expiring soon (30 days or less) or already expired
  - alerts for medications running low (below 25% remaining) and needing a refill
  - a daily schedule sorted by intake time
  - a star-rating system per medication (compliance tracking), with an option to sort the list by highest compliance

## Requirements

- Python 3.9
- Streamlit
- pandas
- requests
- python-dotenv
- openai (used here to call OpenRouter's API)

Install everything from requests.txt

## Setup

1. Clone or download the project files, keeping the folder structure abve (main file at the root, page files inside a `pages/` folder).
2. Create a `.env` file in the project root with your OpenRouter API key:
   ```
   API_KEY=your_openrouter_api_key_here
   ```
3. Make sure `wellness_tips.csv` exists with a `content` column of tip text. `medications.csv`, `medications_intake.csv`, and `compliance.csv` will be created automatically the first time they're needed.

## Running the App

```bash
streamlit run medication_app.py
```

This opens the app in your browser, with the navigation menu linking to all five pages.

## How the Data Works

- **medications.csv** — one row per medication, with columns: `name`, `expiry_date`, `ingredient`, `symptoms`, `dosage`, `quantity`, `usage`, `urgency`, `category`.
- **medications_intake.csv** — one row per logged dose, with `name`, `intake_time`, and `remaining_quantity`, used to calculate when the next dose is due and how much of a medication is left.
- **compliance.csv** — stores the star rating a user gives each medication, used to sort the medication list by compliance.

## Notes & Limitations

- Dosage frequency is entered as text (e.g. `"Every 8 hours"`, `"As Needed"`) the app extracts the number of hours from that text to calculate next-dose timing.
- The AI advisor is for informational purposes only as it explicitly reminds the user to confirm anything important with a doctor or pharmacist and is not a substitute for medical advice.
- This project was built as a course assignment, so the implementation intentionally sticks to techniques covered in class (e.g. `requests`, `.json()`, `to_csv`) rather than more advanced libraries or patterns.