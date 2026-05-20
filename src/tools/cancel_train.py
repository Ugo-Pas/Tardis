##
## EPITECH PROJECT, 2026
## tools
## File description:
## tools
##

import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import streamlit as st


def train_cancel_one_year(years, df: list):
    delay_col = "Number of cancelled trains"
    # Support single year, list of years or "All"
    if years == "All" or (isinstance(years, (list, tuple)) and "All" in years):
        filtered = df[["Date", delay_col]].dropna()
    else:
        if not isinstance(years, (list, tuple)):
            years = [years]
        filtered = df.loc[df["Date"].dt.year.isin(years), ["Date", delay_col]].dropna()

    monthly_delay = (
        filtered.sort_values("Date").groupby("Date", as_index=False)[delay_col].mean()
    )
    fig, ax = pl.subplots(figsize=(10, 5))
    ax.plot(
        monthly_delay["Date"].dt.to_timestamp(),
        monthly_delay[delay_col],
        color="tab:blue",
        linewidth=2,
    )
    mean_delay = monthly_delay[delay_col].mean()
    ax.axhline(
        mean_delay,
        color="tab:red",
        linestyle="--",
        linewidth=1.8,
        label=f"Moyenne globale: {mean_delay:.2f} trains",
    )
    years_title = (
        "toutes les années"
        if (years == "All" or (isinstance(years, (list, tuple)) and "All" in years))
        else (str(years) if isinstance(years, (list, tuple)) else str(years))
    )
    ax.set_title(f"Nombre de train annulé par mois - {years_title}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre de train annulé")
    ax.legend()
    ax.grid(alpha=0.25)
    pl.tight_layout()
    st.pyplot(fig)
