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
    return years

def render_executive_summary(df):
    """Affiche un résumé exécutif avec métriques clés et tendances"""
    
    # Préparation des données
    df_clean = df.copy()
    df_clean["Number of scheduled trains"] = pd.to_numeric(
        df_clean["Number of scheduled trains"].astype(str).str.replace(',', '.'), 
        errors="coerce"
    )
    
    # Vérifier si la colonne "Number of cancelled trains" existe
    if "Number of cancelled trains" in df_clean.columns:
        df_clean["Number of cancelled trains"] = pd.to_numeric(
            df_clean["Number of cancelled trains"].astype(str).str.replace(',', '.'), 
            errors="coerce"
        )
        has_cancelled_data = True
    else:
        has_cancelled_data = False
    
    df_clean["Average delay of all trains at arrival"] = pd.to_numeric(
        df_clean["Average delay of all trains at arrival"].astype(str).str.replace(',', '.'), 
        errors="coerce"
    )
    
    # Métriques clés globales
    st.markdown("## 📊 Résumé Exécutif")
    
    total_trains = df_clean["Number of scheduled trains"].sum()
    total_cancelled = df_clean["Number of cancelled trains"].sum() if has_cancelled_data else 0
    cancelled_pct = (total_cancelled / total_trains * 100) if (total_trains > 0 and has_cancelled_data) else 0
    avg_delay = df_clean["Average delay of all trains at arrival"].mean()
    
    # Affichage des cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📋 Nombre total de trains",
            value=f"{int(total_trains):,}",
            delta=None
        )
    
    with col2:
        if has_cancelled_data:
            st.metric(
                label="❌ Pourcentage d'annulation",
                value=f"{cancelled_pct:.2f}%",
                delta=None
            )
        else:
            st.info("💡 Données d'annulation non disponibles")
    
    with col3:
        st.metric(
            label="⏱️ Retard moyen global",
            value=format_minutes_as_duration(avg_delay),
            delta=None
        )
    
    st.divider()
    
    # KPIs par année avec tendances
    st.markdown("### 📈 Tendances par année")
    
    if "Date" in df_clean.columns:
        agg_dict = {
            "Number of scheduled trains": "sum",
            "Average delay of all trains at arrival": "mean"
        }
        if has_cancelled_data:
            agg_dict["Number of cancelled trains"] = "sum"
        
        yearly_stats = df_clean.groupby(df_clean["Date"].dt.year).agg(agg_dict)
        
        # Calculer le taux d'annulation si les données existent
        if has_cancelled_data:
            yearly_stats["Taux annulation %"] = (
                yearly_stats["Number of cancelled trains"] / yearly_stats["Number of scheduled trains"] * 100
            )
        
        # Renommer les colonnes
        rename_dict = {
            "Number of scheduled trains": "Trains programmés",
            "Average delay of all trains at arrival": "Retard moyen"
        }
        if has_cancelled_data:
            rename_dict["Number of cancelled trains"] = "Trains annulés"
        
        yearly_stats = yearly_stats.rename(columns=rename_dict)
        
        yearly_view = yearly_stats.reset_index().rename(columns={"Date": "Année", "index": "Année"})
        yearly_view = yearly_view.rename(columns={yearly_view.columns[0]: "Année"})

        yearly_view["Évolution trains"] = yearly_view["Trains programmés"].pct_change().mul(100).round(1)
        yearly_view["Évolution retard"] = yearly_view["Retard moyen"].pct_change().mul(100).round(1)

        if has_cancelled_data:
            yearly_view["Évolution annulation"] = yearly_view["Taux annulation %"].pct_change().mul(100).round(1)

        display_cols = ["Année", "Trains programmés", "Retard moyen"]
        if has_cancelled_data:
            display_cols.append("Taux annulation %")
        display_cols += ["Évolution trains", "Évolution retard"]
        if has_cancelled_data:
            display_cols.append("Évolution annulation")

        yearly_display = yearly_view[display_cols].copy()
        yearly_display["Retard moyen"] = yearly_display["Retard moyen"].apply(format_minutes_as_duration)
        yearly_display["Évolution trains"] = yearly_display["Évolution trains"].apply(
            lambda value: "-" if pd.isna(value) else f"{value:+.1f}%"
        )
        yearly_display["Évolution retard"] = yearly_display["Évolution retard"].apply(
            lambda value: "-" if pd.isna(value) else f"{value:+.1f}%"
        )
        if has_cancelled_data:
            yearly_display["Taux annulation %"] = yearly_display["Taux annulation %"].round(2).astype(str) + "%"
            yearly_display["Évolution annulation"] = yearly_display["Évolution annulation"].apply(
                lambda value: "-" if pd.isna(value) else f"{value:+.1f}%"
            )

        st.dataframe(
            yearly_display,
            use_container_width=True,
            hide_index=True,
        )
    
    st.divider()
    
    # Évolution du nombre de trains
    st.markdown("### 📊 Évolution du nombre de trains")
    
    if "Date" in df_clean.columns:
        monthly_trains = df_clean.groupby("Date", as_index=False)["Number of scheduled trains"].sum().sort_values("Date")
        
        fig, ax = pl.subplots(figsize=(12, 5))
        ax.plot(
            monthly_trains["Date"].dt.to_timestamp(),
            monthly_trains["Number of scheduled trains"],
            color="tab:green",
            linewidth=2.5,
            marker="o",
            markersize=4,
            label="Nombre de trains"
        )
        
        # Ligne de tendance
        z = np.polyfit(range(len(monthly_trains)), monthly_trains["Number of scheduled trains"].values, 2)
        p = np.poly1d(z)
        ax.plot(
            monthly_trains["Date"].dt.to_timestamp(),
            p(range(len(monthly_trains))),
            "r--",
            linewidth=2,
            alpha=0.7,
            label="Tendance"
        )
        
        mean_trains = monthly_trains["Number of scheduled trains"].mean()
        ax.axhline(mean_trains, color="gray", linestyle=":", linewidth=1.5, alpha=0.6, label=f"Moyenne: {int(mean_trains):,}")
        
        ax.set_title("Évolution mensuelle du nombre de trains programmés", fontsize=12, fontweight='bold')
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre de trains")
        ax.legend(loc="best")
        ax.grid(True, alpha=0.25)
        pl.tight_layout()
        
        st.pyplot(fig)
        
        # Statistiques d'évolution
        first_value = monthly_trains["Number of scheduled trains"].iloc[0]
        last_value = monthly_trains["Number of scheduled trains"].iloc[-1]
        evolution = ((last_value - first_value) / first_value * 100) if first_value > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Trains min (mois)", f"{int(monthly_trains['Number of scheduled trains'].min()):,}")
        with col2:
            st.metric("Trains max (mois)", f"{int(monthly_trains['Number of scheduled trains'].max()):,}")
        with col3:
            trend_icon = "📈" if evolution > 0 else "📉"
            st.metric(f"Évolution globale {trend_icon}", f"{abs(evolution):.2f}%")

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

