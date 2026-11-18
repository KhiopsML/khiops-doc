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
### New Parameters for Learning the Vocabulary

**The main addition to the model is that it learns how to divide each variable into meaningful parts.** These parts form the descriptive “vocabulary” grouped by coclustering.

Consider two variables describing customers: **age** and **contact channel**. In the example below, each is divided into two parts: intervals for age and sets of categorical values for the channel.

<figure id="coclustering-variable-partitions" style="width:95%; margin:1.5rem auto;">
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

For each variable $X_k$, the notation refers to the objects shown in the figure:

- **$J_k$ is the number of parts**: here, two for each variable.
- **$V_{k,t}$ denotes a part**: $k$ identifies the variable and $t$ the part.
- **$\mathcal P_k$ denotes the complete partition**, that is, the set of these parts:

$$
\mathcal P_k = \{V_{k,1},\ldots,V_{k,J_k}\}.
$$

The parts do not overlap and together cover the variable’s entire domain.

**For a numerical variable, the intervals are determined by the rank order and the observation counts in each part.** In the figure, three observations in the first part place the boundary after the third rank; the next five observations form the second part.

These parts form the units that coclustering groups along its second axis.


### A Hierarchy of Parameters { #hierarchie-parametres }

As in the [coclustering model introduced earlier][coclustering-parametres], the model is described through a hierarchy of choices. This hierarchy forms the basis of the *prior* presented in the next section and of its interpretation in terms of [description length][modl-information].

1. **Define the vocabulary size:** choose the number of parts $J_k$ for each variable.
2. **Specify the parts:** choose the partitions $\mathcal P_k$ of the categorical variables. For numerical variables, the contents of the intervals are determined by the counts introduced in step 4.
3. **Form the groups:** choose $K^u$ instance groups and $K^p$ groups of parts. Their composition is described by the partitions $\mathcal C^u$ and $\mathcal C^p$, which define the **rows and columns of the coclustering matrix**, respectively.
4. **Describe the observation counts:** specify, in the matrix $\Phi$, the number of observations in each cocluster, then detail the counts by instance, by part, and by categorical value.

The figure reuses the four parts from the previous example. Here, they form two groups of parts, **each combining a numerical part and a categorical part**, crossed with two instance groups.

<figure id="coclustering-model-parameters" style="width:95%; margin:1.5rem auto;">
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


The counts break down the matrix totals at several levels:

- **$\delta^u$ breaks down each row total across its instances**: here, each customer contributes two observations.
- **$\delta^p$ breaks down each column total across its parts**: in the close-up, the eight observations in column A are split into three for the numerical part and five for the categorical part.
- **$\lambda_k$ gives the value counts for each categorical variable**: within the part containing *Web* and *App*, the five observations comprise three occurrences of *Web* and two of *App*.

This order describes the probabilistic construction of a model; **variable partitioning, the grouping of variable parts, and the grouping of instances are optimized jointly.**

## Critère d’optimisation

**Le principe MODL reste le même : sélectionner le modèle $h$ le plus probable sachant les données $d$.** Selon le principe de [sélection bayésienne][modl-bayes], cela revient à minimiser deux [longueurs de description][modl-information] : celle du modèle et celle des données sachant le modèle.

$$
C(h)
=
\underbrace{-\log P(h)}_{L(h)\;:\;\text{description du modèle}}
+
\underbrace{-\log P(d\mid h)}_{L(d\mid h)\;:\;\text{description des données sachant le modèle}}.
$$

L’apprentissage du vocabulaire ajoute des choix à décrire dans le modèle et des informations à coder pour retrouver les valeurs ou les rangs des observations.


### Le prior

