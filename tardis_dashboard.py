##
## EPITECH PROJECT, 2026
## tardis_dashboard
## File description:
## tardis_dashboard
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

from src.info_generale import render as render_info_generale
from src.info_utilisateur import render as render_info_utilisateur

DATASET = "cleaned_dataset.csv" 

COLUMNS_TO_NUMERIC = ['Average journey time', 'Number of scheduled trains', 'Number of cancelled trains', 'Number of trains delayed at departure', 
                      'Average delay of late trains at departure', 'Average delay of all trains at departure', 'Number of trains delayed at arrival',
                      'Average delay of late trains at arrival', 'Average delay of all trains at arrival', 'Number of trains delayed > 15min', 
                      'Average delay of trains > 15min (if competing with flights)', 'Number of trains delayed > 30min',
                      'Number of trains delayed > 60min', 'Pct delay due to external causes', 'Pct delay due to infrastructure',
                      'Pct delay due to traffic management', 'Pct delay due to rolling stock', 
                      'Pct delay due to station management and equipment reuse', 
                      'Pct delay due to passenger handling (crowding, disabled persons, connections)']

type dataframe = pd.DataFrame



def main():
    df = pd.read_csv(DATASET, on_bad_lines="skip", sep=";")

    with st.sidebar:
        selected_page = st.radio(
            "Navigation",
            ["🏠 Home", "1️⃣ Page 1", "2️⃣ Page 2"],
            index=0,
        )
        csv = convert_for_download(df)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    if selected_page == "1️⃣ Page 1":
        render_info_generale()
    elif selected_page == "2️⃣ Page 2":
        render_info_utilisateur()
    else:
        st.write("## Tardis")

def convert_for_download(df):
    return df.to_csv().encode("utf-8")

main()