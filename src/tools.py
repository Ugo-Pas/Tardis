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
    return ['All'] + years

def one_year_old_Garph(year, df:list):
    delay_col = "Average delay of all trains at arrival"

    filtered = df.loc[
        df["Date"].dt.year == year,
        ["Date", "Service", delay_col]
    ].dropna()
    monthly_delay_by_service = (
        filtered
        .groupby(["Date", "Service"], as_index=False)[delay_col]
        .mean()
        .pivot(index="Date", columns="Service", values=delay_col)
    )
    fig, ax = pl.subplots(figsize=(10, 5))
    if "National" in monthly_delay_by_service.columns:
        ax.plot(
            monthly_delay_by_service.index.to_timestamp(),
            monthly_delay_by_service["National"],
            label="National",
            color="tab:blue",
            linewidth=2
        )
    if "International" in monthly_delay_by_service.columns:
        ax.plot(
            monthly_delay_by_service.index.to_timestamp(),
            monthly_delay_by_service["International"],
            label="International",
            color="tab:orange",
            linewidth=2
        )
    ax.set_title(f"Retard moyen a l'arrivee par mois - {year}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Retard moyen (minutes)")
    ax.legend()
    ax.grid(alpha=0.25)
    pl.tight_layout()
    st.pyplot(fig)

def train_cancel_one_year(years, df:list):
    delay_col = "Number of cancelled trains"
    monthly_delay = ( 
        df.loc[df["Date"].dt.year == years, ["Date", delay_col]]
        .dropna()
        .sort_values("Date")
        .groupby("Date", as_index=False)[delay_col]
        .mean()
    )
    fig, ax = pl.subplots(figsize=(10, 5))
    ax.plot(
        monthly_delay["Date"].dt.to_timestamp(),
        monthly_delay[delay_col],
        color="tab:blue",
        linewidth=2
    )
    mean_delay = monthly_delay[delay_col].mean()
    ax.axhline(mean_delay, color="tab:red", linestyle="--", linewidth=1.8,
            label=f"Moyenne globale: {mean_delay:.2f} trains")
    ax.set_title("Nombre de train annulé par mois")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre de train annulé")
    ax.legend()
    ax.grid(alpha=0.25)
    pl.tight_layout()
    st.pyplot(fig)

