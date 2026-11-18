# Instances × Variables Coclustering



<figure id="coclustering-intro" style="width:45%; margin:1.5rem auto;">
  <picture>
    <source
      srcset="/assets/images/coclustering_indi_var_first_picture.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_indi_var_first_picture.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>

To get the idea, picture a child discovering the world: as they learn to recognize objects and situations, they also learn the words to describe them. **Discovery and vocabulary learning go hand in hand.**

Instances × variables coclustering follows a similar intuition: **discover profiles in the data while learning the vocabulary needed to characterize them.** The goal is not just to group similar instances, but also to learn how to describe their similarities and differences.

## Describing and Exploring Together

Exploratory analysis aims to understand the structure of a population without knowing in advance what we will find. The data consist of **instances**, the statistical units in a dataset — *customers, documents, objects, events, and so on* — described by numerical or categorical variables. Clustering brings similar instances together, while identifying profiles that are distinct enough to reveal and help interpret the structure of the data.

!!! info "What Makes This Approach Different"
    Instances × variables coclustering **explores the data while learning the language used to describe them**. The **instance groups** and the **variable parts** that characterize them are learned **jointly**. For a categorical variable, a part is a group of categorical values; for a numerical variable, it is an interval of values. These parts can be grouped together, even when they come from variables of different types.


Variables therefore need not belong *“as a whole”* to a single group: they are split into parts, some of which reveal strong structure while others are less informative. **This expressive power is one of the approach’s strengths.**

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

Think of a **jigsaw puzzle**: the original variables are like large, preassembled sections, but the most interesting structure may emerge at a finer scale. The approach jointly learns to **split these variables into smaller pieces** and **reassemble those pieces** to reveal instance profiles. The aim is not just to group instances, but also to identify the **pieces of information** that best describe what they have in common and what sets them apart.

**The following illustration shows how instances × variables coclustering works in practice**, using a deliberately simple dataset describing a company’s customers. It shows how variables are split into parts, how these parts can be grouped, and how instance profiles are characterized by different distributions over these groups of parts.
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

**The resulting model can be read as a map of the population’s profiles** *(see the bottom-right corner of the figure above)*. Each matrix row represents an instance group, and each column a group of variable parts. In this example, customers within the same group have similar distributions of observations over these groups of parts. **These distributions characterize the profiles** and help us understand their similarities and differences.


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
      <strong>The null model</strong> — which retains no structure — is also a possible and informative outcome.
      When the data do not justify a more complex structure, optimization may select a model with a single part per variable, a single instance group, and a single group of variable parts. In other words, the method <strong>does not have to force profiles onto the data</strong>.
    </p>
  </div>

</div>


## A Closer Look at What Changes

**Let’s return to the child discovering the world while learning to describe it.** This analogy illustrates what instances × variables coclustering adds to the [texts × words coclustering introduced earlier][coclustering-applications].

**Texts × words: the vocabulary is given; its groups are learned.** Each occurrence links a text to an already identified word. Texts are grouped according to their distributions over word groups, and vice versa: both groupings are learned jointly, but the words themselves are fixed.

**Instances × variables: the vocabulary units are learned too.** Instances play the role of texts, and variable parts play the role of words. These descriptive units — numerical intervals or sets of categorical values — are themselves constructed jointly with the instance groups and the groups of variable parts.


**The coclustering principle stays the same; building the vocabulary is now part of the same learning problem.**


<figure id="coclustering-comparison" style="width:100%; margin:1.5rem 0;">
  <a
    href="/assets/images/coclustering_indi_var_new_vs_words_x_IDtext.png"
    target="_blank"
    rel="noopener"
    title=""
  >
    <picture>
      <source
        srcset="/assets/images/coclustering_indi_var_new_vs_words_x_IDtext.webp"
        type="image/webp"
      >
      <img
        src="/assets/images/coclustering_indi_var_new_vs_words_x_IDtext.png"
        alt=""
        style="display:block; width:100%; height:auto;"
        loading="lazy"
      >
    </picture>
  </a>
</figure>

## Paramètres du modèle

Plutôt que de redéfinir le modèle depuis le début, nous allons partir du modèle de coclustering déjà présenté et nous concentrer uniquement sur ce que l’approche instances × variables lui ajoute. La section [*Model parameters* de la page Coclustering][coclustering-parametres] décrit un modèle sur deux variables catégorielles par quatre familles de paramètres : (i) le nombre de groupes, (ii) leur composition, (iii) les effectifs dans les coclusters et (iv) les effectifs des modalités. Le modèle instances × variables conserve cette logique, mais insère un niveau supplémentaire : **avant de regrouper les parties de variables, il faut les définir elles-mêmes !**

### Recodage des données

