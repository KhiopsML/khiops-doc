  
## This is not clustering 

Parmi les approches non-supervisées, les algorithmes de **clustering** sont sans doute les plus connus. Mais ne vous y méprendrenez pas, le **co-clustering** est un problème bien différent. Pour y voir plus clair dans cette distinction entre clustering et co-clustering, commençons par distinguer leurs objectifs respectifs: 

!!! example "Objectif du clustering"
    Regrouper les lignes d’un *jeu de données* en *groupes d’individus* homogènes.

<figure markdown>
<picture>
  <source srcset="/assets/images/exemple_clustering.webp" type="image/webp">
  <img style="width:70%;" src="/assets/images/exemple_clustering.png" alt="exemple_clustering" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

Comme le montre cette figure, les algorithmes de clustering sont utilisés pour trouver des **sous-poputations homogènes** au sein d'un **jeu de donnés**. Ces algorithmes sont généralement basés sur une **distance** qui peut prendre différentes formes et qui est utilisée pour identifier des groupes: (i) les plus éloignés les uns des autres; (i) à l'interieur desquels les individus sont les plus proches possible. En pratique, le choix de cette distance a un impact important sur les resultats d'un clustering, car elle constitue une sorte de **connaissance apriori** utilisée pour simplifier le problème et rendre les algorithmes efficaces en temps de calcul. Notons également que les algorithmes de clustering impliquent généralement de choisir le **nombre de groupes** à former, sans garantie qu'il y existe réellement ces sous-populations identifiables dans le jeu de données. 

!!! example "Objectif du coclustering"
    Regrouper les *lignes* et les *colonnes* d’une *matrice* pour étudier la **dépendance** entre ses deux dimensions. 

<figure markdown>
<picture>
  <source srcset="/assets/images/exemple_coclustering.webp" type="image/webp">
  <img style="width:70%;" src="/assets/images/exemple_coclustering.png" alt="exemple_coclustering" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

Les algorithmes de coclustering regroupent simultanément les **lignes** et les **colonnes** d'une matrice, généralement une **matrice de contingence** décrivant les coocurrences de deux variables catégorielles. Cette matrice de contingence contient le nombre individus pour chaque combinaison de modalité des deux variables catégorielles étudiées. Le croisement (i.e. le produit cartésien) des groupes formés sur les deux dimentions de la matrice constituent un ensemble de **coclusters** (représentés par les bins dans la figure ci-dessus). Un cocluster caractérise une **sous-partie** de la matrice en aggrégant l'information qu'elle contient, i.e. le nombre d'individus dont les combinaisons de modalités sur les deux variables appartiennent au cocluster. Finalement, un modèle de coclustering donne une vue aggrégée d'une matrice de contingence décrivant le lien de **dépendance** entre les deux variables étudiées, il peut être vu comme une modésilation de la **densité jointe** des deux variables.   



!!! info "Ce qu'il faut retenir"
    Comme le **clusterring**, le **coclustering** est un outil puissant pour l'annalyse exploratoire, mais ces deux types d'approches s'appliquent sur des **données différentes** (comme le montre la figure ci-dessous) et leur **finalité** ne sont pas les mêmes.

<figure markdown>
<picture>
  <source srcset="/assets/images/data_clustering_coclustering.webp" type="image/webp">
  <img style="width:95%;" src="/assets/images/data_clustering_coclustering.png" alt="data_clustering_coclustering" loading="lazy"> 
</picture>
  <figcaption>Two different kinds of data used</figcaption>
</figure> 

Le problème du coclustering est également connu sous le vocable **biclustering** en raison des deux seules dimensions de la matrice traitées. En tant que tel, le coclustering est un problème relativement **limité** se restreignant à l'étude de deux variables catégorielles. 

!!! example "MODL généralise le coclustering"
    - Extention aux **variables numériques**
    - **Mixte** entre variables numériques et catégorielles
    - Extention à **plus de deux** variables


Grâce aux extentions permises par le formalisme MODL, le coclustering peut s'appliquer à un **large éventaille d'applications** impliquant des données de nature très différentes. En voici quelques exemples:   

- Text / mots  
- Séries temporelles -> cluster caractérisé par une densité jointes entre valeurs et timestamp
- Graphs -> détection de cliques et d'anti-cliques
     

!!! example "MODL sécurise l'utilisation du coclustering"
    - Pas de choix a priori sur le **nombre de groupes**
    - Garantie de ne **pas former de groupe** en cas **d'indépendance** des variables
    - Garantie contre le **surajustement**


## Intuition du critère 

## Modèle parameter 

## Optimisation criterion 

## Algorithme 




