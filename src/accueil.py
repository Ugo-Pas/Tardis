##
## EPITECH PROJECT, 2026
## acceuil 
## File description:
## acceuil
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

def render(df):
    st.title("Tardis")