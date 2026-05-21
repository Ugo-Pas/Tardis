##
## EPITECH PROJECT, 2026
## tools
## File description:
## tools
##

import pandas as pd  # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import streamlit as st
import numpy as np


def graph_delay_causes_by_route(df, departure=None, arrival=None, year=None):
    departure_col = "Departure station"
    arrival_col = "Arrival station"
    # name cols for pct delay 
    cause_cols = [
        "Pct delay due to external causes",
        "Pct delay due to infrastructure",
        "Pct delay due to traffic management",
        "Pct delay due to rolling stock",
        "Pct delay due to station management and equipment reuse",
        "Pct delay due to passenger handling (crowding, disabled persons, connections)",
    ]
    if year == []:
        return st.error("Aucune année n'a été sélectionnée", icon="🚨")
    filtered = df.copy()
# get cols which stations
    if year is not None:
        years = year if isinstance(year, (list, tuple, np.ndarray)) else [year]
        if "All" not in years:
            filtered = filtered[filtered["Date"].dt.year.isin(years)]
    if departure not in (None, "Toute direction"):
        filtered = filtered[filtered[departure_col] == departure]
    if arrival not in (None, "Toute direction"):
        filtered = filtered[filtered[arrival_col] == arrival]

    available_cause_cols = [col for col in cause_cols if col in filtered.columns]
    if not available_cause_cols:
        st.warning(
            "Aucune colonne de pourcentage des causes de retard n'a été trouvée."
        )
        return

    for col in available_cause_cols:
        filtered[col] = pd.to_numeric(
            filtered[col].astype(str).str.replace(",", "."), errors="coerce"
        )

    cause_pct = (
        filtered[available_cause_cols]
        .dropna(how="all")
        .mean()
        .sort_values(ascending=False)
    )

    if cause_pct.empty:
        st.info("Aucune donnée disponible pour cette combinaison de filtres.")
        return

    labels = {
        "Pct delay due to external causes": "Causes externes",
        "Pct delay due to infrastructure": "Infrastructure",
        "Pct delay due to traffic management": "Gestion du trafic",
        "Pct delay due to rolling stock": "Materiel roulant",
        "Pct delay due to station management and equipment reuse": "Gestion en gare",
        "Pct delay due to passenger handling (crowding, disabled persons, connections)": "Gestion voyageurs",
    }

    pretty_index = [labels.get(col, col) for col in cause_pct.index]
#creat grapph 
    fig, ax = pl.subplots(figsize=(10, 5))
    bars = ax.barh(pretty_index, cause_pct.values, color="tab:blue", alpha=0.9)
    ax.invert_yaxis()

    for bar, value in zip(bars, cause_pct.values):
        ax.text(
            value + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            fontsize=9,
        )

    departure_str = (
        departure if departure not in (None, "Toute direction") else "Toutes les gares"
    )
    arrival_str = (
        arrival if arrival not in (None, "Toute direction") else "Toutes les gares"
    )

    if year is None or (isinstance(year, (list, tuple, np.ndarray)) and "All" in year):
        year_str = "toutes les années"
    else:
        years = year if isinstance(year, (list, tuple, np.ndarray)) else [year]
        year_str = str(years[0]) if len(years) == 1 else f"{min(years)} à {max(years)}"

    ax.set_title(
        f"Répartition des causes de retard (%)\n{departure_str} -> {arrival_str} ({year_str})"
    )
    ax.set_xlabel("Pourcentage moyen (%)")
    ax.set_ylabel("Cause du retard")
    ax.grid(axis="x", alpha=0.25)
    pl.tight_layout()

    st.pyplot(fig)
    # légende
    st.markdown(
        """
**Légende des causes**
- Causes externes: météo, incidents externes
- Infrastructure: voies, signaux
- Gestion du trafic: régulation des circulations
- Matériel roulant: panne ou indisponibilité du train
- Gestion en gare: organisation et équipements en gare
- Gestion voyageurs: affluence, assistance, correspondances
        """
    )
