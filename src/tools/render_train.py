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

from .format_time import format_minutes_as_duration


def render_executive_summary(df):
    """Affiche un résumé exécutif avec métriques clés et tendances"""

    # Préparation des données
    df_clean = df.copy()
    df_clean["Number of scheduled trains"] = pd.to_numeric(
        df_clean["Number of scheduled trains"].astype(str).str.replace(",", "."),
        errors="coerce",
    )

    # Vérifier si la colonne "Number of cancelled trains" existe
    if "Number of cancelled trains" in df_clean.columns:
        df_clean["Number of cancelled trains"] = pd.to_numeric(
            df_clean["Number of cancelled trains"].astype(str).str.replace(",", "."),
            errors="coerce",
        )
        has_cancelled_data = True
    else:
        has_cancelled_data = False

    df_clean["Average delay of all trains at arrival"] = pd.to_numeric(
        df_clean["Average delay of all trains at arrival"]
        .astype(str)
        .str.replace(",", "."),
        errors="coerce",
    )

    # Métriques clés globales
    st.markdown("## 📊 Résumé Exécutif")

    total_trains = df_clean["Number of scheduled trains"].sum()
    total_cancelled = (
        df_clean["Number of cancelled trains"].sum() if has_cancelled_data else 0
    )
    cancelled_pct = (
        (total_cancelled / total_trains * 100)
        if (total_trains > 0 and has_cancelled_data)
        else 0
    )
    avg_delay = df_clean["Average delay of all trains at arrival"].mean()

    # Affichage des cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📋 Nombre total de trains",
            value=f"{int(total_trains):,}",
            delta=None,
        )

    with col2:
        if has_cancelled_data:
            st.metric(
                label="❌ Pourcentage d'annulation",
                value=f"{cancelled_pct:.2f}%",
                delta=None,
            )
        else:
            st.info("💡 Données d'annulation non disponibles")

    with col3:
        st.metric(
            label="⏱️ Retard moyen global",
            value=format_minutes_as_duration(avg_delay),
            delta=None,
        )

    st.divider()

    # KPIs par année avec tendances
    st.markdown("### 📈 Tendances par année")

    if "Date" in df_clean.columns:
        agg_dict = {
            "Number of scheduled trains": "sum",
            "Average delay of all trains at arrival": "mean",
        }
        if has_cancelled_data:
            agg_dict["Number of cancelled trains"] = "sum"

        yearly_stats = df_clean.groupby(df_clean["Date"].dt.year).agg(agg_dict)

        # Calculer le taux d'annulation si les données existent
        if has_cancelled_data:
            yearly_stats["Taux annulation %"] = (
                yearly_stats["Number of cancelled trains"]
                / yearly_stats["Number of scheduled trains"]
                * 100
            )

        # Renommer les colonnes
        rename_dict = {
            "Number of scheduled trains": "Trains programmés",
            "Average delay of all trains at arrival": "Retard moyen",
        }
        if has_cancelled_data:
            rename_dict["Number of cancelled trains"] = "Trains annulés"

        yearly_stats = yearly_stats.rename(columns=rename_dict)

        yearly_view = yearly_stats.reset_index().rename(
            columns={"Date": "Année", "index": "Année"}
        )
        yearly_view = yearly_view.rename(columns={yearly_view.columns[0]: "Année"})

        yearly_view["Évolution trains"] = (
            yearly_view["Trains programmés"].pct_change().mul(100).round(1)
        )
        yearly_view["Évolution retard"] = (
            yearly_view["Retard moyen"].pct_change().mul(100).round(1)
        )

        if has_cancelled_data:
            yearly_view["Évolution annulation"] = (
                yearly_view["Taux annulation %"].pct_change().mul(100).round(1)
            )

        display_cols = ["Année", "Trains programmés", "Retard moyen"]
        if has_cancelled_data:
            display_cols.append("Taux annulation %")
        display_cols += ["Évolution trains", "Évolution retard"]
        if has_cancelled_data:
            display_cols.append("Évolution annulation")

        yearly_display = yearly_view[display_cols].copy()
        yearly_display["Retard moyen"] = yearly_display["Retard moyen"].apply(
            format_minutes_as_duration
        )
        yearly_display["Évolution trains"] = yearly_display["Évolution trains"].apply(
            lambda value: "-" if pd.isna(value) else f"{value:+.1f}%"
        )
        yearly_display["Évolution retard"] = yearly_display["Évolution retard"].apply(
            lambda value: "-" if pd.isna(value) else f"{value:+.1f}%"
        )
        if has_cancelled_data:
            yearly_display["Taux annulation %"] = (
                yearly_display["Taux annulation %"].round(2).astype(str) + "%"
            )
            yearly_display["Évolution annulation"] = yearly_display[
                "Évolution annulation"
            ].apply(lambda value: "-" if pd.isna(value) else f"{value:+.1f}%")

        st.dataframe(
            yearly_display,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # Évolution du nombre de trains
    st.markdown("### 📊 Évolution du nombre de trains")

    if "Date" in df_clean.columns:
        monthly_trains = (
            df_clean.groupby("Date", as_index=False)["Number of scheduled trains"]
            .sum()
            .sort_values("Date")
        )

        fig, ax = pl.subplots(figsize=(12, 5))
        ax.plot(
            monthly_trains["Date"].dt.to_timestamp(),
            monthly_trains["Number of scheduled trains"],
            color="tab:green",
            linewidth=2.5,
            marker="o",
            markersize=4,
            label="Nombre de trains",
        )

        # Ligne de tendance
        z = np.polyfit(
            range(len(monthly_trains)),
            monthly_trains["Number of scheduled trains"].values,
            2,
        )
        p = np.poly1d(z)
        ax.plot(
            monthly_trains["Date"].dt.to_timestamp(),
            p(range(len(monthly_trains))),
            "r--",
            linewidth=2,
            alpha=0.7,
            label="Tendance",
        )

        mean_trains = monthly_trains["Number of scheduled trains"].mean()
        ax.axhline(
            mean_trains,
            color="gray",
            linestyle=":",
            linewidth=1.5,
            alpha=0.6,
            label=f"Moyenne: {int(mean_trains):,}",
        )

        ax.set_title(
            "Évolution mensuelle du nombre de trains programmés",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre de trains")
        ax.legend(loc="best")
        ax.grid(True, alpha=0.25)
        pl.tight_layout()

        st.pyplot(fig)

        # Statistiques d'évolution
        first_value = monthly_trains["Number of scheduled trains"].iloc[0]
        last_value = monthly_trains["Number of scheduled trains"].iloc[-1]
        evolution = (
            ((last_value - first_value) / first_value * 100) if first_value > 0 else 0
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Trains min (mois)",
                f"{int(monthly_trains['Number of scheduled trains'].min()):,}",
            )
        with col2:
            st.metric(
                "Trains max (mois)",
                f"{int(monthly_trains['Number of scheduled trains'].max()):,}",
            )
        with col3:
            trend_icon = "📈" if evolution > 0 else "📉"
            st.metric(f"Évolution globale {trend_icon}", f"{abs(evolution):.2f}%")
