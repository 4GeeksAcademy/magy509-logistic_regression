import streamlit as st
import requests
import pandas as pd
import json
import pickle

model_url = "https://raw.githubusercontent.com/4GeeksAcademy/magy509-logistic_regression/main/models/logistic_regression_opt.sav"

response = requests.get(model_url)
with open("logistic_regression_opt.sav", "wb") as f:
    f.write(response.content)

with open("logistic_regression_opt.sav", "rb") as file:
    model = pickle.load(file)

#Cargar Reglas
rules_urls = {
    "default_rules": "https://raw.githubusercontent.com/4GeeksAcademy/magy509-logistic_regression/refs/heads/main/rules/default_rules.json",
    "contact_rules": "https://raw.githubusercontent.com/4GeeksAcademy/magy509-logistic_regression/refs/heads/main/rules/contact_rules.json",
    "month_rules": "https://raw.githubusercontent.com/4GeeksAcademy/magy509-logistic_regression/refs/heads/main/rules/month_rules.json",
    "poutcome_rules": "https://raw.githubusercontent.com/4GeeksAcademy/magy509-logistic_regression/refs/heads/main/rules/poutcome_rules.json",
}

rules = {}

for name, url in rules_urls.items():
    response = requests.get(url)
    response.raise_for_status()
    rules[name] = response.json()

default_dic = rules["default_rules"]
contact_dic = rules["contact_rules"]
month_dic = rules["month_rules"]
poutcome_dic = rules["poutcome_rules"]
    
st.title("Will the customer take a credit?")

default_choice = st.selectbox("Does the customer have a credit at the moment?", list(default_dic.keys()))
contact_choice = st.selectbox("Contact type", list(contact_dic.keys()))
month_choice = st.selectbox("Month", list(month_dic.keys()))
duration = st.number_input("Call Duration (seconds)", min_value=0, max_value=5000, step=1)
pdays = st.number_input("Days since last campaign", min_value=-1, max_value=999, step=1)
poutcome_choice = st.selectbox("Previous campaign result", list(poutcome_dic.keys()))
cons_price_idx = st.number_input("Consumer price index", min_value=90.0, max_value=95.0, step=0.1)
euribor3m = st.number_input("EURIBOR 3-month rate", min_value=0.0, max_value=10.0, step=0.1)

row = [[
    default_dic[default_choice],
    contact_dic[contact_choice],
    month_dic[month_choice],
    duration,
    pdays,
    poutcome_dic[poutcome_choice],
    cons_price_idx,
    euribor3m
]]

if st.button("🔮 Predict"):
    prediction = model.predict(row)[0]
    result = "✅ The customer WILL take the credit" if prediction == 1 else "❌ The customer WILL NOT take the credit"
    st.subheader(result)