
# Coclustering instances × variables


## Décrire et Explorer à la fois

Lors de l’étape d’analyse exploratoire, on cherche à comprendre la structure d’une population sans savoir à l’avance ce que l’on va y trouver. On dispose d’**instances**, c’est-à-dire des individus statistiques d'un jeu de données  — *des clients, des documents, des objets, des événements, etc.* — décrits par un ensemble de variables numériques ou catégorielles. Le clustering permet alors de faire émerger des groupes d’instances qui se ressemblent, tout en distinguant des profils suffisamment différents les uns des autres pour révéler et interpréter la structure présente dans les données.

!!! info "Quelle est l'originalité de l'approche?"
    Le coclustering instances × variables **explore les données en apprenant également le langage pour les décrire**. En effet, les **groupes d’instances** et les **parties de variables** qui permettent de les caractériser sont appris **conjoitement**. Pour une variable catégorielle, une partie est un groupe de modalités ; pour une variable numérique, une partie est un intervalle de valeurs. Ces parties peuvent être regroupées entre elles, y compris lorsqu’elles proviennent de variables de types différents.


Les variables ne sont donc pas condamnées à appartenir *« en bloc »* à un seul groupe : elles sont découpées en parties, dont certaines peuvent être très structurantes et d’autres beaucoup moins. **Cette expressivité est une des forces de l’approche.** 

<figure id="coclustering-intro" style="width:90%; margin:1.5rem auto;">
  <picture>
    <source
      srcset="/assets/images/coclustering_indi_var_intro.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_indi_var_intro.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>

Une image simple est celle d’un **puzzle** : les variables d’origine correspondent à de grandes pièces déjà assemblées, mais ce n’est pas forcément à ce niveau que la structure la plus intéressante apparaît. L’approche commence par **découper ces variables en pièces plus fines**, puis **réassemble les pièces les plus informatives pour faire émerger les profils d’instances**. Le but n’est donc pas seulement de regrouper des individus, mais aussi d’identifier les **morceaux d’information** les plus utiles pour décrire ce qui les rapproche et ce qui les distingue.   

**L’illustration suivante présente plus concrètement le fonctionnement du coclustering instances × variables**, à partir d’un jeu de données volontairement simple décrivant les clients d’une entreprise. Elle montre comment les variables sont découpées en parties, comment ces parties peuvent être regroupées, puis comment les profils d’instances se caractérisent par des distributions différentes sur ces groupes de parties.
  
<figure id="coclustering-overview" style="width:100%; margin:1.5rem 0;">
  <a
    href="/assets/images/coclustering_indi_var_overview.png"
    target="_blank"
    rel="noopener"
    title=""
  >
    <picture>
      <source
        srcset="/assets/images/coclustering_indi_var_overview.webp"
        type="image/webp"
      >
      <img
        src="/assets/images/coclustering_indi_var_overview.png"
        alt=""
        style="display:block; width:100%; height:auto;"
        loading="lazy"
      >
    </picture>
  </a>
</figure>

**Le modèle obtenu se lit comme une carte des profils de la population** *(voir en bas à droite de la figure ci-dessus)*. Chaque ligne de la matrice représente un groupe d’instances, et chaque colonne un groupe de parties de variables. Dans cet exemple, les clients d’un même groupe présentent des distributions similaires de leurs observations sur ces groupes de parties. **Ces distributions caractérisent les profils** et permettent de comprendre ce qui les rapproche et ce qui les distingue.


