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


def render(df, departure_station, arrival_station, year):
    st.markdown(
        "<h1 style='text-align: center;'>Info utilisateur</h1>", unsafe_allow_html=True
    )
    st.divider()
    st.markdown(
        f"### Nombre de trains annulés sur le trajet {departure_station} -> {arrival_station}"
    )
    if departure_station == None and arrival_station == None:
        st.warning("Aucune station n'a été sélectionnée", icon="⚠️")
    graph_departure_arrival_station(df, departure_station, arrival_station, year)
    graph_departure_arrival_station_delay(df, departure_station, arrival_station, year)
    st.divider()
    st.markdown(
        f"### Causes des retards sur le trajet {departure_station} -> {arrival_station}"
    )
    use_pie_chart = st.checkbox("Afficher en camembert", value=False)
    graph_delay_causes_by_route(
        df, departure_station, arrival_station, year, use_pie_chart=use_pie_chart
    )
