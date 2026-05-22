##
## EPITECH PROJECT, 2026
## info_utilisateur
## File description:
## info_utilisateur
##

import joblib
import pandas as pd
import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import numpy as np
import pydeck as pdk
import re
import streamlit as st

from src.tools import *


def get_service_national(df, departure_station: str, arrival_station: str) -> int:
    departure_key = str(departure_station).strip().casefold()
    arrival_key = str(arrival_station).strip().casefold()
    filtered = df[
        df["Departure station"].astype(str).str.strip().str.casefold().eq(departure_key)
        & df["Arrival station"].astype(str).str.strip().str.casefold().eq(arrival_key)
    ]
    if filtered.empty:
        filtered = df[
            df["Departure station"]
            .astype(str)
            .str.strip()
            .str.casefold()
            .eq(arrival_key)
            & df["Arrival station"]
            .astype(str)
            .str.strip()
            .str.casefold()
            .eq(departure_key)
        ]
    if filtered.empty:
        return 1
    service = filtered.iloc[0]["Service"]
    return 1 if str(service).strip().casefold() == "national" else 0


def check_error(detparture, arrival, month):
    ret = 0
    if detparture == None:
        st.error("Aucune station de départ n'a été sélectionnée", icon="🚨")
        ret = -1
    if arrival == None:
        st.error("Aucune station d'arrivée n'a été sélectionnée", icon="🚨")
        ret = -1
    if month == -1:
        st.error("Aucun mois n'a été sélectionné", icon="🚨")
        ret = -1
    return ret


def model(
    model_file: str,
    departure: str,
    arrival: str,
    year: int,
    month: int,
    vacances: int,
    weekend: int,
    service_national: int,
):
    saved = joblib.load(model_file)
    model = saved["model"]
    model_columns = saved["columns"]
    data = {
        "month": month,
        "year": year,
        "day_of_week": weekend,
        "is_peak_month": vacances,
        "Service_National": service_national,
        departure: 1,
        arrival: 1,
    }
    X_input = pd.DataFrame([data], columns=model_columns).fillna(0)
    prediction = model.predict(X_input)
    return prediction[0]


def render(
    df,
    departure_station: str,
    arrival_station: str,
    month: int,
    year: int,
    vacances: int,
    weekend: int,
):
    st.markdown(
        "<h1 style='text-align: center;'>Prédiction</h1>", unsafe_allow_html=True
    )
    st.divider()
    left, middle, right = st.columns(3)
    if middle.button(
        "Lancer la prédiction", icon="📈", width="stretch", shortcut="Enter"
    ):
        if check_error(departure_station, arrival_station, month) == -1:
            return
        departure = "Departure station_" + departure_station
        arrival = "Arrival station_" + arrival_station
        service_national = get_service_national(df, departure_station, arrival_station)
        train_late = model(
            "model.pkl",
            departure,
            arrival,
            year,
            month,
            vacances,
            weekend,
            service_national,
        )
        pct_cancel = model(
            "src/Bonus/model_train_cancel.pkl",
            departure,
            arrival,
            year,
            month,
            vacances,
            weekend,
            service_national,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="📋 Nombre total de trains",
                value=f"in progress",
                delta=None,
            )
        with col2:
            if pct_cancel:
                st.metric(
                    label="❌ Pourcentage d'annulation",
                    value=f"{pct_cancel:.2f}%",
                    delta=None,
                )
            else:
                st.info("💡 Données d'annulation non disponibles")
        with col3:
            st.metric(
                label="⏱️ Retard moyen global",
                value=format_minutes_as_duration(train_late),
                delta=None,
            )
        st.divider()
        print(f"Retard prédit : {train_late:.1f} minutes")
        print(f"Pourcentage de chance qu'un train soit annulé : {pct_cancel:.1f} %")
