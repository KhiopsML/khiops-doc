# Coclustering

## What is the difference between Variable x Variable \(VxV\) and Instances x Variables \(IxV\) coclustering? { #discussion-1184 }

### Khiops coclustering

#### Variable x Variable (VxV) Coclustering

A co-clustering of variable x variable involves two or more dimensions, one for each variable.

Each variable is partitioned into intervals (for numerical variables) or groups of values (for categorical variables).
The entire data space is then partitioned into a grid of co-clusters, resulting from the cross-product of the univariate partitions.

This results in density estimation models, assuming the density is constant within each co-cluster.

#### Instances x Variables (IxV) Coclustering

A co-clustering of instances x variables involves two dimensions:

- A dimension for the instances

- A dimension for variable parts

This second dimension corresponds to the set of variables describing each instance: these are the inner variables, specific to this dimension.
Each inner variable is partitioned into a set of variable parts, which serve as the vocabulary used to describe each instance.

Thus, on one hand, we have a partition of the instances, and on the other hand, a partition of the variable parts. The co-clustering of instances x variables tends to group instances into clusters if they are described by the same variable parts.

This approach is analogous to text x word co-clustering, where texts are grouped into clusters if they are described by the same clusters of words.

#### Takeaway

- **Variable x Variable Coclustering**
    - Objective: joint density estimation
    - Suitable for datasets with two variables, or a few variables (typically less than 10)
    - Relevant for comparison with alternative clustering approaches on bivariate toy datasets

- **Instances x Variables Coclustering**
    - Objective: provide a meaningful summary of the dataset by describing each cluster of instances with representative variable parts
    - Similar to text x word coclustering, where each text cluster is characterized by its distribution over word clusters
    - Not suitable for datasets with very few variables; typically, two variables are too few

- Both methods focus on intrinsic correlations across variables, invariant to any monotonous transformation of the data

- Sometimes, in bivariate datasets, visually natural clusters can be explained solely by the marginal distributions of each variable, even when the variables are uncorrelated.

- These methods are particularly valuable when the data exhibits complex density structures or smooth transitions between dense regions, where traditional clustering may fail or be less meaningful.

- When the data is inherently cluster-based, both clustering and coclustering approaches tend to produce comparable results, especially focusing on dense coclusters.

