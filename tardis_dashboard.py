import streamlit as st
import pandas as pd

DATASET = "dataset.csv"

raw_df = pd.read_csv(DATASET, on_bad_lines="skip", sep=";")
st.write("# hello world¡¡")

st.dataframe(raw_df)