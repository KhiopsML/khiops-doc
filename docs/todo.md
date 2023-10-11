---
hide:
  - toc
  - navigation
---

Cette page provisoire permet de suivre et organiser notre travail. 

**Deadline premier jet : 31 juillet**

**Relectures prévues pour le mois d'août.**

points à traiter (idées):

- vérifier dans la CICD que les lines cassés sont vérifiés??
- un lien vers l'ancien site pour les anciennes version de Khiops
- dans la partie getting started, faire un lien vers no-code 
- page : contact us, renvoyer vers 'issue' de git
- métriques de download sur le site 


## Travail technique pour Getting Started: Stéphane

- Conda install: **(prioritaire V0)** **Vladimir** (1/2 temps) et **Felipe** sur python, et **Bruno.G** et **Stéphane** le binaire (Luc-Aurélien et Alexis test Mac)
- CICD: **(prioritaire V0)** **Bruno.G** et **Felipe** (Luc-Aurélien et Alexis test Mac)
- Integration de la visu dans pyKhiops: **(1)** **Yassine**
- Docker notebook: **(1)** **Stéphane**
- Intégrer les drivers dans le conda install: **(2)** **Stephane**

## Pages en cours de construction
Pour chaque sous-section, un contributeur principal a été identifié afin de produire un premier jet.

- **Welcome Page**: **Luc-Aurélien** et **Alexis**
  
  
- **Getting Started**: coordinateur Luc-Aurélien
    - Installation: **Luc-Aurélien** 
    - Quickstart + CICD: **Felipe**
    - Main functions + simple notebook examples: **Felipe** 
 

- **Advanced use cases**: coordinateur Felipe
    - Technical benefits: **(prioritaire V0)** **Yassine** + **Vincent** (aout)
    - GO / No Go: **(1)** **Vladimir**
    - Analyse descriptive + corrélation des paires: **(2)** **Vladimir** et **Fabrice** MAJ V11 - adaptée à la dispo du widget de visu
    - Covariate shift detection: **(3)** **Vincent** et **Pierre** 
    - Time Series (ou log) en multi-table: **(4)** **Yassine**

    - **After V11**
        - NLP (données mixtes)
        - Introduction co-clustering
        - Anomaly detection: **Pierre**   
        - Model calibration: **Yassine** et **Nicolas** 
        - Variable importance with Shapley 


    
- **Understanding**: coordinateur Alexis 
    - What makes Khiops Different : (V0) **Luc-Aurélien**
    - How it works:
        - An original formalism: (V0) **Alexis**
        - Optimal Encoding: (V0) **Alexis**
        - Auto Feature Engineering: (V0) **Alexis**
            - Ajouter une section très courte à la fin sur les arbres : (1) **Nicolas**
                - (Si notebook: utiliser le dataset Letter)
        - Parcimonious Training: (V0) **Alexis**
        - Unsupervised Analysis:(AFTER)  **Alexis**
        - Auto Hardware Adaptation: (V0) **Alexis**
            - Ajouter un tableau de resultats de temps de calcul en out of core et parallélisant: (1) **Marc** 
    - How to use:
        - Reports & visualization: (V0) **Fabrice**
            - sanbox demo live: **(1)** **Gregory**
        - Variable Types: (V0) **Marc** et **Alexis**
        - Data Management tools: After
- **Tools**: *(3 catégories avec un niveau de support décroissant)*
    - **Other Products** : **Vincent** (rédaction) + **Bruno.G** (page de download)
        -  No-code: **(prioritaire V0)**
        -  Visu.exe: **(prioritaire V0)** si pas intégré à No-code ou pas intégré à pyKhiops
    - **Enablers / Dockers (1)** : **Stephane** 
        1. Docker Khiops.bin + Drivers
        2. Docker Khiops.bin + pyKhiops 
        3. Docker Vertex AI + notebooks d'exemple
        4. Dockers Workbench (+ jupyter notebooks)
             1. GCP
             2. Debian
        5. Drivers seuls   
    - **Lab / Add-on** : (2) After (les codes pythons utilisant pyKhiops)
        -  Enead No-code (windows): (2) After - à recoder en python, Vincent  
        -  Fears: (2) After, Alexis 
        -  Khiosto: (2) After, Marc 
        -  Kastor: (2) After, Nicolas
  
- **Bibliography**: Alexis

*Note: une fois votre page terminée, vous devez ajouter votre section dans la liste ci-dessous pour relecture.*

## Pages prêtes à la relecture
Les pages listées ci-dessous sont prêtes à être relues. 
Vous pouvez soit faire une relecture sur une version PDF du document et envoyer au contributeur principal, soit créer une nouvelle branche `git` (préférable pour les corrections importantes).  

- **Welcome Page**: Luc-Aurélien et Alexis
- **Understanding**: 
    - How it works:
        - An original formalism: Alexis
        - Optimal Encoding: Alexis
        - Auto Feature Engineering: Alexis
        - Parcimonious Training: Alexis 
        - Auto Hardware Adaptation: Alexis