*Source: [discussion #1184](https://github.com/orgs/KhiopsML/discussions/1184)*

## How do VxV and IxV coclustering compare on simple bivariate patterns? { #discussion-1185 }

### Study: VxV versus IxV coclustering

Both coclustering approaches can be applied to the same data.

In particular, in the bivariate case, it is tempting to use samples where clusters can be easily identified by humans, and to compare the results obtained by both approaches.

In this study, we apply both approaches to a series a bivariate patterns and analyse the results.

Python script for the study: `khiops_coclustering_study.py`

[khiops_coclustering_study.py](/assets/discussion-scripts/q-and-a/coclustering/1185-study-vxv-versus-ixv-coclustering-1.py)

#### Datasets

We generate datasets using the `make_blobs` function from the Python Scikit-learn library which creates a list of isotropic Gaussian blobs with a standard deviation of 1.

Each dataset contains 1,000 points for two numerical variables, `a` and `b`, displayed using scatterplots, with `a` on the X-axis and `b` on the Y-axis.

Since Khiops coclustering models operate using the ranks of values rather than the raw values,
making the results invariant to any monotonic transformation of the data, we also display scatterplots based on the ranks of the values to facilitate the interpretation of the coclustering results.

The following patterns are used in this study:

- Circle: blob centered at [0, 0]

- TriangleU: blobs centered at [10, 10], [-10, 10], [0, 0]

- TriangleL: blobs centered at [10, 0], [0, 10], [0, 0]

- Diagonal: blobs centered at [-10, -10], [0, 0], [10, 10]

- NoisyDiagonal: blobs centered at [-3, -3], [0, 0], [3, 3]

- NoisyDiagonal: blobs centered at [-2, -2], [0, 0], [2, 2]

- Square: blobs centered at [10, 10], [-10, -10], [10, -10], [-10, 10]

- Checkers: blobs centered on a 10 x 10 grid, with centers at [10i, 10j] for even (i + j)

- NoisyCheckers: blobs centered on a 10 x 10 grid, with centers at [3i, 3j] for even (i + j)

#### Circle

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-circle-1.png">

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-circle-2.png">

Both approaches fail to detect any meaningful information. More specifically, during the model optimization process, no explored model performs significantly better than the null model, which assumes independence between the two variables.

This is consistent with the data distribution, which is based on a single isotropic Gaussian distribution.
The plot, based on a rank-based normalization of the values, visually aligns with the assumption of two independent variables.

This bivariate distribution can be explained by the marginal Gaussian distributions of `a` and `b` (see below), with no correlation between the two variables.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-circle-3.png">

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-circle-4.png">

#### TriangleU

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-triangleu-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-triangleu-2.png">

The VxV approach correctly identifies the pattern consisting of three dense coclusters, with `a` partitioned into three intervals and `b` into two intervals.
There is actually a good match between these dense coclusters and the natural clusters visually distinguishable in the scatterplots.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-triangleu-3.png">


Surprisingly, the IxV approach only retrieves two clusters of instances, with `a` partitioned into five intervals and `b` into three intervals.

<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-triangleu-4.png">

The coclusters have a fundamentally different nature, as they relate to clusters of instances correlated with clusters of intervals.
In fact, the two dense coclusters can be summarized as follows:

- First dense cocluster
    - Relates to either small or large values of a and large values of b
    - Corresponds to the two upper natural clusters of the displayed pattern

- Second dense cocluster
    - Relates to medium values of a and small values of b
    - Corresponds to the lower natural cluster of the displayed pattern

This dataset summary makes sense, but the fact that the two upper clusters are not separated is somewhat surprising.


##### The Limits of IxV Coclustering

The behavior can actually be explained with some deeper insight into this type of model.

In IxV coclustering, let's call **inner variable** the variables that describe each instance.

An IxV coclustering can be viewed as a VxV coclustering related to two categorical variables:

- The first variable, `Id`, represents the instances, with one distinct value per instance: the instance identifier.

- The second variable, `VarPart`, represents the inner variable parts, with one value per part of each inner variable.

- There is one observation per instance and per inner variable.

In our previous example, we have:

- The `Id` variable with 1,000 distinct values.

- The `VarPart` variable with 8 distinct values, related to the five intervals of a and the three intervals of b.

- Altogether, there are 2,000 observations, given the values of the two inner variables describing each instance.

The objective of IxV coclustering is thus to partition a contingency table of size 1,000 x 8, containing a total of 2,000 observations, where each value of the Id variable has only two observations.

The average expected frequency for each cell is approximately 2,000 / (1,000 * 8) ~ 0.25.

For comparison, consider the chi-square test of independence applied to contingency tables.
Small expected frequencies lead to poor approximation of the chi-square distribution of the test statistic.
A general rule of thumb is to have at least 5 as the smallest expected frequency in each cell.

In our case, the expected cell frequency of 0.25 is far too low to obtain an accurate model.

The IxV coclustering obtained under these conditions cannot be highly accurate, given the tiny number of observations per instance.
However, it still provides a meaningful summary of the data, making the best use of the available data while avoiding overfitting.

##### The Limits of VxV Coclustering

VxV coclustering yields accurate results in the case of two variables. \
It can be applied to datasets with more than two variables, but this introduces new challenges.

Suppose you have a dataset with `n` instances and `k` variables, each partitioned into only two parts, intervals or groups of values. \
The VxV coclustering resulting from the cross-product of the univariate partitions contains \(2^k\) coclusters. \

For example, with `n` = 1,000 instances and `k` = 10 variables, we obtain \(2^10 = 1024\) coclusters, which means on average less than one observation per cocluster.
With such a sparsity, there is not enough data to produce a model better than the null model, which consists of a single cocluster.

Overall, no meaningful information can be retrieved using a VxV coclustering model when the number of variables becomes too high, typically beyond around \(log_2(n)\).

#### TriangleL

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-trianglel-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-trianglel-2.png">

As with the TriangleU pattern, the VxV approach correctly identifies the pattern consisting of three dense coclusters.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-trianglel-3.png">

Once again, the IxV approach only retrieves two clusters of instances, with `a` and `b` each partitioned into two intervals.

<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-trianglel-4.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-trianglel-5.png">

The two clusters obtained are of even poorer quality than before. \
Looking at the rank-based scatterplot, we understand that `a` is partitioned into two equal-frequency intervals, and `b` exploits quartiles, with the second interval corresponding to the last quartile.
This aligns with the optimization algorithm, which explores a series of starting solutions with univariate preprocessing based on 2, 4, 8, ... equal-frequency partitions.

Given this pattern and only two observations per instance, these raw results are probably the most accurate possible given the data and the limitations of the optimization algorithm.
IxV models are definitely not suitable for datasets with only two variables.

#### Diagonal

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-diagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-diagonal-2.png">

This pattern consists of three diagonal blobs, with highly correlated variables. \
It is easier than the triangle patterns and is easily retrieved by both the VxV and IxV approaches.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-diagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-diagonal-4.png">


#### NoisyDiagonal

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisydiagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisydiagonal-2.png">

This pattern is similar to the diagonal pattern, with closer blobs.
Like the diagonal pattern, it is correctly identified by both the VxV and IxV approaches.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisydiagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisydiagonal-4.png">

Note that the clusters are less separable than in the diagonal pattern.

- With the VxV coclustering, the three original blobs are primarily identified within the three dense diagonal coclusters, derived from the 25 coclusters resulting from a 5 x 5 intervals coclustering.

- Similarly, with the IxV coclustering, three clusters of instances are identified, also based on a 5 x 5 partition of variables a and b.

- These methods are particularly valuable when the data exhibits complex density structures or smooth transitions between dense regions, where traditional clustering may fail or be less meaningful.

It is noteworthy that the objective of both coclustering approaches is to estimate piecewise constant densities within each cocluster.
Contrary to traditional clustering methods, clusters are only a by-product of the approach: only dense coclusters can be interpreted as traditional clusters.


#### BlurredDiagonal

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-blurreddiagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-blurreddiagonal-2.png">

The three blobs are even closer than before, resulting in visually indistinguishable clusters.

The VxV coclustering correctly retrieves the joint density, although the connection between dense coclusters and clusters has disappeared.
The IxV coclustering provides a rough estimation of the joint density, using two clusters of instances.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-blurreddiagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-blurreddiagonal-4.png">

Note that assuming data can be decomposed into distinct clusters is a strong hypothesis, which often does not hold for many real datasets where there is a smooth transition between dense regions.
In such cases, traditional clustering methods may not be appropriate or effective.
In contrast, density-based coclustering approaches aim to provide a summary of the dataset through piecewise constant estimation of the joint density. These methods are applicable regardless of the underlying distribution.
When the data is inherently cluster-based, both clustering and coclustering approaches are more likely to produce comparable results, with a particular emphasis on the dense coclusters identified by the coclustering methods.

#### Square

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-square-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-square-2.png">

Surprisingly, the four _natural_ clusters, visually distinguishable in the scatterplots, are not retrieved by either the VxV or the IxV approaches.

In fact, as shown in the rank-based scatterplot, the two variables `a` and `b` are perceived as independent, and no correlation pattern can be identified. \
The visual pattern can be much more simply explained by the marginal distributions of `a` and `b`, each having two modes, resulting in a bivariate scatterplot that appears as four clusters.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-square-3.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-square-4.png">

It is important to remember that coclustering models seek correlation patterns that are invariant to any monotonic transformation of the data. \
Therefore, some visual bivariate patterns may sometimes appear due to strong patterns in the marginal distributions of the variables, even when the variables are uncorrelated.


#### Checkers

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-checkers-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-checkers-2.png">

This complex pattern is correctly retrieved using the VxV approach.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-checkers-3.png">

As expected, the IxV approach cannot retrieve such a complex pattern given the very few observations per instance.


#### NoisyCheckers

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisycheckers-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisycheckers-2.png">

This complex and noisy pattern is also correctly retrieved using the VxV approach. It is all the more remarkable that the underlying pattern is hardly visually distinguishable in the scatterplots. \

This is close to the limit of reliable detection of correlation patterns, especially since the method is regularized against overfitting, preventing it from retrieving patterns in the case of independent variables.

<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering/1185-noisycheckers-3.png">

As expected, the IxV approach cannot retrieve such a complex pattern given the very few observations per instance.

*Source: [discussion #1185](https://github.com/orgs/KhiopsML/discussions/1185)*

## Why does VxV coclustering become sparse in higher dimensions, and what protects IxV? { #discussion-1186 }

### Clarification on Coclustering Approaches and Sparsity Issues

V×V coclustering partitions each input variable and exploits the cross-product of all partitioned dimensions. Because its size grows exponentially with the number of variables, it can lead to extreme sparsity. I×V coclustering does not implicitly face the same combinatorial explosion for the following reasons:

#### Data in a k-dimensional space

When data is defined in a **k-dimensional space** (e.g., numerical space), if the space is **fully populated**, nothing can be learned.

##### Extreme cases:

- **k independent variables:** \
  Both coclustering approaches, **VxV** and **IxV**, result in the null model because the variables are independent.

- **k identical variables:** \
  The dependency pattern is straightforward, as the data lies on a manifold of dimension 1. \
    - The **VxV** approach describes the data in its full k-dimensional space. \
    - The **IxV** approach seeks clusters located on the data manifold, summarizing them by partitioning each dimension.

#### The case of k identical variables

##### VxV Coclustering Approach

- There are **n observations** in **k dimensions**. \
- Describing the position of each observation in the k-dimensional space is costly. \
- For example, splitting each dimension into **I** equal intervals results in **$I^k$** coclustering cells. \
- To describe **n** instances, a multinomial distribution with **$I^k$** outcomes is needed, with zero probability everywhere except for **I** outcomes.
- This limits the precision of data summarization, especially as **k** increases (curse of dimensionality).

##### IxV Coclustering Approach

- There are **n * k observations**, each represented as a pair **(instance, variable value)** in 2D space. \
- Splitting each dimension into **I** parts results in:
    - **I** clusters of instances, \
    - **I** clusters of variable parts, \
    - and a multinomial distribution with **$I^2$** outcomes to describe the data, with zero probability everywhere except for **I** outcomes.
- This approach effectively captures strong dependencies across variables in a parsimonious way.

##### Experimental Illustration

We consider datasets with **2, 4, 8** numerical variables uniformly distributed on [0, 1], generated with sizes from **2 to 1024** (powers of two). Each experiment is repeated 10 times.

###### **VxV coclustering** Results:
<img width="320" height="240" alt="VxV_Simulation_False_NUM_MeanPartitionSize" src="/assets/images/q-and-a/coclustering/1186-vxv-coclustering-results-1.png"> <img width="320" height="240" alt="VxV_Simulation_False_NUM_VarNumber" src="/assets/images/q-and-a/coclustering/1186-vxv-coclustering-results-2.png">

Synthesis:
    - When data is small, the null model (single part per variable) is optimal. \
    - With more data, models improve, but the number of parts per variable increases slowly. \
    - For **8 variables**, at least **128 instances** are needed to exploit all variables. \
    - The mean number of parts per variable increases with data size but suffers from the curse of dimensionality (up to 20 parts for 2 variables, but only 3 for 8 variables).

###### **IxV coclustering**  results:

<img width="320" height="240" alt="Simulation_False_NUM_MeanPartitionSize" src="/assets/images/q-and-a/coclustering/1186-ixv-coclustering-results-1.png">

Synthesis:
    - When data is small, the null model (single part per variable and single cluster per dimension) is optimal.
    - Performs less accurately with only **2 variables** (only 2 observations per instance), and poorly in the case of more complex patterns.
    - With **1000 instances**, it builds more than **30 parts per variable**, more than ten times the VxV approach for the same number of variables.

#### Summary

- **VxV coclustering:** \
  Describes the data manifold in **k-dimensional space**. \
    - The data size must grow exponentially with **k** due to the curse of dimensionality.
    - Suitable for **small dimensions**. \

- **IxV coclustering:** \
  Focuses on the **intrinsic dimension** of the data manifold. \
    - Suitable for manifold of intrinsic dimension far less than **k**, summarizing it via instance clusters and variable parts.

Estimating joint density remains challenging. If the **intrinsic dimension** of the manifold is too high, **nothing** can be effectively learned, regardless of the modeling approach.

*Source: [discussion #1186](https://github.com/orgs/KhiopsML/discussions/1186)*

## What does an IxV coclustering analysis look like on a real dataset \(Iris\)? { #discussion-1187 }

### Exploratory analysis of the Iris dataset using Instances x Variables Coclustering

We present an exploratory analysis of the Iris dataset using Instances x Variables Coclustering.

Python script for the study: iris_coclustering_study.py

[iris_coclustering_study.py](/assets/discussion-scripts/q-and-a/coclustering/1187-exploratory-analysis-of-the-iris-dataset-using-instances-x-v-1.py)

#### Iris dataset

The Iris dataset consists of 150 instances of flowers, described by one categorical variable, **Class**, and four numerical variables, **PetalLength**, **PetalWidth**, **SepalLength**, **SepalWidth**.

The **Class** variable has three values: `Iris-setosa`, `Iris-versicolor` and `Iris-virginica`.

Below is an extract from this dataset.

| Class           |PetalLength | PetalWidth | SepalLength | SepalWidth |
|-----------------|------------|------------|-------------|------------|
| Iris-setosa     | 1.4        | 0.2        | 5.1         | 3.5        |
| Iris-setosa     | 1.5        | 0.2        | 4.6         | 3.1        |
| Iris-versicolor | 4.7        | 1.4        | 7.0         | 3.2        |
| Iris-versicolor | 3.9        | 1.4        | 5.2         | 2.7        |
| Iris-virginica  | 6.0        | 2.5        | 6.3         | 3.3        |
| Iris-virginica  | 5.1        | 1.9        | 5.8         | 2.7        |
| ...             | ...        | ...        | ...         | ...        |

#### Instances x Variables Coclustering

A co-clustering of instances x variables involves two dimensions:

- A dimension for the instances

- A dimension for variable parts

This second dimension corresponds to the set of variables describing each instance: these are the inner variables, specific to this dimension.
Each inner variable is partitioned into a set of variable parts, which serve as the vocabulary used to describe each instance.

Thus, on one hand, we have a partition of the instances, and on the other hand, a partition of the variable parts. The co-clustering of instances x variables tends to group instances into clusters if they are described by the same variable parts.

This approach is analogous to text x word co-clustering, where texts are grouped into clusters if they are described by the same clusters of words.

#### IxV Coclustering of the Iris dataset


The IxV coclustering optimize the following model parameters:

- Partition of the variables

- Clusters of instances

- Clusters of variable parts

- Coclusters

##### Partition of the Variables

The descriptive variables are partitioned as follows:

| Variable        | Type        | Parts  | Partition                                                                       | Frequencies         |
|---------------|-----------|--------|----------------------------------------------------------|--------------------|
| **Class**       | Categorical | 3      |\{Iris-setosa\} <br> \{Iris-versicolor\} <br> \{Iris-virginica\} | 50 <br> 50 <br> 50 |
| **PetalLength** | Numerical   | 3      | ]-inf, 2.4] <br> ]2.4, 4.75] <br> ]4.75, +inf[  | 50 <br> 55 <br> 45 |
| **PetalWidth**  | Numerical   | 3      | ]-inf, 0.8] <br> ]0.8, 1.75] <br> ]1.75, +inf[  | 50 <br> 46 <br> 54 |
| **SepalLength** | Numerical   | 3      |]-inf, 5.45] <br> ]5.45, 6.85] <br> ]6.85, +inf[ | 52 <br> 17 <br> 81 |
| **SepalWidth**  | Numerical   | 2      |]-inf, 3.35] <br> ]3.35, +inf[                   | 36 <br> 114        |

Given these partitions, the original Iris instances can be considered as text documents, described by words based on variable parts.

| Instance | Class               | PetalLength   | PetalWidth    | SepalLength    | SepalWidth    |
|----------|---------------------|---------------|---------------|----------------|---------------|
| 1        | \{Iris-setosa\}     | ]-inf, 2.4[   | ]-inf, 0.8[   | ]-inf, 5.45[   | ]3.35, +inf[  |
| 2        | \{Iris-setosa\}     | ]-inf, 2.4[   | ]-inf, 0.8[   | ]-inf, 5.45[   | ]-inf, 3.35[  |
| 3        | \{Iris-versicolor\} | ]2.4, 4.75[   | ]0.8, 1.75[   | ]6.85, +inf[   | ]-inf, 3.35[  |
| 4        | \{Iris-versicolor\} | ]2.4, 4.75[   | ]0.8, 1.75[   | ]-inf, 5.45[   | ]-inf, 3.35[  |
| 5        | \{Iris-virginica\}  | ]4.75, +inf[  | ]1.75, +inf[  | ]5.45, 6.85]   | ]-inf, 3.35[  |
| 6        | \{Iris-virginica\}  | ]4.75, +inf[  | ]1.75, +inf[  | ]5.45, 6.85]   | ]-inf, 3.35[  |
| ...      | ...                 | ...           | ...           | ...            | ...           |

##### Clusters of instances and of variables parts

Given the new description of the instances, the instances are partitionned into clusters on one dimension, and the variable parts are partitioned into clusters of variables part in the other dimension of the coclustering.

There are three clusters of instances.

| Cluster | Frequency |
|---------|-----------|
| `Ci1`   | 50        |
| `Ci2`   | 50        |
| `Ci3`   | 50        |

And four clusters of variable parts.

| Cluster | Variable parts | Frequencies |
|---------|----------------------|------------|
| `Cvp1`    | Class \{Iris-setosa\} <br> PetalLength ]-inf, 2.4] <br> PetalWidth ]-inf, 0.8] <br> SepalLength ]-inf, 5.45] <br> SepalWidth ]3.35, +inf[ | 50 <br> 50 <br> 50 <br> 52 <br> 36 |
| `Cvp2`    | Class {Iris-virginica} <br> PetalLength ]4.75, +inf[ <br> PetalWidth ]1.75, +inf[ <br> SepalLength ]6.85, +inf[ | 50 <br> 55 <br> 46 <br> 17      |
| `Cvp3`    | Class {Iris-versicolor} <br> PetalLength ]2.4, 4.75] <br> PetalWidth ]0.8, 1.75] | 50 <br> 45 <br> 54     |
| `Cvp4`    | SepalLength ]5.45, 6.85] <br> SepalWidth ]-inf, 3.35] | 81 <br> 114      |

