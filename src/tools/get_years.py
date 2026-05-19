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

def get_def_years(df):
    # Find a column that looks like a date
    date_col = None
    for c in df.columns:
        if isinstance(c, str) and 'date' in c.strip().lower():
            date_col = c
            break
    if date_col is None:
        return ['All']

    series = df[date_col]
    # Ensure we have a PeriodIndex-like series
    if not (pd.api.types.is_period_dtype(series) or pd.api.types.is_datetime64_any_dtype(series)):
        series = pd.to_datetime(series.astype(str), format="%Y-%m", errors="coerce").dt.to_period("M")

    years = sorted({int(p.year) for p in series.dropna().unique()})
    return years