<div style="display:flex; align-items:center; gap:1.5rem; margin:1.5rem 0;">

  <figure id="coclustering-null-model" style="flex:0 0 23%; margin:0;">
    <picture>
      <source
        srcset="/assets/images/coclustering_indi_var_null_model.webp"
        type="image/webp"
      >
      <img
        src="/assets/images/coclustering_indi_var_null_model.png"
        alt="Null coclustering model"
        style="display:block; width:100%; height:auto;"
        loading="lazy"
      >
    </picture>
  </figure>

  <div style="flex:1;">
    <p style="margin:0;">
      <strong>Le modèle nul</strong> — qui ne retient aucune structure — reste une réponse possible et porteuse d’information.
      Lorsque les données ne justifient pas une structure plus complexe, l’optimisation peut sélectionner un modèle avec une seule partie par variable, un seul groupe d’instances et un seul groupe de parties de variables. Autrement dit, la méthode <strong>n’est pas contrainte de produire artificiellement des profils</strong>. 
    </p>
  </div>

</div>


### Intuition : apprendre les mots en découvrant le monde

Un enfant n’apprend pas d’abord un dictionnaire complet avant de commencer à comprendre le monde. Il apprend progressivement à reconnaître des situations, des objets ou des catégories, tandis que se construit le vocabulaire qui lui permet de les décrire.

**Un dictionnaire entier dans la tête ?** Dans le [coclustering textes × mots][coclustering-applications], le vocabulaire est déjà là : chaque occurrence relie un identifiant de texte à un mot. Le coclustering découvre alors des groupes de textes qui utilisent les mots de manière similaire et, réciproquement, des groupes de mots qui apparaissent dans des groupes de textes similaires. Les deux dimensions se structurent ensemble.

**Quand le modèle construit son propre vocabulaire.** Dans le coclustering instances × variables, les instances jouent le rôle des textes à regrouper et les parties de variables jouent un rôle analogue aux mots : elles forment un vocabulaire descriptif. Mais ce vocabulaire n’est pas donné a priori. Il est construit à partir des données et optimisé en même temps que les groupes d’instances et les groupes de parties de variables.

**Autrement dit : le modèle ne cherche pas seulement les profils d’instances ; il apprend aussi la manière utile de les décrire.**

!!! note "Figure à réaliser — Textes × mots et instances × parties de variables"
    Mettre en parallèle l’application textuelle et le cas général. Le principe du coclustering est conservé, mais, dans le cas général, le vocabulaire descriptif est lui-même appris. Montrer des parties numériques et catégorielles au sein d’un même groupe.

## Paramètres du modèle

Plutôt que de redéfinir le modèle depuis le début, nous allons partir du modèle de coclustering déjà présenté et nous concentrer uniquement sur ce que l’approche instances × variables lui ajoute. La section [*Model parameters* de la page Coclustering][coclustering-parametres] décrit un modèle sur deux variables catégorielles par quatre familles de paramètres : le nombre de groupes, leur composition, les effectifs dans les coclusters et les effectifs des modalités. Le modèle instances × variables conserve cette logique, mais insère un niveau supplémentaire : **avant de regrouper les parties de variables, il faut les définir elles-mêmes !**

### Recodage des données

**Avant toute chose, les données sont recodées dans une représentation adaptée au coclustering instances × variables.** Une instance, décrite à l’origine par plusieurs variables numériques ou catégorielles, est représentée ici par une **collection d’observations** : chaque valeur $v$ observée pour une variable $X_k$ devient un triplet $(u,k,v)$, où $u$ identifie l’instance et $k$ la variable. Ainsi, une même instance génère généralement plusieurs observations. On note $M$ le nombre d’instances, $P$ le nombre de variables et $N$ le nombre total d’observations.

!!! note "Figure à réaliser — Une instance, une collection d’observations"
    Montrer une instance du tableau d’origine, décrite par plusieurs variables, puis sa représentation sous la forme d’une collection de triplets $(u,k,v)$. Le même identifiant $u$ doit apparaître dans tous les triplets issus de cette instance.

Dans un tableau complet avec une seule valeur par variable, chaque instance génère $P$ observations et $N=M\times P$. Cette représentation permet également de gérer naturellement les valeurs manquantes, pour lesquelles aucune observation n’est créée, ainsi que les variables multivaluées, pour lesquelles plusieurs observations sont créées.