##### Coclusters

We have a total of 5 observations per instance, one for each variable (e.g., (`1`, `SepalLength ]-inf, 5.45[`)), which gives 150 * 5 = 750 observations.

These 750 observations are distributed across the 3 x 4 coclustering matrix, with the following frequencies per cocluster:

|	     | `Cvp1` | `Cvp2` | `Cvp3` | `Cvp4` |
|--------|--------|---------|--------|--------|
| `Ci1`    | 8        |   8        | 144     | 90       |
| `Ci2`    | 5        |  160     | 5         | 80       |
| `Ci3`    | 225    |   0        | 0         | 25       |


##### Interpretation using Dense Coclusters

<img width="600" height="350" alt="Image" src="/assets/images/q-and-a/coclustering/1187-interpretation-using-dense-coclusters-1.png">

The coclustering matrix exhibits significant contrasts compared to the case where instances and variable parts are independent.

It is visualized below with colors assigned according to the contribution to the mutual information between the two dimensions:

- Red for dense coclusters, where the observed frequency is above the expected frequency under independence,

- Blue when the observed frequency is below the expected frequency,

- White when the observed frequency is very small or close to the expected frequency.

In the case of the Iris dataset, there is one dense cocluster per cluster of instances, which facilates their interpretation.

- `Ci1` contains 50 instances, over-represented across  the variables parts
    - Class {Iris-versicolor}
    - PetalLength ]2.4, 4.75]
    - PetalWidth ]0.8, 1.75]
