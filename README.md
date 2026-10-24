# master-mva

Supports de cours (pages HTML) pour le master 2 **Mathématiques, Vision, Apprentissage (MVA)** de l'ENS Paris-Saclay (co-accrédité avec l'Institut Polytechnique de Paris, partagé avec l'Université Paris Cité).

**Site (EN only)** : <https://knoel99.github.io/master-mva/> (GitHub Pages, à activer sur la branche par défaut).

## Objectif

Reconstituer, cours par cours, un **support complet et auto-contenu** pour chaque matière scientifique du catalogue MVA 2026–2027, destiné à un étudiant de niveau M1 en mathématiques, informatique ou physique. Chaque page contient :

- une **fiche** avec les faits officiels (enseignants, semestre, label Learning / Modelling / Opening, track, ECTS, volume horaire, évaluation, prérequis) et un **tableau de correspondance** avec le programme officiel ;
- un **plan de séances** dont les heures totalisent le volume officiel, avec un niveau 1/2/3 qui ne redescend jamais ;
- le **cours** (définitions, théorèmes, démonstrations, exemples chiffrés) et du **code Python** exécutable ;
- des **exercices gradués** (★ / ★★ / ★★★) avec solutions ;
- une section **Projects and assessment** : sujets de projets en solo et en groupe (dont l'étude d'un article de recherche, tradition du MVA), un sujet d'examen écrit avec barème, une grille d'évaluation ;
- les **références** officielles et standard.

La page d'accueil (générée) donne l'arbre des cours par semestre et par label, les boutons des tracks officiels (Santé, I&I, RR) et trois parcours d'exemple vérifiés contre les modalités de validation, le tableau des volumes horaires, et un lien vers les **projets de fin d'année** (`projects/`).

## État (octobre 2026)

- **67 pages de cours** : 64 matières scientifiques du catalogue 2026–2027, et 3 refreshers indépendants pour la quinzaine de remise à niveau. S'y ajoutent 4 pages de cadrage (immersion à l'hôpital, Regulating AI, projet de recherche reproductible, stage) et la page des projets de fin d'année (`projects/`).
- **Contrôles** : `python3 tools/check_gates.py` passe (1636/1636), `check_progression` 67/67, `check_airiness` sans erreur. Tous les liens entre pages sont valides.
- **Rendu** : un navigateur sans interface a ouvert toutes les pages, en 1440 px clair et 390 px sombre. Aucune erreur JavaScript ou KaTeX, aucun débordement horizontal.
- **Relecture** : chaque rédacteur a exécuté tous les blocs Python de sa page et vérifié les nombres cités. 17 pages ont en plus été relues par un second agent indépendant, qui a corrigé faits, mathématiques et références. Cette seconde lecture reste à faire pour les autres pages.

## Sources

- Catalogue et règles : <https://www.master-mva.com/> (listes des cours des deux semestres, chaque page de cours, modalités de validation, planning, tracks, stage), lu le 22 octobre 2026.
- Volumes et ECTS : <https://www.universite-paris-saclay.fr/en/education/master/mathematics-and-applications/m2-mathematics-vision-learning>.
- Les deux sources sont fusionnées dans `data/catalog-2026-2027.json`, source structurelle unique.

> Ces supports sont des **reconstitutions pédagogiques indépendantes** rédigées à partir du programme public et des références standard de chaque domaine ; ils ne remplacent pas les cours officiels et ne sont ni produits ni validés par l'ENS Paris-Saclay ou les enseignants du master.

## Structure

```
index.html                   page d'accueil (générée par tools/build_home.py)
projects/index.qmd|html      projets de fin d'année
courses/<slug>/index.qmd     source Quarto d'un cours (s0- refresher, s1- / s2- semestre, year-, s3- stage)
courses/<slug>/index.html    page rendue
data/catalog-2026-2027.json  catalogue officiel fusionné
assets/                      paper.css, theme.js, illustrations
specs/                       contrats (dont lessons-from-llga.md : ce que le site hérite du dépôt LLGA)
tools/                       génération, rendu, contrôles
```

## Construire et vérifier

```bash
pip install quarto-cli==1.7.32
python3 tools/new_course.py <slug>      # squelette d'une nouvelle page
python3 tools/render.py --all           # rendu Quarto + KaTeX épinglé
python3 tools/build_home.py             # page d'accueil
python3 tools/check_gates.py            # toutes les vérifications
```
