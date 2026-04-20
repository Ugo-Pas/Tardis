
import pandas as pd 
import matplotlib as pl 
import streamlit as st

st.write("# hello world¡¡")

def selecte_box_station(df:list, messager:str):
    a = df['Departure station'].unique().dropna()
    gare = []
    for station in a:
        gare.append(station)
    option = st.selectbox(messager, gare,)
    return option