- `Ci2` contains 50 instances, over-represented across  the variables parts
    - Class {Iris-virginica}
    - PetalLength ]4.75, +inf[
    - PetalWidth ]1.75, +inf[
    - SepalLength ]6.85, +inf[
- `Ci3` contains 50 instances, over-represented across  the variables parts
    - Class \{Iris-setosa\}
    - PetalLength ]-inf, 2.4]
    - PetalWidth ]-inf, 0.8]
    - SepalLength ]-inf, 5.45]
    - SepalWidth ]3.35, +inf[

Overall, we can summarize the Iris dataset using three clusters, focusing on the variables Class, PetalLength, and PetalWidth.
The first cluster mainly consists of flowers of class Iris-versicolor, with medium-sized petals.
The second cluster consists primarily of flowers of class Iris-virginica, with large petals.
The third cluster includes flowers of class Iris-setosa, with small petals.

The last two variables SepalLength and SepalWidth are less important for characterizing the clusters.

##### Additional Visual Evidence for Cluster Interpretation

<img width="600" height="500" alt="Image" src="/assets/images/q-and-a/coclustering/1187-additional-visual-evidence-for-cluster-interpretation-1.png">

We present a scatter plot of the most explanatory variables, with **PetalWidth** on the X-axis, **PetalLength** on the Y-axis, and shapes used to indicate the **Class** of each instance.
The intervals of these two variables are represented by vertical or horizontal dashed lines.
Each dot corresponds to an instance, with the color indicating the cluster to which the instance belongs.
This scatter plot demonstrates a good alignment between the clusters and the variable parts associated with these explanatory variables.

<img width="600" height="500" alt="Image" src="/assets/images/q-and-a/coclustering/1187-additional-visual-evidence-for-cluster-interpretation-2.png">

We also show a scatter plot using the less important variables **SepalWidth** and **SepalLength**.
In this case, the correspondence between the clusters and SepalLength and SepalWidth is much less clear, as indicated by the dataset summary provided through the IxV coclustering.

##### Relation with Variable x Variable Coclustering

##### VxV Coclustering

Variable x Variable Coclustering involves two or more dimensions, one for each variable.
Each variable is partitioned into intervals (for numerical variables) or groups of values (for categorical variables).
The entire data space is then partitioned into a grid of co-clusters, resulting from the cross-product of the univariate partitions.
This results in density estimation models, assuming the density is constant within each co-cluster.

##### Bivariate analysis

In the case of bivariate analysis, VxV coclustering provides a reliable and accurate joint density estimator.
For the Iris dataset, some VxV coclustering results are based on up to 4 parts per variable.

Conversely, IxV coclustering is not suitable when only two variables are involved, as it results in only two observations per instance.
This is insufficient for accurate density estimation, and IxV coclustering systematically uses fewer parts.

##### Multivariate analysis

With more variables, the IxV coclustering approach offers a good summary of the dataset, as demonstrated in the exploratory study of the Iris dataset.

In contrast, VxV coclustering suffers from sparsity as the number of variables increases.
For example, with only two parts per variable and `k` variables, the resulting coclustering consists of `2^k` coclusters.
Furthermore, visualization tools become much more difficult to utilize with more than two dimensions.

In the case of the Iris dataset, VxV coclustering results in a 3 x 3 x 3 x 2 x 1 cocluster grid, with SepalWidth partitioned into a single interval.
This can be compared to IxV approaches, which build 3 clusters of instances distributed across 4 clusters of variable parts, based on 3, 3, 3, 3, and 2 parts per variable, offering a finer partitioning of the descriptive variables.

##### Key Takeaways

**VxV coclustering** provides detailed joint density estimates, but the quality of the estimation decreases with data sparsity as the number of variables increases.
Additionally, the usefulness of visualization tools diminishes with higher dimensions.

**IxV coclustering** offers a robust summary of datasets, especially when there are a sufficient number of variables.
However, it is not suitable for precise density estimation in bivariate cases.

*Source: [discussion #1187](https://github.com/orgs/KhiopsML/discussions/1187)*
