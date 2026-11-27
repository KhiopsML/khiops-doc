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

## Optimization Criterion

**The MODL principle remains the same: select the model $h$ that is most probable given the data $d$.** Following [Bayesian model selection][modl-bayes], this is equivalent to minimizing the sum of two [description lengths][modl-information]: that of the model and that of the data given the model.

$$
C(h)
=
\underbrace{-\log P(h)}_{L(h)\;:\;\text{description of the model}}
+
\underbrace{-\log P(d\mid h)}_{L(d\mid h)\;:\;\text{description of the data given the model}}.
$$

Learning the vocabulary adds choices to the model description and information to encode to recover the values or ranks of the observations.


### The Prior

**The prior follows the [parameter hierarchy](#hierarchie-parametres).** At each stage, choices compatible with the preceding choices are equally likely. Choosing among $q$ possibilities therefore costs $\log q$.

The [coclustering mechanisms][coclustering-critere] carry over to the two axes: instances and variable parts. Three additional types of choices are introduced:

- **The number of parts $J_k$.** It is chosen from $1,\ldots,|V_k|$ for a categorical variable with domain $V_k$, or from $1,\ldots,N$ for a numerical variable, where $N$ is the total number of observations. These choices are equally likely: the cost, respectively $\log|V_k|$ or $\log N$, is the same for every allowed number of parts.

- **The composition of categorical parts.** Choosing the partition $\mathcal P_k$ costs $\log B(|V_k|,J_k)$. The function $B(a,b)$ counts the partitions of $a$ elements into at most $b$ nonempty classes, following the [convention used in the previous coclustering model][coclustering-critere].

- **Value counts within parts.** For a categorical part containing $n$ observations and $r$ categorical values, the corresponding components of $\lambda_k$ specify the counts of these $r$ values, which sum to $n$. The cost is:

    $$
    \log\binom{n+r-1}{r-1}.
    $$

In the *Web/App* part of our example, there are **six possible count vectors** for the five observations, from $(0,5)$ to $(5,0)$. Describing the observed counts — three *Web* and two *App* — therefore costs $\log 6$.

For numerical variables, **no separate choice of boundaries is introduced**: the intervals are determined by the counts $\delta^p$ and the rank order.


### The Likelihood

The terms from the [previous coclustering model][coclustering-critere] describe the assignment of observations to coclusters, instances, and parts. **We still need to specify the categorical value or numerical rank of each observation within its part.**

**For a categorical part**, the value counts are already fixed by $\lambda_k$. We must now specify **which observations correspond to each value**. For a part $V_{k,t}$ containing $n$ observations, with $n_v$ occurrences of each value $v$, the cost is:

$$
\log\frac{n!}{\displaystyle\prod_{v\in V_{k,t}}n_v!}.
$$

Returning to our five observations, we know that three are *Web* and two are *App*. We still need to choose which ones are *Web*. There are $\binom{5}{3}=10$ possible assignments, at a cost of $\log 10$.

**At this level, the prior describes the counts; the likelihood describes the assignments consistent with those counts.**

**For a numerical part**, the rank interval is already determined. Assigning its $n$ distinct ranks to the $n$ observations gives $n!$ possible assignments, at a cost of:

$$
\log(n!).
$$


### The Full Criterion: Spot the Differences

Putting all the terms together gives the criterion $C(h)=L(h)+L(d\mid h)$. The additions specific to vocabulary learning are shown in blue.

To keep the notation compact, let $M$ be the number of instances, $J=\sum_k J_k$ the total number of parts, and $\mathrm{Cat}$ and $\mathrm{Num}$ the sets of indices of categorical and numerical variables.

Here, the numbers of groups $K^u,K^p$ play the roles of $J_1,J_2$ in the previous coclustering model, while the counts $\phi_{ij}$ play the role of $N_{j_1j_2}$.

#### Describing the Model — the Prior:

$$
\begin{aligned}
L(h) ={}&
{\color{blue}
\sum_{k\in\mathrm{Cat}}\log|V_k|
+
\sum_{k\in\mathrm{Num}}\log N
}
\\[0.5em]
&+
{\color{blue}
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
{\color{blue}
\sum_{k\in\mathrm{Cat}}\sum_{t=1}^{J_k}
\log\binom{\delta^p_{k,t}+|V_{k,t}|-1}
{|V_{k,t}|-1}
}.
\end{aligned}
$$

#### Describing the Data Given the Model — the Likelihood:

$$
\begin{aligned}
L(d\mid h) ={}&
\log(N!)
-
\sum_{i=1}^{K^u}\sum_{j=1}^{K^p}\log(\phi_{ij}!)
\\[0.5em]
&+ \sum_{i=1}^{K^u}\log(\phi_{i\cdot}!)
-
\sum_{\ell=1}^{M}\log(\delta_\ell^u!)
\\[0.5em]
&+ \sum_{j=1}^{K^p}\log(\phi_{\cdot j}!)
-
\sum_k\sum_{t=1}^{J_k}\log(\delta^p_{k,t}!)
\\[0.5em]
&+
{\color{blue}
\sum_{k\in\mathrm{Cat}}\sum_{t=1}^{J_k}
\log\frac{\delta^p_{k,t}!}
{\displaystyle\prod_{v\in V_{k,t}}\lambda_{k,v}!}
}
\\[0.5em]
&+
{\color{blue}
\sum_{k\in\mathrm{Num}}\sum_{t=1}^{J_k}
\log(\delta^p_{k,t}!)
}.
\end{aligned}
$$

Here, $\phi_{ij}$ is the observation count in cocluster $(i,j)$, and $\phi_{i\cdot}$ and $\phi_{\cdot j}$ are its row and column totals. The cardinalities $|\mathcal C_i^u|$ and $|\mathcal C_j^p|$ give the numbers of instances and parts in each group, respectively. Finally, $\lambda_{k,v}$ denotes the component of $\lambda_k$ associated with the categorical value $v$.

For a categorical part $V_{k,t}$, the notation used in the examples corresponds to $n=\delta^p_{k,t}$, $r=|V_{k,t}|$, and $n_v=\lambda_{k,v}$.

These expressions apply to models compatible with the data. In the count allocation terms, a class with no elements has a count of zero and, by convention, contributes zero cost.

**The formula may look daunting… but there are just five families of blue terms to spot!** These are precisely the additions we have just explained. The remaining terms use the same mechanisms as the [coclustering criterion introduced earlier][coclustering-critere], applied to instances and variable parts.

## Optimization algorithm

**When variable parts are fixed, we recover the coclustering problem introduced earlier: each observation links an instance to a part.** The algorithm therefore reuses the [MODL coclustering optimizer][coclustering-algorithme], while exploring different ways to build this vocabulary.

**A — Explore starting vocabularies.** Variables are initially partitioned at several levels of granularity, as illustrated by the two starting vocabularies for *Age* and *Channel*. For each, the optimization algorithm searches for groups of instances and groups of variable parts. The resulting models are then compared using the **full criterion**, which also accounts for the cost of defining the vocabulary. The best candidate provides the starting point for the next stage of the search.

**B — Adjust parts and groups.** The initial vocabulary can still change. The figure illustrates two local operations: moving a categorical value between parts of the same variable, or moving an entire part between groups of parts. In the latter case, the part’s content remains unchanged. Parts or groups can also be merged, and instance groups can change as well. **A change is accepted when it lowers the full criterion.**

These adjustments continue as long as a tested operation improves the model. **The vocabulary and the groups are thus optimized jointly**, using the same criterion. This optimization algorithm remains heuristic: it aims to find a good solution, without guaranteeing a global optimum.


<figure id="coclustering_inst_var_algo" style="width:100%; margin:1.5rem auto;">
  <picture>
    <source
      srcset="/assets/images/coclustering_inst_var_optimization_algorithm.webp"
      type="image/webp"
    >
    <img
      src="/assets/images/coclustering_inst_var_optimization_algorithm.png"
      alt=""
      style="display:block; width:100%; height:auto;"
      loading="lazy"
    >
  </picture>
</figure>



[^article]: A. Bouchareb, M. Boullé, F. Clérot, C. Hue et F. Rossi. *Fully Automated Co-clustering of Mixed Data Using a Maximum A Posteriori Approach*. Article fourni pour cette rédaction.

[coclustering-applications]: coclustering.md#a-wide-range-of-applications
[coclustering-parametres]: coclustering.md#model-parameters
[coclustering-critere]: coclustering.md#optimization-criterion
[coclustering-algorithme]: coclustering.md#optimization-algorithm
[modl-bayes]: modl.md#bayes
[modl-information]: modl.md#info-theory