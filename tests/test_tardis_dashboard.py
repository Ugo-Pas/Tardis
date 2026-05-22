import itertools
import pandas as pd
import pytest

import tardis_dashboard as td


@pytest.mark.parametrize("month", td.MONTHS + ["Nonexistent"])
def test_get_month_index_param(month):
    idx = td.get_month_index(month, td.MONTHS)
    if month == "Nonexistent":
        assert idx == -1
    else:
        assert 1 <= idx <= 12


@pytest.mark.parametrize("month_index,month", list(enumerate(td.MONTHS, start=1)))
def test_selectbox_prediction_month_index(monkeypatch, month_index, month):
    # selectbox returns month, number_input returns 2025, toggles both False
    monkeypatch.setattr(td.st, "selectbox", lambda *a, **k: month)
    monkeypatch.setattr(td.st, "number_input", lambda *a, **k: 2025)
    toggles = iter([False, False])
    monkeypatch.setattr(td.st, "toggle", lambda *a, **k: next(toggles))

    idx, year, vac, weekend = td.selectbox_prediction(td.MONTHS)
    assert idx == month_index
    assert year == 2025
    assert vac == 0
    assert weekend == 0


# Exhaustive combos of toggles across several years to reach many tests
toggles_combos = list(itertools.product([0, 1], repeat=2))
years = [2023, 2024, 2025]
cases = [(v, w, y) for y in years for (v, w) in toggles_combos]


@pytest.mark.parametrize("vac,weekend,year", cases)
def test_selectbox_prediction_toggles(monkeypatch, vac, weekend, year):
    # use a known month
    month = td.MONTHS[0]
    monkeypatch.setattr(td.st, "selectbox", lambda *a, **k: month)
    monkeypatch.setattr(td.st, "number_input", lambda *a, **k: year)
    toggles = iter([bool(vac), bool(weekend)])
    monkeypatch.setattr(td.st, "toggle", lambda *a, **k: next(toggles))

    idx, y, v, w = td.selectbox_prediction(td.MONTHS)
    assert idx == 1
    assert y == year
    assert v == vac
    assert w == weekend


def test_convert_for_download_empty():
    df = pd.DataFrame()
    b = td.convert_for_download(df)
    assert isinstance(b, (bytes, bytearray))
    s = b.decode("utf-8")
    assert isinstance(s, str)


def test_convert_for_download_unicode():
    df = pd.DataFrame({"ville": ["Nîmes", "Montréal"], "retard": [5, 10]})
    b = td.convert_for_download(df)
    s = b.decode("utf-8")
    assert "Nîmes" in s and "Montréal" in s


def test_convert_for_download_large():
    df = pd.DataFrame({f"c{i}": range(100) for i in range(8)})
    b = td.convert_for_download(df)
    s = b.decode("utf-8")
    assert "c0" in s and "c7" in s


@pytest.mark.parametrize(
    "departures,arrivals,choice_dep,choice_arr",
    [
        (["A", "A", "B"], ["X", "Z", "Y"], "A", "Z"),
        (["S"], ["P"], "S", "P"),
        (["D", "D", "D"], ["C", "B", "A"], "D", "A"),
    ],
)
def test_selectbox_stations_various(
    monkeypatch, departures, arrivals, choice_dep, choice_arr
):
    df = pd.DataFrame({"Departure station": departures, "Arrival station": arrivals})
    choices = iter([choice_dep, choice_arr])

    captured = []

    def fake_selectbox(label, options=None, *a, **k):
        if options is not None:
            captured.append(list(options))
        return next(choices)

    monkeypatch.setattr(td.st, "selectbox", fake_selectbox)
    dep, arr = td.selectbox_stations(df, selected_page="any")
    assert dep == choice_dep
    assert arr == choice_arr
    assert any(isinstance(opts, list) and len(opts) >= 1 for opts in captured)


def test_selectbox_stations_none_departure(monkeypatch):
    df = pd.DataFrame({"Departure station": ["A", "B"], "Arrival station": ["X", "Y"]})
    choices = iter([None, "Y"])
    monkeypatch.setattr(td.st, "selectbox", lambda *a, **k: next(choices))
    dep, arr = td.selectbox_stations(df, selected_page="any")
    assert dep is None
    assert arr == "Y"


def test_prediction_input_padding(monkeypatch):
    # Ensure selectbox_prediction fills missing dummies by returning 0s when needed
    monkeypatch.setattr(td.st, "selectbox", lambda *a, **k: td.MONTHS[0])
    monkeypatch.setattr(td.st, "number_input", lambda *a, **k: 2030)
    toggles = iter([False, False])
    monkeypatch.setattr(td.st, "toggle", lambda *a, **k: next(toggles))

    idx, year, vac, weekend = td.selectbox_prediction(td.MONTHS)
    assert isinstance(idx, int)
    assert year == 2030
    assert vac == 0 and weekend == 0
