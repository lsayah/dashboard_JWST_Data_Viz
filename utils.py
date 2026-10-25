
# Utils.py sert à toutes les pages 
# - chargement des données 
# - filtres

# IMPORT
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# chemin à partir de ce fichier, sinon sa casse sur Streamlit Cloud (bug 3 du notebook)
DATA_PATH = Path(__file__).parent / "data" / "exoplanets.csv"

# 92 colonnes dans le csv --> j'en garde 11
COLUMNS = ["pl_name", "hostname", "default_flag", "disc_year", "discoverymethod",
           "pl_rade", "pl_orbsmax", "pl_eqt", "st_rad", "st_teff", "sy_dist"]

# COULEURS
# orange = cibles, bleu = type Terre mais trop loin, gris = le reste
ACCENT = "#E8590C"
FAR = "#5C7CFA"
GREY = "#B0B0B0"


# au final les 9 cibles tournent toutes autour d'une naine rouge mais pas une seule autour d'une étoile comme le Soleil
def star_type(teff):
    if pd.isna(teff):
        return "Inconnu"
    if teff < 3900:
        return "M (naine rouge)"
    if teff < 5300:
        return "K"
    if teff < 6000:
        return "G (type Soleil)"
    return "F ou plus chaude"


# IMPORTANT --> sans le cache streamlit relit les 37 Mo à chaque clic sur un filtre
@st.cache_data
def load_data():
    # comment="#" sinon les com NASA au début du fichier font planter pandas
    raw = pd.read_csv(DATA_PATH, comment="#", usecols=COLUMNS, low_memory=False)

    # 1 ligne = 1 publication --> default_flag == 1 pour avoir 1 ligne par planète
    df = raw[raw["default_flag"] == 1].copy()

    # les trous sont remplis avec ce que les autres publications ont mesuré
    for col, key in [("sy_dist", "hostname"), ("st_rad", "hostname"),
                     ("st_teff", "hostname"), ("pl_orbsmax", "pl_name"),
                     ("pl_rade", "pl_name")]:
        median_by_key = raw.groupby(key)[col].median()
        df[col] = df[col].fillna(df[key].map(median_by_key))

    # zone habitable avec l'orbite et pas avec pl_eqt (vide à 74,5 %)
    # 5778 K = le Soleil, tout est comparé à lui
    lum = df["st_rad"] ** 2 * (df["st_teff"] / 5778) ** 4
    inner = np.sqrt(lum / 1.776)
    outer = np.sqrt(lum / 0.32)
    # -1 = bord chaud, +1 = bord froid. la Terre est à -0,5
    df["HZD"] = (df["pl_orbsmax"] - (inner + outer) / 2) / ((outer - inner) / 2)
    df["in_hz"] = df["HZD"].abs() <= 1

    df["star_type"] = df["st_teff"].apply(star_type)
    return df


# pour la page données manquantes : % de trous avant / après remplissage
@st.cache_data
def missing_report():
    raw = pd.read_csv(DATA_PATH, comment="#", usecols=COLUMNS, low_memory=False)
    before = raw[raw["default_flag"] == 1]
    after = load_data()

    cols = {"pl_orbsmax": "Distance planète-étoile", "pl_rade": "Taille de la planète",
            "st_rad": "Taille de l'étoile", "st_teff": "Température de l'étoile",
            "sy_dist": "Distance à la Terre"}
    return pd.DataFrame({
        "Colonne": list(cols.values()),
        "Avant remplissage": [before[c].isna().mean() * 100 for c in cols],
        "Après remplissage": [after[c].isna().mean() * 100 for c in cols],
    })


# FILTRES SIDEBAR
def sidebar_filters(df):
    types = sorted(df["star_type"].unique())
    year_min, year_max = int(df["disc_year"].min()), int(df["disc_year"].max())

    # Evite de remetre les filtres par défaut à chaque changement de page
    defaults = {"max_dist": 50, "max_radius": 2.0, "star_types": types,
                "years": (year_min, year_max)}
    for key, value in defaults.items():
        st.session_state[key] = st.session_state.get(key, value)

    # les 2 seuils en sliders, comme sa le choix est pas caché
    st.sidebar.header("Réglages")
    max_dist = st.sidebar.slider(
        "Distance max (parsecs)", 10, 200, step=5, key="max_dist",
        help="1 parsec ≈ 3,26 années-lumière. Plus loin, JWST capte trop peu de lumière.")
    # au-delà de 2 × la Terre c'est plutôt une boule de gaz (pas top pour s'y poser)
    max_radius = st.sidebar.slider(
        "Taille max d'une planète rocheuse (× Terre)", 1.0, 3.0, step=0.1, key="max_radius",
        help="Au-delà de 2 fois la Terre, la planète est probablement gazeuse.")

    st.sidebar.header("Filtrer le catalogue")
    chosen_types = st.sidebar.multiselect("Type d'étoile", types, key="star_types")
    years = st.sidebar.slider("Années de découverte", year_min, year_max, key="years")

    filtered = df[df["star_type"].isin(chosen_types)
                  & df["disc_year"].between(years[0], years[1])].copy()

    # candidate = type Terre / target = type Terre + assez proche pour JWST
    filtered["candidate"] = filtered["in_hz"] & (filtered["pl_rade"] < max_radius)
    filtered["target"] = filtered["candidate"] & (filtered["sy_dist"] < max_dist)
    return filtered, max_dist, max_radius
