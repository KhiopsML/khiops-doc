

**An old unresolved problem**

Before embarking on any data science project, conducting a thorough [exploratory data analysis:octicons-link-external-16:][EDA]{:target="_blank"} is essential. This initial step helps data scientists understand the underlying structure of the data, and identify potential issues related to data quality and consistency. Common methods used during *exploratory data analysis* include summary statistics, correlation analysis, scatter plots, box plots, and various data visualization techniques. Among these, *histograms* stand out as a basic and indispensable tool for univariate analysis, providing a clear visual representation of the distribution of each variable, enabling analysts to quickly grasp the shape, spread, and potential irregularities.

[EDA]: https://en.wikipedia.org/wiki/Exploratory_data_analysis

!!! example "Objective of optimal histograms"
    Provide a *clear* and *accurate* view of data distributions, even in *unexpected* cases.

Although the construction of histograms is a classical problem dating back to the early days of statistics, the challenge of accurately representing *complex* and *real-world* data distributions remains unresolved. Real-world data often deviate significantly from idealized theoretical models, exhibiting *arbitrary shapes* that are difficult to capture with simple binning strategies. Characteristics such as outliers, heavy-tailed distributions, discrete or truncated values, and multiple patterns occurring at different scales complicate the visualization process. These issues can lead to misleading or overly noisy histograms, obscuring the true underlying structure of the data. In response to these persistent challenges, the Khiops approach introduces an innovative method for constructing *optimal histograms* that effectively address these limitations[^equal_width_note]:

[^equal_width_note]: For comparison purposes, the equal-width histograms shown in the following examples use the same bins number as the corresponding optimal Khiops histograms. Only the interval boundaries differ between the two approaches.

- *The happy case of a Gaussian distribution:* This example illustrates a straightforward case where the data follow a Gaussian distribution with a mean of zero and a variance of one. Both the optimal Khiops histogram and a standard equal-width histogram are trained from a sample of 100,000 observations. While Khiops automatically determines the optimal number of bins and their widths, the equal-width method uses a fixed number of bins and divides the variable's range into equal-sized intervals. In this simple scenario, both approaches effectively capture the distribution. However, the Khiops histogram adjusts the bin widths to better reflect the data's density, resulting in a slightly more accurate representation.
   
<picture>
  <source srcset="/assets/images/histo_gaussian.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/histo_gaussian.png" alt="histo_gaussian"> 
</picture>

- *Outlier impact:* In this second example, we add an outlier with a value of 50 to the same Gaussian dataset. Outliers are common in real-world data and can greatly distort histograms. As shown, the equal-width histogram is heavily affected, reducing its ability to accurately represent the underlying distribution. In contrast, the Khiops histogram remains unaffected, maintaining the same level of detail. This illustrates that the Khiops approach is robust to such anomalies, which are often noise but can also contain valuable information. Unlike traditional methods, it does not require pre-filtering outliers, making it a more reliable tool for complex, real-world data analysis. 

<picture>
  <source srcset="/assets/images/histo_gaussian_outlier.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/histo_gaussian_outlier.png" alt="histo_gaussian_outlier"> 
</picture>

- *Multi-scale patterns:* This third example illustrates data generated from a mixture of two Gaussian distributions. The first component accounts for 95% of the observations, with a mean of zero and a variance of one, representing the main data pattern. The second component, comprising 5% of the observations, has a mean of 2 and a smaller variance of 0.1, being a secondary finer-scale pattern. As shown, the Khiops histograms effectively describe these multi-scale patterns. In contrast, the equal-width approach struggles to represent the smaller, high-density region because its fixed bin sizes cannot adjust to the different scales.

<picture>
  <source srcset="/assets/images/histo_gaussian_mixture.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/histo_gaussian_mixture.png" alt="histo_gaussian_mixture"> 
</picture>

- *Heavy-tailed distributions:* The final example illustrates a heavy-tailed distribution, specifically a [Lévy distribution:octicons-link-external-16:][levy] with a location parameter of 0 and a scale parameter of 1. Heavy-tailed patterns are common in real-world data, such as transaction amounts on e-commerce platforms or call durations in telecommunications. As shown in the following log scale figure, the Khiops histogram demonstrates an excellent ability to capture this kind of patterns. The bins vary greatly in width and count: the most prominent bin contains over 10,000 observations (10%) within a narrow width of approximately 0.12, while the rightmost bin, with an extremely large width of around 10,000, contains only 4 observations. By contrast, the equal-width approach cannot accurately represent such a distribution, concentrating 99% of the observations into a single extremely wide bin.

<picture>
  <source srcset="/assets/images/histo_levy.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/histo_levy.png" alt="histo_levy"> 
</picture>

[levy]: https://en.wikipedia.org/wiki/Lévy_distribution