**Avant toute chose, les données sont recodées dans une représentation adaptée au coclustering instances × variables.** Une instance, décrite à l’origine par plusieurs variables numériques ou catégorielles, est représentée ici par une **collection d’observations** : chaque valeur $v$ observée pour une variable $X_k$ devient un triplet $(u,k,v)$, où $u$ identifie l’instance et $k$ la variable. Ainsi, une même instance génère généralement plusieurs observations. On note $M$ le nombre d’instances, $P$ le nombre de variables et $N$ le nombre total d’observations.

<figure id="coclustering-inst-var-data-recoding" style="width:75%;">
  <picture>
    <source
      srcset="/assets/images/coclustering_inst_var_data_recoding.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_inst_var_data_recoding.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>

Dans un tableau complet avec une seule valeur par variable, chaque instance génère $P$ observations et $N=M\times P$. Cette représentation permet également de gérer naturellement les valeurs manquantes, pour lesquelles aucune observation n’est créée.


Maintenant que les données sont recodées, il reste à construire le vocabulaire qui permettra de les analyser : **les parties de variables.**

### De nouveaux paramètres pour apprendre le vocabulaire

**La principale nouveauté du modèle consiste à apprendre comment découper chaque variable en parties pertinentes.** Ces parties constituent le « vocabulaire » descriptif regroupé par le coclustering.

Prenons deux variables décrivant des clients : **l’âge** et **le canal de contact**. Dans l’exemple ci-dessous, chacune est divisée en deux parties : des intervalles pour l’âge, des ensembles de modalités pour le canal.


<figure id="coclustering-inst-var-data-recoding" style="width:95%;">
  <picture>
    <source
      srcset="/assets/images/coclustering_inst_var_variable_partitions_v1.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_inst_var_variable_partitions_v1.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>

Pour chaque variable $X_k$, les notations désignent les objets visibles dans la figure :

- **$J_k$ est le nombre de parties** : ici, deux pour chaque variable.
- **$V_{k,t}$ désigne une partie** : $k$ identifie la variable et $t$ la partie.
- **$\mathcal P_k$ désigne la partition complète**, c’est-à-dire l’ensemble de ces parties :

$$
\mathcal P_k = \{V_{k,1},\ldots,V_{k,J_k}\}.
$$

Les parties ne se recouvrent pas et couvrent l’ensemble du domaine de la variable.

**Pour une variable numérique, les intervalles sont déterminés par l’ordre des rangs et les effectifs des parties.** Dans la figure, trois observations dans la première partie fixent la coupure après le troisième rang ; les cinq observations suivantes constituent la seconde partie.

Ces parties forment les unités que le coclustering regroupe sur son second axe.


### Une hiérarchie de paramètres { #hierarchie-parametres }

Comme dans le [coclustering présenté précédemment][coclustering-parametres], la description du modèle suit une hiérarchie de choix. Celle-ci fournit la trame du *prior* présenté dans la section suivante et prépare son interprétation en termes de [longueur de description][modl-information].

1. **Définir la taille du vocabulaire :** choisir le nombre de parties $J_k$ de chaque variable.
2. **Préciser les parties :** choisir les partitions $\mathcal P_k$ des variables catégorielles. Pour les variables numériques, le contenu des intervalles se déduit des effectifs introduits au point 4.
3. **Former les groupes :** choisir $K^u$ groupes d’instances et $K^p$ groupes de parties. Leur composition est décrite par les partitions $\mathcal C^u$ et $\mathcal C^p$, qui définissent respectivement les **lignes et les colonnes de la matrice de coclustering**.
4. **Décrire les effectifs d’observations :** préciser, dans la matrice $\Phi$, le nombre d’observations de chaque cocluster, puis détailler les effectifs par instance, par partie et par modalité catégorielle.

La figure reprend les quatre parties de l’exemple précédent. Elles forment ici deux groupes de parties, **chacun réunissant une partie numérique et une partie catégorielle**, croisés avec deux groupes d’instances.

<figure id="coclustering-inst-var-data-recoding" style="width:95%;">
  <picture>
    <source
      srcset="/assets/images/coclustering_inst_var_model_parameters_v1.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_inst_var_model_parameters_v1.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>


Les effectifs détaillent les totaux de la matrice à plusieurs niveaux :

- **$\delta^u$ détaille le total de chaque ligne entre ses instances** : ici, chaque client contribue deux observations.
- **$\delta^p$ détaille le total de chaque colonne entre ses parties** : dans le zoom, les huit observations de la colonne A se répartissent en trois pour la partie numérique et cinq pour la partie catégorielle.
- **$\lambda_k$ précise les effectifs des modalités de chaque variable catégorielle** : au sein de la partie contenant *Web* et *App*, les cinq observations se répartissent en trois occurrences de *Web* et deux d’*App*.

Cet ordre décrit la construction probabiliste d’un modèle ; **le découpage des variables, le regroupement de leurs parties et le regroupement des instances sont optimisés conjointement.**

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