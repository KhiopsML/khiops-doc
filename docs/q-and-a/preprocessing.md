# Preprocessing and encoding

## Does Khiops automatically apply log, square, or other transformations during variable encoding? { #discussion-634 }

### Why Are Such Transformations Unnecessary in Khiops?

Khiops does not automatically apply transformations such as logarithms, squares, or square roots based on skewness or other distributional characteristics. Instead, it uses a non-parametric, information-theoretic discretization method based on the ordering of numerical values. Therefore, explicit transformations are unnecessary for variable encoding.

Khiops employs the **MODL (Minimum Optimized Description Length)** discretization method, which ensures:

- **Optimal Binning via Information Theory**: The MODL criterion selects the best discretization scheme with the optimal number of intervals and bounds, without requiring parametric assumptions. It directly adapts to the data’s intrinsic structure.
- **Invariance to Monotonic Transformations**: Khiops encodes numerical variables using value ranks rather than raw values. Thus, monotonic transformations (log, square root, exponential, etc.) have no effect on the discretization outcome.
- **Robustness to Skewness and Outliers**: Unlike parametric approaches, Khiops does not rely on moments (mean, variance, skewness) or density estimation, making it naturally resilient to skewed distributions and outliers.
- **No Need for Normalization or Standardization**: Since Khiops operates on ranks rather than raw values, common preprocessing steps like Z-score normalization (subtracting the mean and dividing by the standard deviation) or standardization to 0-1 range, are unnecessary. Feature scaling does not impact the learning process.

### Conclusion

Transformations aimed at normalizing distributions or correcting skewness **are unnecessary** in Khiops. Its MODL-based encoding automatically adapts to the data, ensuring optimal variable encoding without manual intervention.

*Source: [discussion #634](https://github.com/orgs/KhiopsML/discussions/634)*

## How does Khiops’ prior for supervised discretization intervals work? { #discussion-993 }

### Parsimonious Prior for Interval Number in Supervised Discretization

#### Objective

The prior for model selection regarding the number of discretization intervals was designed with the following requirements:

- **Parameter-free**, being an objective rather than a subjective prior
- **Parsimonious**
- **As flat as possible**, allowing the data to speak freely
- **Monotonically decreasing** with respect to the number of intervals, favoring smaller numbers of intervals
- **Monotonically consistent** with respect to the total number of instances, to ensure consistent preferences across varying sample sizes

#### Limits of the Proposed Prior

The binomial prior based on $\binom{N-1}{I-1}$ for choosing $I-1$ cut-points among $N-1$ possible cut-points is an "intuitive" prior, but it does not meet these requirements regarding the monotonicity constraints.

As $\binom{N-1}{I-1} = \binom{N-1}{N-I}$, the prior probability increases with $I$ for $I \geq N/2$, and the prior probability for the null model ($I=1$) is exactly the same as for the overfitting model ($I=N$), with as many intervals as instances.


#### Interest of Khiops' Prior (2006)

Khiops' original prior introduced in [1] is based on $\binom{N+I-1}{I-1}$. It is inspired by the prior distribution of the $N_i$ instances per interval over $J$ classes, which exploits the number of possible multinomial parameters $\binom{N_i+J-1}{J-1}$.

#### New Khiops' Prior

A new, more parsimonious prior, not yet published, is now used in the latest versions of Khiops, for the part of the criterion related to choosing interval cut-points.
It is inspired by the problem of selecting a subset of variables from a large, potentially infinite number of variables [2] (end of Section 2.1), introduced to deal with automatic feature construction from multi-table databases.

The formula in the case of selecting $I-1$ cut-points among $N-1$ potential cut-points is:

$$\frac{(I-1)!}{(N-1)^{I-1}}$$

It meets all the requirements and is more parsimonious than Khiops' initial prior.

#### Experiments

Below are the results of some experiments showing the coding length for each prior (coding length = opposite of the logarithm of prior probabilities), for $N=20$ and $N=1000$:
- the proposed prior is parsimonious but does not meet the requirements,
- both Khiops priors meet all the requirements and are as parsimonious as the proposed prior for small numbers of intervals, up to $I \approx 0.15 N$,
- the latest Khiops prior is by far more parsimonious than the initial one for larger numbers of intervals.

<img width="420" height="250" alt="image" src="/assets/images/q-and-a/preprocessing/993-experiments-1.png">
<img width="420" height="250" alt="image" src="/assets/images/q-and-a/preprocessing/993-experiments-2.png">



#### References

[1] M. Boullé. *MODL: a Bayes optimal discretization method for continuous attributes*. Machine Learning, 65(1):131–165, 2006.
[2] M. Boullé, C. Charnay, N. Lachiche. *A scalable robust and automatic propositionalization approach for Bayesian classification of large mixed numerical and categorical data*. Machine Learning, 108(2):229–266, 2019.

*Source: [discussion #993](https://github.com/orgs/KhiopsML/discussions/993)*