While these synthetic examples highlight the strength of an adaptive binning method like Khiops to effectively describe a wide range of data distributions, real-world data often present additional challenges. 

Unlike the perfectly controlled datasets shown above, actual data is typically a *mixture* of valuable information about the *underlying distribution* and various forms of *artifacts* introduced during the process of data collection, such as noise, biases, or extraneous patterns. For example, asking individuals their age typically yields integer values, which do not perfectly reflect the continuous nature of aging, but rather a discretized *approximation* influenced by reporting *biases*. The process of *measurement* itself introduces inaccuracies. For example, weighing a whale to the nearest gram is impossible due to the limitations of measurement tools. Similarly, the act of *recording data* on a digital device imposes its own constraints. Numerical values are stored with finite precision, often rounded or truncated to fit within a fixed number of digits or bits. This illustrates that data collection can introduce patterns that are artifacts rather than true signals. On the other hand, collected data still contain valuable insights into the true distribution to be modeled.

!!! warning "Collected data may not accurately represent reality"
    The stored data may *deviate* from the true underlying distribution, embedding a layer of *extraneous patterns*, *bias* or *noise* that can obscure the genuine statistical structure of the true data. 

Therefore, it becomes essential to develop methods that can adaptively *filter out* the less relevant details while preserving the core information. This is similar to signal processing, where the signal-to-noise ratio guides the design of filters that remove unwanted noise without losing the essential features of the original signal. To address this, Khiops embodies this principle by providing a *spectrum of levels of precision* and provides a heuristic to select an appropriate level of precision, effectively filtering out irrelevant artifacts while preserving the core information.


As an example, the next figure shows three histograms built from the "Age" variable in the public dataset "Adults", where the recorded values are integers. The central histogram represents the default level of precision proposed by Khiops. To the right, the finest histogram reveals a series of peaks corresponding to the recorded integer values, while the histogram on the left displays a lower level of precision. The provided collection of histograms allows the user to explore and better understand the underlying data structure at different levels of precision. 

<picture>
  <source srcset="/assets/images/histo_accuracy_levels.webp" type="image/webp">
  <img style="max-width:1300px;width: -webkit-fill-available;" src="/assets/images/histo_accuracy_levels.png" alt="histo_accuracy_levels"> 
</picture>

The rest of this section is organized into three main sub-sections:

- **Model parameters:** describing how histogram models are defined and how bins are structured across multiple scales.  
- **Optimization criterion:** explaining the information-theoretic principle used to select the most relevant histogram.  
- **Optimization algorithm:** providing an overview of the procedure used to efficiently build the optimal histogram.

Let’s explore these components to gain a deeper understanding of how optimal histograms are constructed in practice.

##Model parameters

A histogram can be seen as a partition of the numerical axis into a set of contiguous intervals, where each interval aggregates the observations it contains. Formally, this partition is defined by a set of ordered boundaries that split the domain into \( K \) intervals. The quality of the representation directly depends on how this partition is defined: too coarse, and important structures are lost; too fine, and the histogram becomes noisy, difficult to interpret, and prone to overfitting random variations in the sample. 

In Khiops, this partition is not fixed in advance. Instead, it is *learned from the data*, allowing the histogram to adapt its resolution to the local density of observations. This leads to variable-width bins, which provide a more faithful representation of complex distributions.

To achieve this, Khiops relies on a specific construction of candidate intervals based on *floating-point bins*. These bins are inspired by the way numerical values are represented in computers, where precision is not uniform across the value range. Floating-point representations naturally define intervals of varying sizes: very fine-grained near zero, and increasingly larger as values grow. By leveraging this structure, Khiops defines a set of elementary bins that are locally regular and, at the same time, globally adapted to multiple scales.

Rather than directly defining a single partition, Khiops first constructs a *family of candidate bins*, organized into a hierarchy of resolutions indexed by a depth parameter[^floating_point_note] \( d \). Each value of \( d \) defines a specific set of bins that can be used as building blocks for the histogram. At low depth (small \( d \)), only a few large bins are available, corresponding to a coarse description of the domain. As \( d \) increases, these bins are progressively refined into smaller ones, enabling a finer description of the data.

[^floating_point_note]: In practice, the floating-point discretization model relies on several technical parameters. They are summarized here through a single resolution parameter \( d \) in order to emphasize the main intuition behind the hierarchy of candidate bins.

The figure below illustrates this hierarchy of candidate bins. Each row corresponds to a different value of \( d \), and shows the set of bins available at that level. As \( d \) increases, the number of bins grows and their width decreases. Importantly, these bins are not uniform across the axis: they adapt to the magnitude of the values, with finer resolution near zero and coarser resolution for larger values. The parameter \( d \) therefore controls the resolution of the *candidate space* from which the histogram will be constructed.

