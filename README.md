# Dashboard JWST --> les planètes « type Terre » à observer en priorité

dashboard Streamlit sur les exoplanètes de la NASA -->  sur 5 903 planètes connues --> 9 sont "type Terre" et assez proches pour être étudiées par le télescope JWST

**en ligne** : 

## lancer en local

```bash
pip install -r requirements.txt
streamlit run Synthese.py
```

le dashboard s'ouvre sur http://localhost:8501

## les fichiers

- `Synthese.py` --> page principale (le message, les 3 KPIs, le graphique)
- `pages/` --> détail des cibles + données manquantes
- `utils.py` --> chargement des données et filtres, partagés par toutes les pages
- `data/exoplanets.csv` --> les données (NASA Exoplanet Archive)
- `cadrage.md` --> le cadrage (1 page) / `annexes.md` --> le complément
- `tests_et_choix.ipynb` --> tous les tests et les choix avant le dashboard
