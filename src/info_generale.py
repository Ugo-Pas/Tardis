##
## EPITECH PROJECT, 2026
## info_general
## File description:
## info_generale
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

from src.tools import * 

def render(df):
	st.write("## Page G")
	YEARS = get_def_years(df)
	years = st.selectbox("Choisis l'année",YEARS,)
	if years == 'All':
		st.write("Graphe all year") #! In progresse
	else:
		one_year_old_Garph(years, df)
		train_cancel_one_year(years, df)
	map_delay_3d(years, df)