<picture>
  <source srcset="/assets/images/hierarchical_candidate-bins.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/hierarchical_candidate-bins.png" alt="floating_point_bins_hierarchy"> 
</picture>

A histogram model \( h \) is characterized by the following parameters, organized according to their hierarchical definition:

- the resolution level \( d \), which determines the set of candidate bins,
- the number of intervals \( K \),
- the set of interval boundaries \( C = \{c_1, \dots, c_{K-1}\} \), corresponding to positions within the ordered set of candidate bins available at resolution level \( d \),
- the counts \( \{h_k\}_{1 \leq k \leq K} \) of observations in each interval.

!!! example "From candidate bins to a histogram"
    A histogram model is obtained by selecting a subset of candidate bins at a given resolution level \( d \), and aggregating observations within the resulting intervals.

To illustrate these parameters, the figure below shows an example of a histogram model obtained for a given resolution level \( d \). Among all candidate bins available at this level, a subset of boundaries is selected to define \( K \) intervals. Each interval aggregates a number of observations \( h_k \), resulting in the final histogram.

<picture>
  <source srcset="/assets/images/hitogram_exemple_model.webp" type="image/webp">
  <img style="max-width:900px;width: -webkit-fill-available;" src="/assets/images/hitogram_exemple_model.png" alt="hitogram_exemple_model"> 
</picture>

In this example:

- the parameter \( d = 4 \) determines the underlying grid of candidate bins,
- the number of intervals is \( K = 3\),
- the boundaries \( C = \{5,10\} \) correspond to the selected bin limits,
- the counts \( h_k = \{100,150,50\} \) reflect the distribution of observations within each interval.

## Optimization criterion

Once the space of candidate models has been defined, the next step is to select the most most probable histogram model. This selection is performed by maximizing the posterior probability of the model using a Bayesian approach. Equivalently, this amounts to minimizing a criterion expressed as the negative logarithm of this probability. According to Bayes' rule, this criterion decomposes into two complementary terms:

\[
-\log(P(h).P(d \mid h)) = -\log P(h) - \log P(d \mid h)
\]

where \( P(h) \) is the prior probability of the model and \( P(d \mid h) \) is the likelihood of the data given the model.


**Prior.**  
The prior defines the probability distribution over models independently of the data. In the MODL framework, it follows a hierarchical construction that mirrors the hierarchy of the model parameters.
A model is generated step by step:
first a resolution level \( d \) is selected, then the number of intervals \( K \), followed by the set of boundaries \( C \), and finally the distribution of counts \( \{h_k\} \) across the intervals.

At each step, the prior is designed to remain as uniform as possible over the admissible choices. For integer parameters such as \( d \) and \( K \), this is achieved using the [Rissanen universal prior for integers:octicons-link-external-16:][rissanen_ref]{:target="_blank"}, while the remaining levels rely on uniform distributions over their corresponding configuration spaces. As a consequence, the probability of a model depends on the number of admissible configurations at each level. This leads to a prior of the following form (capturing the main intuitions of the full MODL criterion described in the original paper[^paper_ref]):



\[
-\log P(h) =
\underbrace{\log^*(d)}_{\text{level 1}}
+
\underbrace{\log^*(K)}_{\text{level 2}}
+
\underbrace{\log \binom{G_d + K - 1}{K - 1}}_{\text{level 3}}
+
\underbrace{\log \binom{N + K - 1}{K - 1}}_{\text{level 4}}
\]

where:

- \( G_d \) is the number of candidate bins at resolution level \( d \),
- \( N \) is the number of observations,
- \( \log^*(\cdot) = \log(p^*(\cdot)) \), where \( p^* \) is the [Rissanen universal prior for integers:octicons-link-external-16:][rissanen_ref]{:target="_blank"}.

[rissanen_ref]: https://projecteuclid.org/journals/annals-of-statistics/volume-11/issue-2/

Each term corresponds to a level in the hierarchical construction of the model:

- **level 1:** selecting the resolution level \( d \),
- **level 2:** choosing the number of intervals \( K \),
- **level 3:** selecting the interval boundaries \( C \) among the \( G_d \) candidate bins,
- **level 4:** distributing the \( N \) observations across the \( K \) intervals.

Because the number of possible configurations grows rapidly with model complexity, this prior naturally favors simpler models. In particular, large values of \( d \), and large numbers of intervals \( K \) are penalized through combinatorial terms.

