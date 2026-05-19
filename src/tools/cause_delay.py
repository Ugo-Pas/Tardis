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

def graph_delay_causes_by_route(df, departure=None, arrival=None, year=None):
    departure_col = "Departure station"
    arrival_col = "Arrival station"
    cause_cols = [
        "Pct delay due to external causes",
        "Pct delay due to infrastructure",
        "Pct delay due to traffic management",
        "Pct delay due to rolling stock",
        "Pct delay due to station management and equipment reuse",
        "Pct delay due to passenger handling (crowding, disabled persons, connections)",
    ]

    filtered = df.copy()

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
        st.warning("Aucune colonne de pourcentage des causes de retard n'a ete trouvee.")
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
        st.info("Aucune donnee disponible pour cette combinaison de filtres.")
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

    # Graphique radar
    fig, ax = pl.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Préparation des données pour le graphique radar
    angles = np.linspace(0, 2 * np.pi, len(pretty_index), endpoint=False).tolist()
    values = cause_pct.values.tolist()
    
    # Fermer le graphique en répétant le premier point
    angles += angles[:1]
    values += values[:1]
    
    # Tracer le graphique radar
    ax.plot(angles, values, 'o-', linewidth=2, color="tab:blue", label="Causes")
    ax.fill(angles, values, alpha=0.25, color="tab:blue")
    
    # Configuration des angles
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(pretty_index, size=10)
    
    # Configuration de l'axe radial
    ax.set_ylim(0, max(values))
    ax.grid(True, alpha=0.25)

    departure_str = departure if departure not in (None, "Toute direction") else "Toutes gares"
    arrival_str = arrival if arrival not in (None, "Toute direction") else "Toutes gares"

    if year is None or (isinstance(year, (list, tuple, np.ndarray)) and "All" in year):
        year_str = "toutes les annees"
    else:
        years = year if isinstance(year, (list, tuple, np.ndarray)) else [year]
        year_str = str(years[0]) if len(years) == 1 else f"{min(years)} a {max(years)}"

    ax.set_title(
        f"Répartition des causes de retard\n{departure_str} -> {arrival_str} ({year_str})\nValeurs en Pourcentage (%)",
        pad=20, fontsize=12, fontweight='bold'
    )
    pl.tight_layout()

    st.pyplot(fig)

    st.markdown(
        """
**Legende des causes**
- Causes externes: meteo, incidents externes
- Infrastructure: voies, signaux
- Gestion du trafic: regulation des circulations
- Materiel roulant: panne ou indisponibilite du train
- Gestion en gare: organisation et equipements en gare
- Gestion voyageurs: affluence, assistance, correspondances
        """
    )
