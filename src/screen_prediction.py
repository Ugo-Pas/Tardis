##
## EPITECH PROJECT, 2026
## info_utilisateur
## File description:
## info_utilisateur
##

import pandas as pd  # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re
from src.tools import *

import joblib
import pandas as pd

def model(model_file : str, departure : str, arrival : str, year : int, month : int):
    saved = joblib.load(model_file)
    model = saved["model"]
    model_columns = saved["columns"]
    data = {
        "month": month,
        "year": year,
        "day_of_week": 0,
        "is_peak_month": 0,
        "Service_National": 1,
        departure: 1,
        arrival: 1,
    }
    X_input = pd.DataFrame([data], columns=model_columns).fillna(0)
    prediction = model.predict(X_input)
    return prediction[0]

def render(df, departure_station : str, arrival_station : str, month : int, year : int):
    st.markdown(
        "<h1 style='text-align: center;'>Prédiction</h1>", unsafe_allow_html=True
    )
    st.divider()
    if departure_station != None and arrival_station != None and month != 84:
        departure = "Departure station_" + departure_station
        arrival = "Arrival station_" + arrival_station
        prediction =  model("model.pkl", departure, arrival, year, month)
        st.write(f"Retard prédit : {prediction:.1f} minutes")
        print(f"Retard prédit : {prediction:.1f} minutes")