def map_delay_3d(year, df):
    station_coords = pd.DataFrame(
        [
            {"Departure station": "Paris Lyon", "lat": 48.8443, "lon": 2.3730},
            {"Departure station": "Paris Montparnasse", "lat": 48.8414, "lon": 2.3207},
            {"Departure station": "Paris Est", "lat": 48.8769, "lon": 2.3594},
            {"Departure station": "Paris Nord", "lat": 48.8809, "lon": 2.3553},
            {"Departure station": "Lyon Part Dieu", "lat": 45.7606, "lon": 4.8611},
            {"Departure station": "Marseille Saint Charles", "lat": 43.3020, "lon": 5.3810},
            {"Departure station": "Bordeaux Saint Jean", "lat": 44.8253, "lon": -0.5563},
            {"Departure station": "Lille", "lat": 50.6364, "lon": 3.0635},
            {"Departure station": "Nantes", "lat": 47.2161, "lon": -1.5423},
            {"Departure station": "Rennes", "lat": 48.1035, "lon": -1.6724},
            {"Departure station": "Le Mans", "lat": 48.0061, "lon": 0.1996},
            {"Departure station": "Poitiers", "lat": 46.5802, "lon": 0.3404},
            {"Departure station": "Toulouse Matabiau", "lat": 43.6117, "lon": 1.4537},
            {"Departure station": "Toulon", "lat": 43.1250, "lon": 5.9300},
            {"Departure station": "Dijon", "lat": 47.3220, "lon": 5.0280},
            {"Departure station": "Metz", "lat": 49.1098, "lon": 6.1781},
            {"Departure station": "Strasbourg", "lat": 48.5857, "lon": 7.7359},
            {"Departure station": "Nice Ville", "lat": 43.7042, "lon": 7.2619},
            {"Departure station": "Montpellier Saint Roch", "lat": 43.6047, "lon": 3.8790},
            {"Departure station": "Angers Saint Laud", "lat": 47.4660, "lon": -0.5560},
            {"Departure station": "Avignon Tgv", "lat": 43.9230, "lon": 4.7860},
            {"Departure station": "Aix En Provence Tgv", "lat": 43.4555, "lon": 5.3182},
            {"Departure station": "St Pierre Des Corps", "lat": 47.3865, "lon": 0.7411},
            {"Departure station": "La Rochelle Ville", "lat": 46.1567, "lon": -1.1525},
            {"Departure station": "Barcelona", "lat": 41.3874, "lon": 2.1686},
            {"Departure station": "Bellegarde (Ain)", "lat": 46.1085, "lon": 5.8230},
            {"Departure station": "Chambery Challes Les Eaux", "lat": 45.5710, "lon": 5.9190},
            {"Departure station": "Dijon Ville", "lat": 47.3230, "lon": 5.0270},
            {"Departure station": "Francfort", "lat": 50.1072, "lon": 8.6638},
            {"Departure station": "Geneve", "lat": 46.2044, "lon": 6.1432},
            {"Departure station": "Italie", "lat": 45.4642, "lon": 9.1900},
            {"Departure station": "Lausanne", "lat": 46.5197, "lon": 6.6323},
            {"Departure station": "Macon Loche", "lat": 46.2696, "lon": 4.7819},
            {"Departure station": "Madrid", "lat": 40.4168, "lon": -3.7038},
            {"Departure station": "Mulhouse Ville", "lat": 47.7429, "lon": 7.3439},
            {"Departure station": "Stuttgart", "lat": 48.7833, "lon": 9.1833},
            {"Departure station": "Zurich", "lat": 47.3769, "lon": 8.5417},
        ]
    )
    delay_col = "Average delay of all trains at departure"
    if year == "All":
        filtered_df = df.copy()
        map_title = "Retard moyen par gare - toutes les années"
    else:
        filtered_df = df.loc[df["Date"].dt.year == year].copy()
        map_title = f"Retard moyen par gare - {year}"
    filtered_df[delay_col] = pd.to_numeric(
        filtered_df[delay_col].astype(str).str.replace(',', '.'),
        errors="coerce",
    )
    filtered_df["Number of scheduled trains"] = pd.to_numeric(
        filtered_df["Number of scheduled trains"].astype(str).str.replace(',', '.'),
        errors="coerce",
    )
    delay_by_station = (
        filtered_df.groupby("Departure station", as_index=False)[delay_col]
        .mean()
        .rename(columns={delay_col: "delay"})
    )
    route_by_station = (
        filtered_df.groupby(["Departure station", "Arrival station"], as_index=False)["Number of scheduled trains"]
        .sum()
        .rename(columns={"Number of scheduled trains": "trains"})
    )
    map_df = (
        delay_by_station.merge(station_coords, on="Departure station", how="inner")
        .sort_values("delay", ascending=False)
    )
    map_df["tooltip_title"] = map_df["Departure station"]
    map_df["tooltip_value"] = map_df["delay"].apply(
        lambda value: f"{format_minutes_as_duration(value)} de retard moyen"
    )
    route_df = (
        route_by_station
        .merge(station_coords.rename(columns={"Departure station": "Departure station", "lat": "source_lat", "lon": "source_lon"}), on="Departure station", how="inner")
        .merge(station_coords.rename(columns={"Departure station": "Arrival station", "lat": "target_lat", "lon": "target_lon"}), on="Arrival station", how="inner")
    )
    route_df["tooltip_title"] = route_df["Departure station"] + " -> " + route_df["Arrival station"]
    route_df["tooltip_value"] = route_df["trains"].round(0).astype("Int64").astype(str) + " trains programmés"
    if not route_df.empty:
        route_min = route_df["trains"].min()
        route_max = route_df["trains"].max()
        def route_color(value):
            if route_max == route_min:
                ratio = 1.0
            else:
                ratio = (value - route_min) / (route_max - route_min)
            red = int(100 + 120 * ratio)
            green = int(190 - 90 * ratio)
            blue = int(230 - 140 * ratio)
            return [red, green, blue, 120]
        route_df["color"] = route_df["trains"].apply(route_color)
        route_df["line_width"] = route_df["trains"].apply(
            lambda value: 1.0 if route_max == route_min else (1.0 + 3.0 * (value - route_min) / (route_max - route_min))
        )
        route_df["source_position"] = route_df.apply(lambda row: [row["source_lon"], row["source_lat"]], axis=1)
        route_df["target_position"] = route_df.apply(lambda row: [row["target_lon"], row["target_lat"]], axis=1)
    st.subheader(map_title)
    if map_df.empty:
        st.info("Aucune gare n'a pu être affichée avec des coordonnées disponibles.")
        return
    if len(map_df) < len(delay_by_station):
        st.caption(f"{len(map_df)} gares affichées avec coordonnées sur {len(delay_by_station)} gares agrégées.")
    if route_df.empty:
        st.caption("Aucun trajet n'a pu être tracé avec les coordonnées disponibles.")
    elif len(route_df) < len(route_by_station):
        st.caption(f"{len(route_df)} trajets affichés avec coordonnées sur {len(route_by_station)} trajets agrégés.")
    view_state = pdk.ViewState(
        latitude=46.8,
        longitude=3.0,
        zoom=4.6,
        pitch=38,
        bearing=0,
    )
    deck = pdk.Deck(
        map_style=None,
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                "ArcLayer",
                data=route_df,
                get_source_position="source_position",
                get_target_position="target_position",
                get_source_color="color",
                get_target_color="color",
                get_width="line_width",
                width_scale=1,
                width_min_pixels=1,
                width_max_pixels=5,
                pickable=True,
                auto_highlight=True,
            ),
            pdk.Layer(
                "ColumnLayer",
                data=map_df,
                get_position="[lon, lat]",
                get_elevation="delay",
                elevation_scale=1200,
                radius=9000,
                extruded=True,
                pickable=True,
                auto_highlight=True,
                get_fill_color="[220, 120, 70, 120]",
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position="[lon, lat]",
                get_radius=4500,
                get_fill_color="[40, 40, 40, 120]",
            ),
        ],
        tooltip={"text": "{tooltip_title}\n{tooltip_value}"},
    )

    st.pydeck_chart(deck)
    st.dataframe(map_df[["Departure station", "delay"]].reset_index(drop=True))
