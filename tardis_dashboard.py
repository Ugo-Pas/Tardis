

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib as pl # matplotlib to create visualisation via graphs
import streamlit as st

DATASET = "dataset.csv" 

COLUMNS_TO_NUMERIC = ['Average journey time', 'Number of scheduled trains', 'Number of cancelled trains', 'Number of trains delayed at departure', 
                      'Average delay of late trains at departure', 'Average delay of all trains at departure', 'Number of trains delayed at arrival',
                      'Average delay of late trains at arrival', 'Average delay of all trains at arrival', 'Number of trains delayed > 15min', 
                      'Average delay of trains > 15min (if competing with flights)', 'Number of trains delayed > 30min',
                      'Number of trains delayed > 60min', 'Pct delay due to external causes', 'Pct delay due to infrastructure',
                      'Pct delay due to traffic management', 'Pct delay due to rolling stock', 
                      'Pct delay due to station management and equipment reuse', 
                      'Pct delay due to passenger handling (crowding, disabled persons, connections)']

raw_df = pd.read_csv(DATASET, on_bad_lines="skip", sep=";")

df = raw_df.drop_duplicates(ignore_index=True) # df is the result of the action of removing rows

for col in COLUMNS_TO_NUMERIC: # COLUMNS_TO_NUMERIC is a list of the columns we have to change
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors="coerce") # we transform "str" value to numeric

df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m", errors="coerce").dt.to_period("M")

df[COLUMNS_TO_NUMERIC] = df[COLUMNS_TO_NUMERIC].interpolate()


st.write("# hello world¡¡")

st.dataframe(df)
title = st.text_input("Movie title", "ou voulez vous aller")

st.write("gare d'arriver :", title)