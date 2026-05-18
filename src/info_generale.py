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

def render(df, years):
	st.markdown("<h1 style='text-align: center;'>Info generale</h1>", unsafe_allow_html=True)
	if not years or (isinstance(years, (list, tuple)) and 'All' in years) or years == 'All':
		st.write("Graphe all year")
		one_year_old_Garph('All', df)
		train_cancel_one_year('All', df)
	else:
		one_year_old_Garph(years, df)
		train_cancel_one_year(years, df)
	map_delay_3d(years, df)