def train_cancel_one_year(years, df:list):
    delay_col = "Number of cancelled trains"
    # Support single year, list of years or "All"
    if years == "All" or (isinstance(years, (list, tuple)) and "All" in years):
        filtered = df[["Date", delay_col]].dropna()
    else:
        if not isinstance(years, (list, tuple)):
            years = [years]
        filtered = df.loc[df["Date"].dt.year.isin(years), ["Date", delay_col]].dropna()

    monthly_delay = (
        filtered
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
    years_title = "toutes les années" if (years == "All" or (isinstance(years, (list, tuple)) and "All" in years)) else (str(years) if isinstance(years, (list, tuple)) else str(years))
    ax.set_title(f"Nombre de train annulé par mois - {years_title}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre de train annulé")
    ax.legend()
    ax.grid(alpha=0.25)
    pl.tight_layout()
    st.pyplot(fig)

def map_delay_3d(years, df):
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
    # Support single year, list of years or "All"
    if years == "All" or (isinstance(years, (list, tuple)) and "All" in years):
        filtered_df = df.copy()
        map_title = "Retard moyen par gare - toutes les années"
    else:
        if not isinstance(years, (list, tuple)):
            years = [years]
        filtered_df = df.loc[df["Date"].dt.year.isin(years)].copy()
        map_title = f"Retard moyen par gare - {years}"
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

def graph_departure_arrival_station(df, departure=None, arrival=None, year=None):
    departure_col = "Departure station"
    arrival_col = "Arrival station"
    target_col = "Number of cancelled trains"

    # Start with all rows
    filtered = df.copy()
    
    # Apply year filter if provided
    if year is not None:
        if not isinstance(year, list):
            year = [year]
        filtered = filtered[filtered["Date"].dt.year.isin(year)]
    
    # Apply departure station filter if provided
    if departure is not None:
        filtered = filtered[filtered[departure_col] == departure]
    
    # Apply arrival station filter if provided
    if arrival is not None:
        filtered = filtered[filtered[arrival_col] == arrival]

    route_monthly = (
        filtered[["Date", target_col]]
        .dropna()
        .groupby("Date", as_index=False)[target_col]
        .mean()
        .sort_values("Date")
    )

    if route_monthly.empty:
        year_str = f"durant {year[0] if len(year) == 1 else str(year)}" if year else "toutes les années"
        departure_str = departure if departure else "toutes les gares de départ"
        arrival_str = arrival if arrival else "toutes les gares d'arrivée"
        print(f"Aucune donnee pour {departure_str} -> {arrival_str} {year_str}.")
        st.write("Aucune donnee pour", departure_str,"->", arrival_str, " ", year_str, ".")
    else:
        fig, ax = pl.subplots(figsize=(10, 5))
        ax.plot(
            route_monthly["Date"].dt.to_timestamp(),
            route_monthly[target_col],
            color="tab:blue",
            marker="o",
            linewidth=2,
        )

        mean_value = route_monthly[target_col].mean()
        ax.axhline(
            mean_value,
            color="tab:red",
            linestyle="--",
            linewidth=1.8,
            label=f"Moyenne: {mean_value:.2f}",
        )

        # Build title
        title_parts = [f"{target_col} par mois"]
        
        if departure or arrival:
            title_parts.append(f" ({departure} -> {arrival})")
        
        if year:
            year_str = f"{year[0]}" if len(year) == 1 else f"{year[0]} à {year[-1]}"
            title_parts.append(f", {year_str}")

        ax.set_title("".join(title_parts))
        ax.set_xlabel("Date")
        ax.set_ylabel(target_col)
        ax.legend()
        ax.grid(alpha=0.25)
        pl.tight_layout()
        st.pyplot(fig)
        st.write("Total line:", len(route_monthly))


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
