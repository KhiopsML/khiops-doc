

Deux API pour des usages différents 

# API SKL : besoins classiques - skl complience - (low scale)

Les plus 

- une syntaxe connue des DS, donc une prise en main imédiate 
- intégration dans l'écosystème SKL (c'est un estimateur standard SKL)
- possibilité de tester le Multi-table et l'Auto feature engineering (shémat en flocon, mais pas de tables externes, limité au mapping 1 pour 1 des fichiers et des tables)

Les moins 

- scalabilité limitée, pas de out-of-core,  
- des IO importants  
- limites inérantes à python et particulièrement Pandas en terme d'usage de la mémoire et de scaling.  
 

# API CORE & dictionnaire : besoin de mise en production (unleach the power of Khiops)

Les plus 

- Dico : un formalisme riche de description de données Multi-Table ()
- Facilité de gestion (et versionnage) de l'ensemble du flow de transformation des données   
- Data management efficace, calculé à la volée (aggrégats métier, sélection de variable, de table et d'exemples ... ) 
- Mise en production agile des modèles 
- Calcul Out-of-core, et une utilisation optimisée des ressources matérielles 

Les moins 

- il faut se former à un nouveau language que sont les dictionnaires et les concepts associés. 


TODO : insister sur le travail préparatoir avant l'auto-ml (cf CRISP-DM). 