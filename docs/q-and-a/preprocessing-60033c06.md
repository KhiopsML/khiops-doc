# Preprocessing and encoding

<a id="discussion-634"></a>
## Does Khiops automatically apply log, square, or other transformations during variable encoding?

<h3>Why Are Such Transformations Unnecessary in Khiops?</h3>
<p>Khiops does not automatically apply transformations such as logarithms, squares, or square roots based on skewness or other distributional characteristics. Instead, it uses a non-parametric, information-theoretic discretization method based on the ordering of numerical values. Therefore, explicit transformations are unnecessary for variable encoding.</p>
<p>Khiops employs the <strong>MODL (Minimum Optimized Description Length)</strong> discretization method, which ensures:</p>
<ul>
<li><strong>Optimal Binning via Information Theory</strong>: The MODL criterion selects the best discretization scheme with the optimal number of intervals and bounds, without requiring parametric assumptions. It directly adapts to the data’s intrinsic structure.</li>
<li><strong>Invariance to Monotonic Transformations</strong>: Khiops encodes numerical variables using value ranks rather than raw values. Thus, monotonic transformations (log, square root, exponential, etc.) have no effect on the discretization outcome.</li>
<li><strong>Robustness to Skewness and Outliers</strong>: Unlike parametric approaches, Khiops does not rely on moments (mean, variance, skewness) or density estimation, making it naturally resilient to skewed distributions and outliers.</li>
<li><strong>No Need for Normalization or Standardization</strong>: Since Khiops operates on ranks rather than raw values, common preprocessing steps like Z-score normalization (subtracting the mean and dividing by the standard deviation) or standardization to 0-1 range, are unnecessary. Feature scaling does not impact the learning process.</li>
</ul>
<h3>Conclusion</h3>
<p>Transformations aimed at normalizing distributions or correcting skewness <strong>are unnecessary</strong> in Khiops. Its MODL-based encoding automatically adapts to the data, ensuring optimal variable encoding without manual intervention.</p>


*Source: [discussion #634](https://github.com/orgs/KhiopsML/discussions/634)*

<a id="discussion-993"></a>
## How does Khiops’ prior for supervised discretization intervals work?

<h3>Parsimonious Prior for Interval Number in Supervised Discretization</h3>
<h4>Objective</h4>
<p>The prior for model selection regarding the number of discretization intervals was designed with the following requirements:</p>
<ul>
<li><strong>Parameter-free</strong>, being an objective rather than a subjective prior</li>
<li><strong>Parsimonious</strong></li>
<li><strong>As flat as possible</strong>, allowing the data to speak freely</li>
<li><strong>Monotonically decreasing</strong> with respect to the number of intervals, favoring smaller numbers of intervals</li>
<li><strong>Monotonically consistent</strong> with respect to the total number of instances, to ensure consistent preferences across varying sample sizes</li>
</ul>
<h4>Limits of the Proposed Prior</h4>
<p>The binomial prior based on <span class="arithmatex">\(\binom{N-1}{I-1}\)</span> for choosing <span class="arithmatex">\(I-1\)</span> cut-points among <span class="arithmatex">\(N-1\)</span> possible cut-points is an &quot;intuitive&quot; prior, but it does not meet these requirements regarding the monotonicity constraints.</p>
<p>As <span class="arithmatex">\(\binom{N-1}{I-1} = \binom{N-1}{N-I}\)</span>, the prior probability increases with <span class="arithmatex">\(I\)</span> for <span class="arithmatex">\(I \geq N/2\)</span>, and the prior probability for the null model (<span class="arithmatex">\(I=1\)</span>) is exactly the same as for the overfitting model (<span class="arithmatex">\(I=N\)</span>), with as many intervals as instances.</p>
<h4>Interest of Khiops' Prior (2006)</h4>
<p>Khiops' original prior introduced in [1] is based on <span class="arithmatex">\(\binom{N+I-1}{I-1}\)</span>. It is inspired by the prior distribution of the <span class="arithmatex">\(N_i\)</span> instances per interval over <span class="arithmatex">\(J\)</span> classes, which exploits the number of possible multinomial parameters <span class="arithmatex">\(\binom{N_i+J-1}{J-1}\)</span>.</p>
<h4>New Khiops' Prior</h4>
<p>A new, more parsimonious prior, not yet published, is now used in the latest versions of Khiops, for the part of the criterion related to choosing interval cut-points.
It is inspired by the problem of selecting a subset of variables from a large, potentially infinite number of variables [2] (end of Section 2.1), introduced to deal with automatic feature construction from multi-table databases.</p>
<p>The formula in the case of selecting <span class="arithmatex">\(I-1\)</span> cut-points among <span class="arithmatex">\(N-1\)</span> potential cut-points is:</p>
<p><span class="arithmatex">\[\frac{(I-1)!}{(N-1)^{I-1}}\]</span></p>
<p>It meets all the requirements and is more parsimonious than Khiops' initial prior.</p>
<h4>Experiments</h4>
<p>Below are the results of some experiments showing the coding length for each prior (coding length = opposite of the logarithm of prior probabilities), for <span class="arithmatex">\(N=20\)</span> and <span class="arithmatex">\(N=1000\)</span>:</p>
<ul>
<li>the proposed prior is parsimonious but does not meet the requirements,</li>
<li>both Khiops priors meet all the requirements and are as parsimonious as the proposed prior for small numbers of intervals, up to <span class="arithmatex">\(I \approx 0.15 N\)</span>,</li>
<li>the latest Khiops prior is by far more parsimonious than the initial one for larger numbers of intervals.</li>
</ul>
<img width="420" height="250" alt="image" src="/assets/images/q-and-a/preprocessing-60033c06/993-experiments-1.png">
<img width="420" height="250" alt="image" src="/assets/images/q-and-a/preprocessing-60033c06/993-experiments-2.png">
<h4>References</h4>
<p>[1] M. Boullé. <em>MODL: a Bayes optimal discretization method for continuous attributes</em>. Machine Learning, 65(1):131–165, 2006.
[2] M. Boullé, C. Charnay, N. Lachiche. <em>A scalable robust and automatic propositionalization approach for Bayesian classification of large mixed numerical and categorical data</em>. Machine Learning, 108(2):229–266, 2019.</p>


*Source: [discussion #993](https://github.com/orgs/KhiopsML/discussions/993)*
