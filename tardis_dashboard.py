
import pandas as pd 
import matplotlib as pl 
import streamlit as st

st.write("# hello world¡¡")

def selecte_box_station(df:list, messager:str):
    if 'Departure station' not in df.columns:
        st.warning("La colonne 'Departure station' est absente.")
        return None

    stations = sorted(df['Departure station'].dropna().unique().tolist())
    if not stations:
        st.warning("Aucune gare disponible.")
        return None

    option = st.selectbox(messager, stations)
    return option
