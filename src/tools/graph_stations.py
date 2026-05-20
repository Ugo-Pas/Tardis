##
## EPITECH PROJECT, 2026
## tools
## File description:
## tools
##

import matplotlib.pyplot as pl  # matplotlib to create visualisation via graphs
import streamlit as st


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
        year_str = (
            f"durant {year[0] if len(year) == 1 else str(year)}"
            if year
            else "toutes les années"
        )
        departure_str = departure if departure else "toutes les gares de départ"
        arrival_str = arrival if arrival else "toutes les gares d'arrivée"
        print(f"Aucune donnee pour {departure_str} -> {arrival_str} {year_str}.")
        st.write(
            "Aucune donnee pour", departure_str, "->", arrival_str, " ", year_str, "."
        )
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
        total_trains_col = next(
            (
                col
                for col in [
                    "Number of trains",
                    "Number of planned trains",
                    "Number of scheduled trains",
                    "Total trains",
                ]
                if col in filtered.columns
            ),
            None,
        )

        cancelled_total = filtered[target_col].fillna(0).sum()
        if total_trains_col is not None:
            total_trains = filtered[total_trains_col].fillna(0).sum()
            ratio = (cancelled_total / total_trains * 100) if total_trains else 0
            st.info(
                f"Trains annulés: {int(cancelled_total)} / {int(total_trains)} ({ratio:.2f}%)",
                icon="ℹ️",
            )
        else:
            st.info(
                f"Trains annulés (total): {int(cancelled_total)}",
                icon="ℹ️",
            )


def graph_departure_arrival_station_delay(df, departure=None, arrival=None, year=None):
    departure_col = "Departure station"
    arrival_col = "Arrival station"
    target_col = "Average delay of all trains at arrival"

    if target_col not in df.columns:
        st.write("Aucune colonne de retard moyen n'a ete trouvee.")
        return

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
        year_str = (
            f"durant {year[0] if len(year) == 1 else str(year)}"
            if year
            else "toutes les années"
        )
        departure_str = departure if departure else "toutes les gares de depart"
        arrival_str = arrival if arrival else "toutes les gares d'arrivee"
        st.write(
            "Aucune donnee de retard pour",
            departure_str,
            "->",
            arrival_str,
            " ",
            year_str,
            ".",
        )
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
            label=f"Moyenne: {mean_value:.2f} min",
        )

        # Build title
        title_parts = ["Retard moyen par mois"]

        if departure or arrival:
            title_parts.append(f" ({departure} -> {arrival})")

        if year:
            year_str = f"{year[0]}" if len(year) == 1 else f"{year[0]} a {year[-1]}"
            title_parts.append(f", {year_str}")

        ax.set_title("".join(title_parts))
        ax.set_xlabel("Date")
        ax.set_ylabel("Retard moyen (minutes)")
        ax.legend()
        ax.grid(alpha=0.25)
        pl.tight_layout()
        st.pyplot(fig)

        delay_mean = filtered[target_col].dropna().mean()
        if delay_mean == delay_mean:
            st.info(
                f"Retard moyen: {delay_mean:.2f} min",
                icon="ℹ️",
            )