<!-- TODO AVANT PUBLICATION : confirmer avec Marc la prise en charge des valeurs
manquantes et multivaluées dans le logiciel. La question reste ouverte dans le
brouillon ; le paragraphe ci-dessus décrit les possibilités de la représentation. -->

Une fois les données ainsi recodées, reste à construire le vocabulaire qui permettra de les analyser : les parties de variables.

### De nouveaux paramètres pour apprendre le vocabulaire

**La principale nouveauté du modèle consiste à apprendre comment découper chaque variable en parties pertinentes.** Ces parties constituent les unités descriptives — le « vocabulaire » — regroupées par le coclustering. Pour chaque variable $X_k$, le modèle introduit d’abord un nombre de parties $J_k$. La partition du domaine $V_k$ de cette variable est notée :

$$
\mathcal P_k=\{V_{k,1},\ldots,V_{k,J_k}\}.
$$

Elle constitue une collection de **sous-ensembles disjoints** dont l’union correspond au domaine de la variable :

- **Pour une variable catégorielle**, chaque $V_{k,t}$ est un ensemble de modalités, par exemple $\{A,C\}$ ou $\{B\}$.
- **Pour une variable numérique**, chaque $V_{k,t}$ est un intervalle dont les bornes sont déduites des effectifs de chacune des parties et de leur ordre, en exploitant les rangs des valeurs.

**Ces parties constituent elles-mêmes l’un des deux axes du coclustering et peuvent être regroupées librement, quelle que soit leur variable d’origine ou leur type.** Un même groupe peut ainsi réunir, par exemple, certaines modalités d’une variable catégorielle et certains intervalles d’une variable numérique. Le modèle dispose ainsi d’un vocabulaire commun pour caractériser les profils, même lorsque les données mélangent variables numériques et catégorielles. **Le découpage des variables, le regroupement de leurs parties et le regroupement des instances sont optimisés conjointement.**

### Une hiérarchie de paramètres { #hierarchie-parametres }

Comme dans le [coclustering présenté précédemment][coclustering-parametres], les paramètres sont introduits dans un ordre hiérarchique, correspondant à des choix successifs lors de l’instanciation d’un modèle. Cette hiérarchie fournit directement la trame du *prior* présenté dans la section suivante et prépare son interprétation en termes de [longueur de description][modl-information].

1. **Définir la taille du vocabulaire :** pour chaque variable $X_k$, choisir son nombre de parties $J_k$.
2. **Définir les parties :** pour chaque variable $X_k$, numérique ou catégorielle, la partition de son domaine en $J_k$ parties est notée $\mathcal P_k=\{V_{k,1},\ldots,V_{k,J_k}\}$.
3. **Former les groupes :** regrouper les instances en $K^u$ groupes, formant la partition $\mathcal C^u$, et les parties de variables en $K^p$ groupes, formant la partition $\mathcal C^p$. Ces deux partitions définissent respectivement les **lignes et les colonnes de la matrice de coclustering**.
4. **Décrire les effectifs d’observations :** chaque case de la matrice $\Phi$ contient le nombre d’observations du cocluster correspondant. Les vecteurs $\delta^u$ et $\delta^p$ détaillent respectivement le total de chaque ligne entre ses instances et le total de chaque colonne entre ses parties. Enfin, pour chaque variable catégorielle $X_k$, $\lambda_k$ précise combien d’observations correspondent à chaque modalité au sein de ses parties.

**Cet ordre organise la description du modèle, mais ne correspond pas à des étapes d’apprentissage indépendantes : le vocabulaire et les groupes sont optimisés conjointement.** La section suivante montre comment évaluer ces choix ensemble, en combinant le coût de description du modèle et celui des données sachant le modèle.

## Critère d’optimisation

