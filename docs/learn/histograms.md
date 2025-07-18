
!!! warning "More details to come on this page"
    This page is currently under construction. Meanwhile, please refer to this [article][article].

[article]: http://www.marc-boulle.fr/publications/BoulleHisto2024.pdf

**Sumary of this article:**

Histograms are among the most popular methods used in exploratory analysis to summarize univariate distributions. In particular, irregular histograms are good non-parametric density estimators that require very few parameters: the number
of bins with their lengths and frequencies. Although many approaches have been proposed in the literature to infer these parameters, most existing histogram methods are difficult to exploit for exploratory analysis in the case of real-world data sets,
with scalability issues, truncated data, outliers or heavy-tailed distributions. In this paper, we focus on the G-Enum histogram method, which exploits the Minimum Description Length (MDL) principle to build histograms without any user parameter.
We then propose to extend this method by exploiting a new modeling space based on floating-point representation, with the objective of building histograms resistant to outliers or heavy-tailed distributions. We also suggest several heuristics and a
methodology suitable for the exploratory analysis of large scale real-world data sets, whose underlying patterns are difficult to recover for digitization reasons. Extensive experiments show the benefits of the approach, evaluated with a dual objective:
the accuracy of density estimation in the case of outliers or heavy-tailed distributions, and the effectiveness of the approach for exploratory data analysis.