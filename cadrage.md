# Cadrage --> dashboard "cibles habitables pour JWST"

**Données** : NASA Exoplanet Archive, même dataset que pour le cours AED (comme convenu dans le sujet et puis ça si prète bien). 5 903 exoplanètes confirmées (1 ligne par planète avec `default_flag == 1`)
**Lien du dashboard** : 

---

**Annexes** (comprendre le sujet, choix et limites, utilisation de l'IA) --> `annexes.md`

---

## 1. Le Message

> **Sur 5 903 exoplanètes connues, seulement 29 sont « type Terre » (rocheuses et en zone habitable), et 9 sont à moins de 50 pc --> c'est la liste à proposer en priorité pour JWST.**

à côté de ça :
- les 9 tournent toutes autour de naines rouges (type M)
- 8 sur 9 ont été découvertes depuis 2017, la plupart par TESS --> la liste est récente et elle va encore bouger

## 2. Pour Qui ??

une **équipe de chercheurs qui prépare une demande de temps d'observation sur JWST** (pour analyser l'atmosphère des planètes)

la décision qu'elle doit prendre --> **quelles planètes mettre dans la demande, et dans quel ordre**

## 3. les KPI

3 KPIs, chacun avec un contexte écrit en dessous (comparaison ou tendance)

| KPI | valeur | contexte | pourquoi c'est actionnable |
|---|---|---|---|
| **planètes « type Terre »** (taille < 2 × la Terre et dans la ZH) | 29 | sur 5 903 exoplanètes connues | c'est la taille du vivier. sa change si on bouge les critères |
| **assez proches pour JWST** (les 29, à moins de 50 pc) | 9 | 8 sur 9 trouvées depuis 2017, la plupart par TESS | c'est directement la liste à mettre dans la demande |
| **bonne température mais taille inconnue** | 60 % (150 sur 249) | 150 planètes en ZH dont on sait pas si elles sont rocheuses --> à mesurer | dit où faire des observations de suivi pour allonger la liste |

**vanity metrics que j'ai écartées :**
- "5 903 exoplanètes découvertes" --> sa impressionne mais sa aide pas à choisir une cible
- "nombre de méthodes de découverte" --> sa décrit le catalogue, aucune action derrière
- "ESI moyen" (indice de ressemblance avec la Terre) --> il faut la masse, mesurée pour seulement 9 candidates sur 29. la moyenne serait biaisée

## 4. La Structure

**filtres --> sidebar** (la même sur toutes les pages)
- distance max (slider, 50 pc par défaut)
- taille max d'une planète rocheuse (slider, 2 × la Terre par défaut)
- type d'étoile
- années de découverte
- les réglages restent les mêmes quand on change de page

**zone KPIs --> page 1, synthèse (`Synthese.py`)**
- le titre = le message, avec les nombres recalculés selon les filtres
- un encadré de 2 lignes : c'est quoi JWST + c'est quoi « type Terre »
- les 3 KPIs côte à côte, contexte écrit en dessous (pas de flèche delta, elle ferait croire à une hausse)
- un graphique distance x taille en échelle log. les cibles en orange, le reste en gris --> on les voit en moins de 5 secondes. les 2 seuils sont tracés en pointillés

**zone détail --> page 2, détail des cibles (`pages/1_Detail_des_cibles.py`)**, un onglet par graphique
- le titre : le nombre de cibles et la distance de la plus proche en années-lumière
- les cibles classées par distance (barres horizontales, axe qui part de 0)
- les découvertes de planètes « type Terre » par année --> les lointaines viennent de Kepler (2013-2016), les cibles proches de TESS (depuis 2018)
- le tableau des planètes « type Terre » (nom, taille, distance, étoile, année), les cibles en premier

**zone détail --> page 3, données manquantes (`pages/2_Donnees_manquantes.py`)**
- la part de valeurs manquantes avant / après remplissage
- la liste des planètes à la bonne température qu'on peut pas classer (taille ou distance inconnue), ex : TRAPPIST-1, Proxima b

**côté technique** --> `@st.cache_data` sur le chargement des données, et `utils.py` partagé par toutes les pages (chargement + filtres)
