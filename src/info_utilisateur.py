##
## EPITECH PROJECT, 2026
## info_utilisateur
## File description:
## info_utilisateur
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re
from src.tools import *


def render(df, departure_station, arrival_station, year):
	st.markdown("<h1 style='text-align: center;'>Info utilisateur</h1>", unsafe_allow_html=True)
	graph_departure_arrival_station(df, departure_station, arrival_station, year)