!!! info "Why not a uniform prior for \( d \) and \( K \)?"

    A naive approach would consist in using a uniform prior over the possible values of integer parameters such as \( d \) or \( K \). However, this would require defining arbitrary upper bounds and would assign the same probability to both simple and highly complex models.

    The [universal prior:octicons-link-external-16:][rissanen_ref]{:target="_blank"}  proposed by Rissanen provides a principled alternative. It defines a probability distribution over all integers without requiring predefined bounds. It assigns higher probability to small values, while still allowing larger ones when supported by the data.

    As a result, simpler models are naturally favored, while more complex models remain accessible if they significantly improve the fit. This mechanism acts as an intrinsic regularization, without introducing any user-defined parameter.

    <picture>
      <source srcset="/assets/images/Rissanen_prior_2.webp" type="image/webp">
      <img style="max-width:400px;width: -webkit-fill-available;" src="/assets/images/Rissanen_prior_2.png" alt="Rissanen_prior" loading="lazy"> 
    </picture>

**Likelihood.**  
While the prior favors simple models, the likelihood evaluates how well a histogram describes the observed data. It measures the probability of observing the dataset given a histogram model \( h \).

The likelihood is derived from a coding perspective. Observations are first assigned to histogram intervals, then localized inside these intervals using the underlying elementary candidate bins, which define the finest level of resolution considered by the model. 
This leads to the following likelihood term:

\[
-\log P(d \mid h)
=
\underbrace{\log N! - \sum_{k=1}^{K} \log h_k!}_{\substack{\text{localization of observations}\\\text{across intervals}}}
+
\underbrace{\sum_{k=1}^{K} h_k \log G_k}_{\substack{\text{localization of observations}\\\text{inside intervals}}}
\]

where:

- \( N \) is the total number of observations,
- \( h_k \) is the number of observations in interval \( k \),
- \( G_k \) is the number of elementary candidate bins contained in interval \( k \).

The **first term** corresponds to the cost of encoding which interval contains each observation. This is a classical multinomial term: histograms with finer partitions reduce the ambiguity of this assignment, leading to a lower coding cost.

The **second term** reflects the uncertainty remaining inside each interval. Large intervals contain many elementary candidate bins and therefore provide a less precise localization of observations. Conversely, smaller intervals reduce this uncertainty by improving the precision of the representation.


!!! info "How does the model avoid overfitting?"

    Maximizing the likelihood alone would always favor increasingly complex histograms. In the extreme case, the optimal solution would consist in creating one interval per observation, perfectly fitting the training data but completely losing the ability to generalize.

    This phenomenon is known as *overfitting*: the model starts capturing random fluctuations and noise instead of the underlying statistical structure.

    The role of the prior is precisely to prevent this behavior by penalizing overly complex models. The optimal histogram therefore emerges from the balance between:
    
    - the likelihood, which favors precision,
    - and the prior, which favors simplicity.

    Because both terms originate from the same Bayesian formulation, this balance is achieved naturally without introducing any user-defined regularization parameter.


## Optimization algorithm

The optimization algorithm used for optimal histograms follows the same general strategy as the one presented in the [supervised discretization section][preprocessing]. This optimization algorithm is implemented independently of the specific criterion being optimized. In the case of histograms, the supervised criterion is simply replaced by the unsupervised MODL histogram criterion described previously.

Starting from a fine-grained initial partition, the algorithm iteratively explores merges of adjacent intervals in order to minimize the optimization criterion. Thanks to the additive structure of the criterion, local modifications can be evaluated efficiently, making the optimization tractable even on large datasets.

As in the supervised setting, the optimization procedure relies on heuristic search strategies designed to efficiently explore the space of possible partitions while maintaining a good approximation of the optimal solution. The interested reader can therefore refer to the [optimal encoding section][preprocessing] for additional details regarding the optimization framework itself.

The following animation illustrates the heuristic optimization process used to construct the final histogram from an initial fine-grained partition:

<video autoplay loop muted playsinline style="max-width:839px;width: -webkit-fill-available;">
  <source src="/assets/images/algo-discretization.mp4" type="video/mp4">
  <source src="/assets/images/algo-discretization.gif" type="image/gif" media="(not type: video/mp4)">
</video>

[preprocessing]: preprocessing.md

!!! info "Pedagogical simplification and further reading"

    This presentation intentionally focuses on the main intuitions behind the MODL histogram criterion.
    For readability, several technical aspects of the original formulation have been simplified. In particular:

    - In the prior distribution, the resolution parameter \( d \) summarizes several original parameters,
    - Several implementation details have been omitted.

    These simplifications preserve the main statistical and algorithmic intuitions while keeping the presentation accessible.
    The histogram method implemented in Khiops is described in:

    - Marc Boullé, *Floating-point histograms for exploratory analysis of large scale real-world data sets*.

    This work extends an earlier MDL histogram approach[^paper_ref2] based on regular elementary bins toward floating-point candidate bins specifically designed for exploratory analysis of real-world data.



[^paper_ref]: Marc Boullé. *Floating-point histograms for exploratory analysis of large scale real-world data sets*. 

[^paper_ref2]: Zelaya et al. *Fast and fully-automated histograms for large-scale data sets*.