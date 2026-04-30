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
from src.accueil import render as render_accueil

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
    def _read_dataset(path):
        # Try common separators and fall back to Python engine sniffing
        for sep in (';', ',', '\t'):
            try:
                d = pd.read_csv(path, sep=sep, on_bad_lines="skip")
            except Exception:
                continue
            if 'Date' in d.columns:
                return d
        # Fallback: let pandas try to infer with the python engine
        return pd.read_csv(path, sep=None, engine='python', on_bad_lines="skip")

    raw_df = _read_dataset(DATASET)
    df = raw_df.drop_duplicates(ignore_index=True)

    # Normalize column names and drop unnamed index columns
    df.columns = [str(c).strip() for c in df.columns]
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed") or c == ""]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    for col in COLUMNS_TO_NUMERIC:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors="coerce")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m", errors="coerce").dt.to_period("M")

    with st.sidebar:
        selected_page = st.radio(
            "Navigation",
            ["🏠 Home", "🌐 Info generale", "👤 Info utilisateur"],
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

    if selected_page == "🌐 Info generale":
        render_info_generale(df)
    elif selected_page == "👤 Info utilisateur":
        render_info_utilisateur(df)
    else:
        render_accueil(df)

def convert_for_download(df):
    return df.to_csv().encode("utf-8")

main()