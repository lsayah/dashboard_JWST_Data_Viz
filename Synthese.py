
# IMPORT
import numpy as np
import plotly.express as px
import streamlit as st

from utils import ACCENT, FAR, GREY, load_data, sidebar_filters

st.set_page_config(page_title="Cibles JWST", page_icon="🔭", layout="wide")


# Données
df = load_data()
data, max_dist, max_radius = sidebar_filters(df)

n_total = len(data)
n_candidates = int(data["candidate"].sum())
targets = data[data["target"]]
n_targets = len(targets)


# titre = le message
st.title(f"{n_targets} planètes « type Terre » sont assez proches pour être étudiées par JWST")

# pour quelqu'un qui connaît rien au sujet
st.info(
    "**JWST** = le télescope spatial le plus puissant. Son temps d'observation est rare "
    "--> il faut choisir les bonnes planètes.\n\n"
    "**« Type Terre »** = une planète rocheuse (pas une boule de gaz) **et** à la bonne "
    "distance de son étoile pour avoir de l'eau liquide."
)


# KPI
# pas de flèche delta, elle ferait croire que le chiffre augmente
total_txt = f"{n_total:,}".replace(",", " ")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Planètes « type Terre »", n_candidates)
    st.caption(f"sur {total_txt} exoplanètes connues")

with col2:
    st.metric("Assez proches pour JWST", n_targets)
    recent = int((targets["disc_year"] >= 2017).sum())
    st.caption(f"à moins de {max_dist} parsecs · {recent} trouvées depuis 2017, la plupart par TESS")

with col3:
    n_hz = int(data["in_hz"].sum())
    no_radius = int((data["in_hz"] & data["pl_rade"].isna()).sum())
    share = no_radius / n_hz if n_hz else 0
    st.metric("Bonne température mais taille inconnue", f"{share:.0%}")
    st.caption(f"{no_radius} planètes : on sait pas si elles sont rocheuses --> à mesurer")

st.divider()


# Graph principal
st.subheader("Chaque point est une planète : les cibles (en orange) sont petites et proches")
st.caption("Plus à gauche = plus proche de nous. Plus bas = plus petite. Les cibles sont dans le coin en bas à gauche.")

plot = data.dropna(subset=["sy_dist", "pl_rade"]).copy()
plot["Catégorie"] = "Autres planètes"
plot.loc[plot["candidate"], "Catégorie"] = "« Type Terre » mais trop loin"
plot.loc[plot["target"], "Catégorie"] = "Cible JWST"

fig = px.scatter(
    plot, x="sy_dist", y="pl_rade", color="Catégorie",
    color_discrete_map={"Autres planètes": GREY,
                        "« Type Terre » mais trop loin": FAR,
                        "Cible JWST": ACCENT},
    # cibles en dernier pour qu'elles passent devant les points gris
    category_orders={"Catégorie": ["Autres planètes", "« Type Terre » mais trop loin", "Cible JWST"]},
    # en linéaire tout est écrasé dans un coin
    log_x=True, log_y=True,
    hover_name="pl_name",
    hover_data={"sy_dist": ":.1f", "pl_rade": ":.2f", "star_type": True,
                "disc_year": True, "Catégorie": False},
    labels={"sy_dist": "Distance à la Terre (parsecs, échelle log)",
            "pl_rade": "Taille (× la Terre, échelle log)",
            "star_type": "Étoile", "disc_year": "Découverte"},
)

# IMPORTANT --> axe log = il faut le log10 de la valeur, sinon la ligne part à 10^50
fig.add_vline(x=np.log10(max_dist), line_dash="dash", line_color="#888", line_width=2,
              annotation_text=f"limite JWST : {max_dist} pc",
              annotation_position="top right")
fig.add_hline(y=np.log10(max_radius), line_dash="dash", line_color="#888", line_width=2,
              annotation_text=f"limite rocheuse : {max_radius} × Terre",
              annotation_position="bottom right")

fig.update_traces(marker=dict(size=6, opacity=0.6))
for trace in fig.data:
    if trace.name == "Cible JWST":
        trace.marker.size = 12
        trace.marker.opacity = 1

fig.update_layout(height=550, legend=dict(title="", orientation="h", y=1.08))
st.plotly_chart(fig, use_container_width=True)

# dommage pour TRAPPIST-1, c'est quand même la star du sujet. mais je bidouille pas le dataset
st.caption(
    "Données : NASA Exoplanet Archive. Absentes faute de données : TRAPPIST-1 e et f "
    "(distance manquante) et Proxima b (taille inconnue)."
)