**Le prior suit la [hiérarchie des paramètres](#hierarchie-parametres).** À chaque étape, les choix compatibles avec les précédents sont équiprobables. Choisir parmi $q$ possibilités coûte donc $\log q$.

Les [mécanismes du coclustering][coclustering-critere] se retrouvent sur les axes instances et parties de variables. Trois familles de choix supplémentaires interviennent :

- **Le nombre de parties $J_k$.** Il est choisi parmi $1,\ldots,|V_k|$ pour une variable catégorielle de domaine $V_k$, ou parmi $1,\ldots,N$ pour une variable numérique, où $N$ est le nombre total d’observations. Ces choix sont équiprobables : le coût, respectivement $\log|V_k|$ ou $\log N$, est identique pour tous les nombres de parties possible. 

- **La composition des parties catégorielles.** Choisir la partition $\mathcal P_k$ coûte $\log B(|V_k|,J_k)$. La fonction $B$ dénombre les partitions possibles selon la [convention du coclustering précédent][coclustering-critere], qui autorise des classes vides.

- **Les effectifs des modalités au sein des parties.** Pour une partie catégorielle contenant $n$ observations et $r$ modalités, les composantes correspondantes de $\lambda_k$ décrivent une répartition de ces $n$ observations entre les $r$ modalités. Son coût est :

    $$
    \log\binom{n+r-1}{r-1}.
    $$

Dans la partie *Web/App* de notre exemple, les cinq observations admettent **six répartitions d’effectifs possibles**, de $(0,5)$ à $(5,0)$. Décrire les effectifs observés — trois *Web* et deux *App* — coûte donc $\log 6$.

Pour les variables numériques, **aucun choix indépendant de bornes n’est ajouté** : les intervalles sont déterminés par les effectifs $\delta^p$ et l’ordre des rangs.


### La vraisemblance

Les termes du [coclustering précédent][coclustering-critere] décrivent l’affectation des observations aux coclusters, aux instances et aux parties. **Il reste à préciser la valeur de chaque observation à l’intérieur de sa partie.**

**Pour une partie catégorielle**, les effectifs des modalités sont déjà fixés par $\lambda_k$. Il faut maintenant préciser **quelles observations portent chaque modalité**. Pour une partie $V_{k,t}$ contenant $n$ observations, dont $n_v$ occurrences de chaque modalité $v$, le coût est :

$$
\log\frac{n!}{\displaystyle\prod_{v\in V_{k,t}}n_v!}.
$$

Reprenons nos cinq observations : nous savons qu’il y a trois *Web* et deux *App*. Il reste à choisir lesquelles portent *Web*. Il existe $\binom{5}{3}=10$ affectations possibles, pour un coût de $\log 10$.

**Le prior décrit donc les effectifs ; la vraisemblance décrit les affectations compatibles avec ces effectifs.**

**Pour une partie numérique**, l’intervalle de rangs est déjà déterminé. Associer ses $n$ rangs distincts aux $n$ observations donne $n!$ affectations possibles, pour un coût :

$$
\log(n!).
$$


### Le critère complet : jouons au jeu des différences.

En réunissant tous les termes, le critère s’écrit $C(h)=L(h)+L(d\mid h)$. Les ajouts propres à l’apprentissage du vocabulaire sont indiqués en rouge.

Pour alléger l’écriture, on note $M$ le nombre d’instances, $J=\sum_k J_k$ le nombre total de parties, et $\mathrm{Cat}$ et $\mathrm{Num}$ les ensembles d’indices des variables catégorielles et numériques.

#### Description du modèle — le prior :

$$
\begin{aligned}
L(h) ={}&
{\color{red}
\sum_{k\in\mathrm{Cat}}\log|V_k|
+
\sum_{k\in\mathrm{Num}}\log N
}
\\[0.5em]
&+
{\color{red}
\sum_{k\in\mathrm{Cat}}\log B(|V_k|,J_k)
}
\\[0.5em]
&+ \log M + \log J
\\[0.5em]
&+ \log B(M,K^u) + \log B(J,K^p)
\\[0.5em]
&+ \log\binom{N+K^uK^p-1}{K^uK^p-1}
\\[0.5em]
&+ \sum_{i=1}^{K^u}
\log\binom{\phi_{i\cdot}+|\mathcal C_i^u|-1}
{|\mathcal C_i^u|-1}
\\[0.5em]
&+ \sum_{j=1}^{K^p}
\log\binom{\phi_{\cdot j}+|\mathcal C_j^p|-1}
{|\mathcal C_j^p|-1}
\\[0.5em]
&+
{\color{red}
\sum_{k\in\mathrm{Cat}}\sum_{t=1}^{J_k}
\log\binom{\delta^p_{k,t}+|V_{k,t}|-1}
{|V_{k,t}|-1}
}.
\end{aligned}
$$

#### Description des données sachant le modèle — la vraisemblance : 

$$
\begin{aligned}
L(d\mid h) ={}&
\log(N!)
-
\sum_{i=1}^{K^u}\sum_{j=1}^{K^p}\log(\phi_{ij}!)
\\[0.5em]
&+ \sum_{i=1}^{K^u}\log(\phi_{i\cdot}!)
-
\sum_{u=1}^{M}\log(\delta_u^u!)
\\[0.5em]
&+ \sum_{j=1}^{K^p}\log(\phi_{\cdot j}!)
-
\sum_k\sum_{t=1}^{J_k}\log(\delta^p_{k,t}!)
\\[0.5em]
&+
{\color{red}
\sum_{k\in\mathrm{Cat}}\sum_{t=1}^{J_k}
\log\frac{\delta^p_{k,t}!}
{\displaystyle\prod_{v\in V_{k,t}}\lambda_{k,v}!}
}
\\[0.5em]
&+
{\color{red}
\sum_{k\in\mathrm{Num}}\sum_{t=1}^{J_k}
\log(\delta^p_{k,t}!)
}.
\end{aligned}
$$

Ici, $\phi_{ij}$ est l’effectif du cocluster $(i,j)$, et $\phi_{i\cdot}$ et $\phi_{\cdot j}$ sont les totaux de sa ligne et de sa colonne. Les cardinalités $|\mathcal C_i^u|$ et $|\mathcal C_j^p|$ comptent respectivement les instances et les parties de chaque groupe. Enfin, $\lambda_{k,v}$ désigne la composante de $\lambda_k$ associée à la modalité $v$.

**La formule a de quoi impressionner… mais le jeu des différences tient en cinq familles de termes rouges !** Ce sont précisément les ajouts que nous venons d’expliquer. Les autres termes reprennent les mécanismes du [critère de coclustering déjà présenté][coclustering-critere], appliqués aux instances et aux parties de variables.


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