**Le principe de sélection MODL reste le même.** Nous recherchons le modèle $h$ le plus probable sachant les données $d$, selon le principe de [sélection bayésienne][modl-bayes]. Cela revient à minimiser la somme de deux [longueurs de description][modl-information] : celle du modèle et celle des données sachant le modèle.

$$
C(h)
=
\underbrace{-\log P(h)}_{L(h)\;:\;\text{description du modèle}}
+
\underbrace{-\log P(d\mid h)}_{L(d\mid h)\;:\;\text{description des données sachant le modèle}}.
$$

**L’apprentissage du vocabulaire ajoute des termes à ces deux composantes.** Dans le *prior*, il faut décrire les paramètres supplémentaires liés aux parties de variables. Dans la *vraisemblance*, il faut préciser les valeurs catégorielles ou les rangs numériques associés aux observations à l’intérieur de ces parties. Nous allons examiner ces ajouts en nous appuyant sur les [termes du coclustering déjà présentés][coclustering-critere].

### Le prior

**Le prior suit la [hiérarchie de paramètres introduite précédemment](#hierarchie-parametres).** À chaque étape, les possibilités compatibles avec les choix précédents sont considérées comme équiprobables. Choisir parmi $q$ possibilités correspond ainsi à une probabilité $1/q$, soit un coût de description de $\log q$. Nous retrouvons le même principe combinatoire que pour le coclustering précédent, appliqué ici à un modèle qui apprend également son vocabulaire.

La longueur de description du modèle se décompose alors suivant les quatre niveaux :

$$
-\log P(h)
=
\underbrace{L_A+L_B}_{\text{nouveaux choix}}
+
\underbrace{L_C}_{\text{coclustering}}
+
\underbrace{L_{D_1}+L_{D_2}+L_{D_3}}_{\text{effectifs, avec }L_{D_3}\text{ nouveau}}.
$$

#### Choisir la taille du vocabulaire

Pour chaque variable $X_k$, le nombre de parties $J_k$ est choisi uniformément : parmi $1,\ldots,|V_k|$ pour une variable catégorielle, et parmi $1,\ldots,N$ pour une variable numérique. Le coût associé est donc respectivement $\log|V_k|$ ou $\log N$.

**Ce premier choix fixe la taille du vocabulaire, pas encore le contenu de ses parties.** À données fixées, son coût ne dépend pas de la valeur retenue pour $J_k$ : c’est l’ensemble du critère qui permettra de départager les granularités.

#### Choisir la composition des parties catégorielles

Une fois $J_k$ fixé, il faut préciser **quelles modalités sont réunies dans chaque partie**. La partition $\mathcal P_k$ est choisie uniformément parmi les partitions possibles du domaine $V_k$, pour un coût :

$$
\log B(|V_k|,J_k).
$$

La fonction $B(a,b)$ compte les partitions de $a$ éléments en au plus $b$ parties non vides, conformément à la convention qui autorise des classes vides, également utilisée dans le [coclustering précédent][coclustering-critere].

Pour les variables numériques, **aucun choix indépendant de bornes n’est ajouté** : les intervalles de rangs seront déterminés par les effectifs des parties et leur ordre. Leur description intervient donc avec les effectifs, au niveau D.

#### Retrouver les choix du coclustering

Nous retrouvons ensuite les mécanismes déjà présentés : choisir le nombre et la composition des groupes, puis les effectifs d’observations associés à cette structure. Les deux axes sont désormais les **instances** et les **parties de variables**.

La matrice $\Phi$ décrit les effectifs des coclusters. Les vecteurs $\delta^u$ et $\delta^p$ détaillent les totaux des lignes entre leurs instances et ceux des colonnes entre leurs parties. À chaque étape, le prior est uniforme parmi les configurations compatibles avec les choix précédents.

#### Décrire les effectifs à l’intérieur des parties catégorielles

**Regrouper des modalités ne signifie pas oublier leurs fréquences respectives.** Pour chaque partie catégorielle, il reste à préciser combien de ses observations correspondent à chacune de ses modalités ; ces effectifs sont les composantes correspondantes du vecteur $\lambda_k$.

Si une partie contient $n$ observations et $r$ modalités, il existe $\binom{n+r-1}{r-1}$ vecteurs d’effectifs possibles dont la somme vaut $n$. Leur choix uniforme donne le coût :

$$
\log\binom{n+r-1}{r-1},
\qquad n=\delta^p_{k,t},\quad r=|V_{k,t}|.
$$

Ce coût est additionné sur toutes les parties catégorielles. Par exemple, une partie $\{A,C\}$ contenant 100 observations admet 101 répartitions d’effectifs possibles : de 0 observation de $A$ et 100 de $C$, jusqu’à 100 de $A$ et 0 de $C$. Le prior décrit laquelle est retenue — par exemple, 70 et 30.

**Les nouveaux termes prolongent donc le même raisonnement : dénombrer les choix nécessaires pour décrire le modèle.** À ce stade, nous avons décrit les partitions et les effectifs. La vraisemblance précise ensuite comment les observations elles-mêmes sont affectées conformément à ces choix.

### La vraisemblance 

**Une fois le modèle défini, il reste à décrire les données en respectant ses partitions et ses effectifs.** Nous retrouvons d’abord les mécanismes du [coclustering précédent][coclustering-critere] : affecter les observations aux coclusters, puis aux instances et aux parties, conformément à $\Phi$, $\delta^u$ et $\delta^p$. La nouveauté intervient ensuite : **connaître la partie associée à une observation ne suffit pas à connaître sa valeur.** Il reste à préciser sa modalité, pour une variable catégorielle, ou son rang, pour une variable numérique.

#### Pour une partie catégorielle 

Le vecteur $\lambda_k$ a déjà fixé le nombre d’occurrences de chaque modalité. **La vraisemblance porte maintenant sur leur affectation aux observations**, en respectant ces effectifs. Pour une partie $V_{k,t}$ contenant $n=\delta^p_{k,t}$ observations, dont $n_v$ occurrences de chaque modalité $v$, le coût est :

$$
\log\frac{n!}{\displaystyle\prod_{v\in V_{k,t}}n_v!}.
$$

Il s’agit du logarithme du nombre d’affectations possibles respectant les effectifs $n_v$, donnés par les composantes correspondantes de $\lambda_k$.

Reprenons la partie $\{A,C\}$ contenant 100 observations, dont 70 de $A$ et 30 de $C$. Le prior a décrit les effectifs **70 et 30** ; il reste à préciser **quelles sont les 70 observations portant $A$**, les autres portant $C$. Le coût correspondant est $\log\binom{100}{70}$.

#### Pour une partie numérique 

Les effectifs des parties et leur ordre déterminent déjà les intervalles de rangs. À l’intérieur d’une partie contenant $n=\delta^p_{k,t}$ observations, il reste à associer les $n$ rangs distincts aux $n$ observations. Il existe $n!$ affectations possibles, d’où le coût :

$$
\log(n!).
$$

Contrairement au cas catégoriel, aucun vecteur d’effectifs par valeur n’est nécessaire : **chaque rang apparaît exactement une fois**.

Ces coûts s’additionnent sur toutes les parties, en complément des termes du coclustering déjà connus. **Le critère ne compare donc pas seulement des coclusterings construits sur des vocabulaires différents : il prend aussi en compte la description de ces vocabulaires et celle des valeurs ou des rangs derrière leurs occurrences.** Le vocabulaire et les groupes peuvent ainsi être évalués conjointement, selon un même critère.

## Algorithme d’optimisation 

Le critère est discret et non convexe ; une exploration exhaustive n’est pas envisageable. L’algorithme procède donc par plusieurs initialisations, exploite l’[optimiseur MODL de coclustering][coclustering-algorithme] lorsque les parties sont fixées, puis affine conjointement les partitions.

1. **Tokeniser les variables à plusieurs granularités.** Pour une granularité donnée, toutes les variables sont initialement découpées avec le même nombre cible de parties. Les variables numériques utilisent des intervalles de fréquences équilibrées ; les variables catégorielles isolent les modalités les plus fréquentes et regroupent les moins fréquentes.
2. **Répéter l’initialisation pour des puissances de deux.** L’article[^article] utilise $2,4,8,\ldots$ jusqu’à $M$, ce qui conduit à environ $\log_2(M)$ lancements du coclustering de base.
3. **Optimiser un coclustering MODL sur instances × parties.** À parties fixées, on retrouve un problème de coclustering de deux variables catégorielles : l’identifiant d’instance et l’identifiant de partie. Le nombre de groupes est optimisé automatiquement.
4. **Évaluer tous les candidats avec le critère complet.** Les solutions obtenues avec les différentes tokenisations sont comparées selon le critère instances × variables, qui inclut précisément le coût de définition des parties.
5. **Affiner conjointement la meilleure solution.** Un procédé glouton teste des opérations telles que déplacer une partie entre groupes, déplacer une valeur entre parties, fusionner des parties ou fusionner des groupes. Une opération est acceptée lorsqu’elle diminue le critère.
6. **S’arrêter à un optimum local.** Lorsque plus aucune opération testée n’améliore le critère, la solution devient le point de départ de l’analyse exploratoire. Il s’agit d’une heuristique : elle vise une solution de haute qualité sans garantie d’optimum global.

!!! note "Figure à réaliser — Stratégie d’optimisation"
    Représenter plusieurs vocabulaires initiaux, l’optimisation MODL du coclustering pour chacun d’eux, la sélection par le critère complet, puis l’affinage conjoint des parties et des groupes.

!!! tip "À retenir"
    - Le besoin reste celui du clustering : des instances semblables dans un même profil et des profils distincts entre eux.
    - La nouveauté est d’apprendre conjointement le vocabulaire descriptif : groupes de modalités pour les variables catégorielles et intervalles pour les variables numériques.
    - Les groupes portent sur les parties de variables : ils peuvent mêler plusieurs variables et plusieurs types, ce qui rend la représentation particulièrement expressive.
    - Le prior donne un coût aux choix successifs du modèle ; la vraisemblance mesure combien d’information reste nécessaire pour retrouver les observations exactes.
    - Le modèle nul est un résultat informatif possible : la méthode n’est pas obligée de fabriquer une segmentation lorsque les données ne la soutiennent pas.
    - L’optimisation réutilise le coclustering MODL sur plusieurs tokenisations, puis ajuste les parties et les groupes de manière conjointe.

<!--
Points éditoriaux encore ouverts dans le brouillon :
- Confirmer le choix des notations de l’article pour la version publique.
- Décider jusqu’où détailler les formules C4a–C4m ; cette version conserve
  le niveau de détail du brouillon sans ajouter leur développement complet.
- Valider avec Marc le comportement du logiciel pour les valeurs manquantes
  et multivaluées, distinct des possibilités du formalisme.
- Réaliser les figures manuellement ; confirmer notamment la piste du puzzle.
- Compléter la référence publique de l’article ci-dessous lorsqu’elle sera disponible.
-->

[^article]: A. Bouchareb, M. Boullé, F. Clérot, C. Hue et F. Rossi. *Fully Automated Co-clustering of Mixed Data Using a Maximum A Posteriori Approach*. Article fourni pour cette rédaction.

[coclustering-applications]: coclustering.md#a-wide-range-of-applications
[coclustering-parametres]: coclustering.md#model-parameters
[coclustering-critere]: coclustering.md#optimization-criterion
[coclustering-algorithme]: coclustering.md#optimization-algorithm
[modl-bayes]: modl.md#bayes
[modl-information]: modl.md#info-theory