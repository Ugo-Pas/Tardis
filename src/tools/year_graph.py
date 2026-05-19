##
## EPITECH PROJECT, 2026
## tools
## File description:
## tools
##

import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import streamlit as st

def one_year_old_Garph(years, df:list):
    delay_col = "Average delay of all trains at arrival"

    # Support a single year, a list of years, or the special "All" value
    if years == "All" or (isinstance(years, (list, tuple)) and "All" in years):
        filtered = df[["Date", "Service", delay_col]].dropna()
    else:
        if not isinstance(years, (list, tuple)):
            years = [years]
        filtered = df.loc[
            df["Date"].dt.year.isin(years),
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
    title_year = "toutes les années" if (years == "All" or (isinstance(years, (list, tuple)) and "All" in years)) else (str(years) if isinstance(years, (list, tuple)) else str(years))
    ax.set_title(f"Retard moyen a l'arrivee par mois - {title_year}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Retard moyen (minutes)")
    ax.legend()
    ax.grid(alpha=0.25)
    pl.tight_layout()
    st.pyplot(fig)
