##
## EPITECH PROJECT, 2026
## tardis_dashboard
## File description:
## tardis_dashboard
##

import pandas as pd  # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re

from src.tools import get_def_years
from src.info_generale import render as render_info_generale
from src.info_utilisateur import render as render_info_utilisateur
from src.accueil import render as render_accueil
from src.screen_prediction import render as render_prédiction

DATASET = "cleaned_dataset.csv"

MONTHS = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]

COLUMNS_TO_NUMERIC = [
    "Average journey time",
    "Number of scheduled trains",
    "Number of cancelled trains",
    "Number of trains delayed at departure",
    "Average delay of late trains at departure",
    "Average delay of all trains at departure",
    "Number of trains delayed at arrival",
    "Average delay of late trains at arrival",
    "Average delay of all trains at arrival",
    "Number of trains delayed > 15min",
    "Average delay of trains > 15min (if competing with flights)",
    "Number of trains delayed > 30min",
    "Number of trains delayed > 60min",
    "Pct delay due to external causes",
    "Pct delay due to infrastructure",
    "Pct delay due to traffic management",
    "Pct delay due to rolling stock",
    "Pct delay due to station management and equipment reuse",
    "Pct delay due to passenger handling (crowding, disabled persons, connections)",
]

type dataframe = pd.DataFrame


def get_month_index(target, months) -> int:
    for i in range(len(months)):
        if target == months[i]:
            return i + 1
    return -1


def selectbox_prediction(years):
    month = st.selectbox(
        "Choisissez votre mois",
        MONTHS,
        index=None,
        placeholder="Choisissez votre mois",
    )
    index_month = get_month_index(month, MONTHS)
    year = st.number_input(
        "Choisissez votre année",
        min_value=0,
        max_value=3000,
        value=2024,
        step=1,
        format="%d",
    )
    vacance = st.toggle("Partez vous durant des vacances")
    weekend = st.toggle("Partez vous durant un week-end")
    int_vacance = 0
    int_weekend = 0
    if vacance:
        int_vacance = 1
    if weekend:
        int_weekend = 1
    return index_month, int(year), int_vacance, int_weekend


def selectbox_stations(df, selected_page):
    # selectbox pour le choix des gares
    df_departure_station = df.dropna(subset=["Departure station"])
    stations = df_departure_station["Departure station"].unique()

    departure_station = st.selectbox(
        "Gare de dapart:",
        stations,
        index=None,
        placeholder="Gare de depart",
    )
    # Adapter la liste des gares d'arrivée selon la gare de départ
    if departure_station == None:
        df_arrival_station = df.dropna(subset=["Arrival station"])
        arrival_stations = df_arrival_station["Arrival station"].unique()
    else:
        # Filtrer les gares d'arrivée selon la gare de départ sélectionnée
        df_filtered = df[df["Departure station"] == departure_station].dropna(
            subset=["Arrival station"]
        )
        arrival_stations = df_filtered["Arrival station"].unique()

    arrival_station = st.selectbox(
        "Gare d'arriver:",
        arrival_stations,
        index=None,
        placeholder="Gare d'arriver",
    )
    return departure_station, arrival_station


def main():
    def _read_dataset(path):
        for sep in (";", ",", "\t"):
            try:
                d = pd.read_csv(path, sep=sep, on_bad_lines="skip")
            except Exception:
                continue
            if "Date" in d.columns:
                return d
        return pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")

    raw_df = _read_dataset(DATASET)
    df = raw_df.drop_duplicates(ignore_index=True)

    # Normalize column names and drop unnamed index columns
    df.columns = [str(c).strip() for c in df.columns]
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed") or c == ""]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    for col in COLUMNS_TO_NUMERIC:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "."), errors="coerce"
            )

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"], format="%Y-%m", errors="coerce"
        ).dt.to_period("M")

    with st.sidebar:
        selected_page = st.radio(
            "Navigation",
            ["🏠 Home", "🌐 Info generale", "👤 Info utilisateur", "📈 Prédiction"],
            index=0,
        )
        YEARS = get_def_years(df)
        if selected_page != "📈 Prédiction":
            year = st.multiselect(
                "Quelle année choisissez-vous ?",
                YEARS,
                default=YEARS,
            )
        if selected_page == "👤 Info utilisateur" or selected_page == "📈 Prédiction":
            departure_station, arrival_station = selectbox_stations(df, selected_page)
        if selected_page == "📈 Prédiction":
            month, year, vacances, weekend = selectbox_prediction(YEARS)

    if selected_page == "🌐 Info generale":
        render_info_generale(df, year)
    elif selected_page == "👤 Info utilisateur":
        render_info_utilisateur(df, departure_station, arrival_station, year)
    elif selected_page == "📈 Prédiction":
        render_prédiction(
            df, departure_station, arrival_station, month, year, vacances, weekend
        )
    else:
        render_accueil(df)


def convert_for_download(df):
    return df.to_csv().encode("utf-8")


main()
