##
## EPITECH PROJECT, 2026
## info_general
## File description:
## info_generale
##

import pandas as pd  # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

from src.tools import *


def render(df, years):
    st.markdown(
        "<h1 style='text-align: center;'>Info générale</h1>", unsafe_allow_html=True
    )
    st.divider()
    st.markdown("### Résumé exécutif")
    # Afficher le résumé exécutif
    render_executive_summary(df)
    st.divider()
    st.markdown("### Évolution des retards et des annulations")
    if (
        not years
        or (isinstance(years, (list, tuple)) and "All" in years)
        or years == "All"
    ):
        st.write("Graphique pour toutes les années")
        one_year_old_Garph("All", df)  # graph no need list of year
        train_cancel_one_year("All", df)
    else:
        one_year_old_Garph(years, df)  # graph need list of year
        train_cancel_one_year(years, df)
    st.divider()
    st.markdown("### Causes des retards")
    use_pie_chart = st.checkbox("Afficher en camembert", value=False)
    graph_delay_causes_by_route(df, None, None, years, use_pie_chart=use_pie_chart)
    st.divider()
    st.markdown("### Carte des retards")
    map_delay_3d(years, df)
