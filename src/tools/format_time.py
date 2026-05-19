##
## EPITECH PROJECT, 2026
## tools
## File description:
## tools
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

def format_minutes_as_duration(minutes_value: float) -> str:
    if pd.isna(minutes_value):
        return "N/A"

    total_seconds = int(round(float(minutes_value) * 60))
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes} min {seconds:02d} s"