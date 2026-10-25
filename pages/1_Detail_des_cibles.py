
# IMPORT
import plotly.express as px
import streamlit as st

from utils import ACCENT, FAR, load_data, sidebar_filters

st.set_page_config(page_title="Détail des cibles", page_icon="🔭", layout="wide")


# Données
df = load_data()
data, max_dist, max_radius = sidebar_filters(df)

candidates = data[data["candidate"]].copy()
targets = data[data["target"]].sort_values("sy_dist")

# bleu = rocheuse en ZH mais trop loin (même couleur que sur la page synthèse)
candidates["Catégorie"] = "« Type Terre » mais trop loin"
candidates.loc[candidates["target"], "Catégorie"] = "Cible JWST"
COLORS = {"Cible JWST": ACCENT, "« Type Terre » mais trop loin": FAR}


# filtres trop serrés --> un message plutôt que des graphiques vides
if len(targets) == 0:
    st.title("Aucune cible avec ces réglages")
    st.warning("Augmente la distance max ou la taille max dans la sidebar.")
    st.stop()


# titre = le message de la page
# ~40 années-lumière pour la plus proche, on est pas près d'y aller
closest = targets.iloc[0]
closest_al = closest["sy_dist"] * 3.26
st.title(f"{len(targets)} cibles, et la plus proche est à seulement {closest_al:.0f} années-lumière")
st.markdown(
    f"C'est **{closest['pl_name']}**, à {closest['sy_dist']:.0f} parsecs. "
    "Plus une cible est proche, plus JWST capte de lumière et mieux il peut analyser son atmosphère."
)


tab1, tab2, tab3 = st.tabs(["Les plus proches", "Quand on les a trouvées", "La liste complète"])

with tab1:
    st.subheader("Plus une planète est proche, plus JWST peut bien l'observer")

    # barres horizontales pour lire les noms + axe à 0 pour pas grossir les écarts
    fig = px.bar(
        targets, x="sy_dist", y="pl_name", orientation="h",
        color_discrete_sequence=[ACCENT],
        text=targets["sy_dist"].round(1),
        hover_data={"pl_rade": ":.2f", "star_type": True, "disc_year": True},
        labels={"sy_dist": "Distance à la Terre (parsecs)", "pl_name": "",
                "pl_rade": "Taille (× Terre)", "star_type": "Étoile", "disc_year": "Découverte"},
    )
    fig.update_yaxes(categoryorder="total descending")
    fig.update_xaxes(range=[0, max_dist])
    fig.update_traces(textposition="outside")
    fig.update_layout(height=max(300, 40 * len(targets)))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Les planètes trop lointaines datent de Kepler, les cibles sont récentes")

    per_year = (candidates.groupby(["disc_year", "Catégorie"]).size()
                .reset_index(name="nb"))
    fig = px.bar(
        per_year, x="disc_year", y="nb", color="Catégorie",
        color_discrete_map=COLORS,
        category_orders={"Catégorie": ["Cible JWST", "« Type Terre » mais trop loin"]},
        labels={"disc_year": "Année de découverte", "nb": "Nombre de planètes"},
    )
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=450, legend=dict(title="", orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)
    # Kepler a fait le gros du boulot, mais il regardait trop loin pour JWST
    st.caption(
        "Kepler (2009-2018) regardait des étoiles lointaines --> beaucoup de planètes, mais trop loin. "
        "TESS (depuis 2018) regarde les étoiles proches --> c'est lui qui trouve les cibles."
    )

with tab3:
    st.subheader("Toutes les planètes « type Terre », les cibles en premier")

    table = (candidates
             .sort_values(["target", "sy_dist"], ascending=[False, True])
             [["pl_name", "target", "sy_dist", "pl_rade", "star_type", "disc_year"]]
             .rename(columns={"pl_name": "Planète", "target": "Cible JWST",
                              "sy_dist": "Distance (parsecs)", "pl_rade": "Taille (× Terre)",
                              "star_type": "Étoile", "disc_year": "Découverte"}))
    st.dataframe(
        table, hide_index=True, use_container_width=True,
        column_config={"Distance (parsecs)": st.column_config.NumberColumn(format="%.1f"),
                       "Taille (× Terre)": st.column_config.NumberColumn(format="%.2f"),
                       "Découverte": st.column_config.NumberColumn(format="%d")},
    )
    st.caption(f"{len(candidates)} planètes : moins de {max_radius} × la taille de la Terre "
               "et à la bonne distance de leur étoile.")
