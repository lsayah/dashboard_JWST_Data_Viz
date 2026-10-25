
# IMPORT
import plotly.express as px
import streamlit as st

from utils import ACCENT, GREY, load_data, missing_report, sidebar_filters

st.set_page_config(page_title="Données manquantes", page_icon="🔭", layout="wide")


# DONNEES
df = load_data()
data, max_dist, max_radius = sidebar_filters(df)
report = missing_report()

n_hz = int(data["in_hz"].sum())
no_radius = int((data["in_hz"] & data["pl_rade"].isna()).sum())


# titre
st.title("On ne connaît pas la taille de beaucoup de planètes")
st.markdown(
    f"**{no_radius} planètes sur {n_hz}** sont à la bonne température mais leur taille est inconnue "
    "--> impossible de savoir si elles sont rocheuses. Si on les mesurait, la liste des cibles "
    "pourrait s'allonger."
)


# Graph manquants avant / après
st.subheader("On a bouché une partie des trous avec les autres mesures")

# melt pour avoir 2 barres par colonne (avant / après)
long = report.melt(id_vars="Colonne", var_name="Moment", value_name="% manquant")
fig = px.bar(
    long, x="% manquant", y="Colonne", color="Moment", barmode="group", orientation="h",
    color_discrete_map={"Avant remplissage": GREY, "Après remplissage": ACCENT},
    text=long["% manquant"].round(0).astype(int).astype(str) + " %",
    labels={"Colonne": "", "% manquant": "Valeurs manquantes (% des 5 903 planètes)"},
)
# axe de 0 à 100 --> c'est un pourcentage (échelle entière)
fig.update_xaxes(range=[0, 100])
fig.update_traces(textposition="outside")
fig.update_layout(height=400, legend=dict(title="", orientation="h", y=1.12))
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Une planète est souvent mesurée par plusieurs équipes. Quand une valeur manque, "
    "on prend celle des autres mesures. Les valeurs déjà présentes ne sont jamais modifiées."
)

st.divider()


# Tableau des planètes en ZH qu'on peut pas classer
st.subheader("Les planètes à la bonne température qu'on ne peut pas classer")

# en ZH mais rayon ou distance manquant --> ne peuvent pas devenir des cibles
unknown = data[data["in_hz"] & (data["pl_rade"].isna() | data["sy_dist"].isna())].copy()
unknown["Il manque"] = ""
unknown.loc[unknown["pl_rade"].isna(), "Il manque"] = "la taille"
unknown.loc[unknown["sy_dist"].isna(), "Il manque"] = "la distance"
unknown.loc[unknown["pl_rade"].isna() & unknown["sy_dist"].isna(), "Il manque"] = "taille + distance"

# les plus proches en premier (celles qui valent le plus le coup d'être mesurées)
table = (unknown.sort_values("sy_dist")
         [["pl_name", "Il manque", "sy_dist", "pl_rade", "star_type", "discoverymethod"]]
         .rename(columns={"pl_name": "Planète", "sy_dist": "Distance (parsecs)",
                          "pl_rade": "Taille (× Terre)", "star_type": "Étoile",
                          "discoverymethod": "Méthode de découverte"}))
st.dataframe(
    table, hide_index=True, use_container_width=True,
    column_config={"Distance (parsecs)": st.column_config.NumberColumn(format="%.1f"),
                   "Taille (× Terre)": st.column_config.NumberColumn(format="%.2f")},
)
# Proxima b c'est la plus proche de nous et on connaît même pas sa taille, frustrant
st.caption(
    "Exemples : Proxima Cen b, la plus proche de nous (elle passe pas devant son étoile, "
    "donc pas de taille mesurée), et TRAPPIST-1 e et f (distance absente du dataset)."
)
