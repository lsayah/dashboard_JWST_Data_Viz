# Annexes --> dashboard « cibles habitables pour JWST »

le cadrage est dans `cadrage.md` en 1 page. 
ici le complément

---

## A. Info sur le sujet

> **Comprendre le sujet**
> - **JWST** --> télescope spatial (de la NASA) qui peut analyser l'atmosphère d'une exoplanète. son temps d'observation est très demandé --> donc optimisé le choix des meilleures cibles.
> - **zone habitable (ZH)** --> distance à l'étoile où l'eau peut rester liquide. Critère de la vie (avéré mais potentiellement hypothétique)
> - **rocheuse** --> rayon < 2 fois la Terre (2 R⊕), au-delà c'est des gazeuse.
> - **proche** --> moins de 50 pc (≈ 163 années-lumière) --> sinon signaltrop faible


## B. Choix et Limites

- **zone habitable** --> calculée avec l'orbite de la planète et la luminosité de l'étoile (limites de Kopparapu). pas avec la température `pl_eqt`, qui manque pour 74,5 % du catalogue et qui ignore l'effet de serre
- **valeurs manquantes** --> remplies avec les autres publications sur la même planète ou la même étoile (médiane). je touche pas aux valeurs qui existent déjà. la ZH devient calculable pour 5 087 planètes au lieu de 2 914
- **planètes absentes** --> TRAPPIST-1 e et f sont en ZH mais n'ont pas de distance dans le dataset, et Proxima b n'a pas de rayon. je les corrige pas à la main, je le signale dans le dashboard
- **seuils (2 R⊕ et 50 pc)** --> ce sont des choix, pas des vérités. du coup ils sont réglables avec des sliders et le titre se recalcule
- **le chiffre de l'AED** --> le « 55 planètes (3,9 %) » de l'AED était écrit en dur sans calcul (55 / 5 903 = 0,9 %). je l'ai pas repris. chaque pourcentage du dashboard affiche son dénominateur

le détail de tous les tests est dans `tests_et_choix.ipynb`

## C. Utilisation de l'IA

Oui, j’ai utilisé l’IA, surtout pour le code Streamlit. Honnêtement, ça m’a fait gagner beaucoup de temps. La structure de l’app, les graphiques Plotly, et quelques bugs sur lesquels j’aurais galéré seul. Par exemple, sur un graphique en échelle log, ma ligne de seuil partait à 10^50. Je ne comprenais pas pourquoi. L’IA m’a expliqué que sur un axe log, Plotly lit les coordonnées en puissance de 10 : il fallait donner le log de la valeur, pas la valeur elle-même. Ça m’a débloqué en deux minutes.

Mais pour le fond, c’est moi. Les hypothèses, les tests, les KPI, le choix des graphiques. J’ai tout bossé à côté dans un notebook. Je voulais vérifier chaque résultat avant de le mettre dans le dashboard, parce que je ne voulais pas afficher un truc faux. Et surtout, je voulais trouver le bon message et savoir comment le dire. Par exemple, en regardant la distribution des distances, j’ai vu que les valeurs allaient de 1,3 à plus de 8 000 parsecs, avec plus de 1 000 planètes au-delà de 1 000 pc. Pareil pour la taille : de 0,3 à 77 fois la Terre, à cause de quelques géantes gazeuses énormes. Ces valeurs extrêmes écrasaient tout le reste, alors que mes 9 cibles sont toutes à moins de 45 pc et font moins de 2 fois la Terre. En échelle linéaire, elles tenaient dans un seul pixel en bas à gauche. C’est pour ça que j’ai choisi de passer en échelle log sur les deux axes, sinon le graphique ne montrait rien d’utile.

Pour la dataviz, j’ai appliqué des règles que je connaissais déjà. L’objectif, c’était de coller à ce que demandait le projet.

En bref encore heureux que j'ai utilisé l’IA. sinon sa serait comme enfoncer un clou avec sa main dans un monde remplie de marteau (c'est honorable, impressionnant mais pas très efficace). l'IA m’a servi à coder et comprendre plus vite pas à réfléchir à ma place.
