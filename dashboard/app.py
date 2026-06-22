"""Streamlit dashboard with three independent analysis modules."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from etl.config import get_settings
from etl.transform.common import parse_percent_series


st.set_page_config(page_title="Grupo 8 - Ciencias de Datos", layout="wide")


@st.cache_data(show_spinner=False)
def load_parquet(path: str) -> pd.DataFrame:
    """Load one processed Parquet file."""

    parquet_path = Path(path)
    if not parquet_path.exists():
        return pd.DataFrame()
    return pd.read_parquet(parquet_path)


def processed_file(dataset: str, filename: str) -> Path:
    """Build a processed dataset path."""

    return get_settings().processed_dir / dataset / filename


def show_empty_state() -> None:
    """Render a message when processed data is missing."""

    st.info("Ejecuta primero `python -m etl.extract.download_kaggle` y `python -m etl.transform.pipeline`.")


def pokemon_module() -> None:
    """Pokemon module focused on competitive attributes and usage."""

    pokemon = load_parquet(str(processed_file("pokemon", "df_pokemon.parquet")))
    teammates = load_parquet(str(processed_file("pokemon", "bridge_pokemon_pokemon_USED_IN_TEAM_WITH.parquet")))

    if pokemon.empty:
        show_empty_state()
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Pokemon registrados", f"{len(pokemon):,}")
    col2.metric("Generaciones", f"{pokemon['generation'].nunique():,}")
    col3.metric("Tipos primarios", f"{pokemon['type1'].nunique():,}")

    permitted = pokemon[pokemon.get("vgc2022_rules", "") == "Permitted"].copy()
    if "usage_percent_numeric" not in pokemon.columns and "usage_percent" in pokemon.columns:
        pokemon["usage_percent_numeric"] = parse_percent_series(pokemon["usage_percent"])

    ranked = pokemon.copy()
    if "usage_percent_numeric" in ranked.columns:
        ranked = ranked.dropna(subset=["usage_percent_numeric"]).sort_values(
            "usage_percent_numeric", ascending=False
        )

    left, right = st.columns(2)
    with left:
        type_counts = pokemon["type1"].value_counts().reset_index()
        type_counts.columns = ["tipo", "cantidad"]
        fig = px.bar(type_counts, x="tipo", y="cantidad", title="Distribucion por tipo primario")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.scatter(
            permitted,
            x="attack",
            y="speed",
            color="type1",
            hover_name="name",
            title="Ataque vs velocidad en Pokemon permitidos VGC 2022",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top uso competitivo")
    ranking_columns = [
        column
        for column in ["name", "type1", "type2", "total", "usage_percent_numeric", "monthly_rank"]
        if column in ranked.columns
    ]
    st.dataframe(ranked[ranking_columns].head(20), use_container_width=True)

    if not teammates.empty and "use_percentage_numeric" in teammates.columns:
        top_pairs = teammates.sort_values("use_percentage_numeric", ascending=False).head(15)
        fig = px.bar(
            top_pairs,
            x="use_percentage_numeric",
            y="teammate",
            color="pokemon",
            orientation="h",
            title="Combinaciones frecuentes de equipo",
        )
        st.plotly_chart(fig, use_container_width=True)


def earthquakes_module() -> None:
    """Earthquakes module focused on magnitude, depth and geography."""

    earthquakes = load_parquet(str(processed_file("earthquakes_chile", "seismic_data.parquet")))

    if earthquakes.empty:
        show_empty_state()
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Eventos", f"{len(earthquakes):,}")
    col2.metric("Magnitud maxima", f"{earthquakes['magnitude'].max():.1f}")
    col3.metric("Profundidad media", f"{earthquakes['depth'].mean():.1f} km")

    left, right = st.columns(2)
    with left:
        fig = px.histogram(earthquakes, x="magnitude", nbins=25, title="Distribucion de magnitudes")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.scatter(
            earthquakes,
            x="depth",
            y="magnitude",
            color="magnitude",
            hover_data=["date_utc", "latitude", "longitude"],
            title="Relacion entre profundidad y magnitud",
        )
        st.plotly_chart(fig, use_container_width=True)

    by_year = earthquakes.dropna(subset=["year"]).groupby("year", as_index=False).size()
    fig = px.line(by_year, x="year", y="size", markers=True, title="Eventos registrados por ano")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter_map(
        earthquakes,
        lat="latitude",
        lon="longitude",
        color="magnitude",
        size="magnitude",
        hover_data=["date_utc", "depth"],
        zoom=3,
        height=520,
        title="Distribucion geografica de sismos",
    )
    st.plotly_chart(fig, use_container_width=True)


def yugioh_module() -> None:
    """Yu-Gi-Oh module focused on prices, rarity and card types."""

    cards = load_parquet(str(processed_file("yugioh", "yugioh-ccd-2025SEP12-163128.parquet")))

    if cards.empty:
        show_empty_state()
        return

    priced = cards.dropna(subset=["price_numeric"]).copy()

    col1, col2, col3 = st.columns(3)
    col1.metric("Registros de mercado", f"{len(cards):,}")
    col2.metric("Cartas unicas", f"{cards['name'].nunique():,}")
    col3.metric("Precio maximo", f"${priced['price_numeric'].max():,.2f}")

    left, right = st.columns(2)
    with left:
        type_counts = cards["type"].value_counts().reset_index()
        type_counts.columns = ["tipo", "cantidad"]
        fig = px.bar(type_counts, x="tipo", y="cantidad", title="Distribucion por tipo de carta")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        rarity_price = (
            priced.groupby("rarity", as_index=False)["price_numeric"]
            .median()
            .sort_values("price_numeric", ascending=False)
            .head(15)
        )
        fig = px.bar(
            rarity_price,
            x="price_numeric",
            y="rarity",
            orientation="h",
            title="Precio mediano por rareza",
        )
        st.plotly_chart(fig, use_container_width=True)

    by_year = cards.dropna(subset=["release_year"]).groupby("release_year", as_index=False).size()
    fig = px.line(by_year, x="release_year", y="size", markers=True, title="Registros por ano de lanzamiento")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cartas con mayor precio")
    st.dataframe(
        priced.sort_values("price_numeric", ascending=False)[
            ["name", "type", "rarity", "price_numeric", "set_name", "set_release"]
        ].head(25),
        use_container_width=True,
    )


st.title("Grupo 8 - Dashboard de Analisis de Datos")

tab_pokemon, tab_earthquakes, tab_yugioh = st.tabs(
    ["Pokemon competitivo", "Terremotos en Chile", "Yu-Gi-Oh mercado"]
)

with tab_pokemon:
    pokemon_module()

with tab_earthquakes:
    earthquakes_module()

with tab_yugioh:
    yugioh_module()
