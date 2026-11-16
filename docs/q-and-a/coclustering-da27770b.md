# Coclustering

<a id="discussion-1184"></a>
## What is the difference between Variable x Variable \(VxV\) and Instances x Variables \(IxV\) coclustering?

<h3>Khiops coclustering</h3>
<h4>Variable x Variable (VxV) Coclustering</h4>
<p>A co-clustering of variable x variable involves two or more dimensions, one for each variable.</p>
<p>Each variable is partitioned into intervals (for numerical variables) or groups of values (for categorical variables).
The entire data space is then partitioned into a grid of co-clusters, resulting from the cross-product of the univariate partitions.</p>
<p>This results in density estimation models, assuming the density is constant within each co-cluster.</p>
<h4>Instances x Variables (IxV) Coclustering</h4>
<p>A co-clustering of instances x variables involves two dimensions:</p>
<ul>
<li>
<p>A dimension for the instances</p>
</li>
<li>
<p>A dimension for variable parts</p>
</li>
</ul>
<p>This second dimension corresponds to the set of variables describing each instance: these are the inner variables, specific to this dimension.
Each inner variable is partitioned into a set of variable parts, which serve as the vocabulary used to describe each instance.</p>
<p>Thus, on one hand, we have a partition of the instances, and on the other hand, a partition of the variable parts. The co-clustering of instances x variables tends to group instances into clusters if they are described by the same variable parts.</p>
<p>This approach is analogous to text x word co-clustering, where texts are grouped into clusters if they are described by the same clusters of words.</p>
<h4>Takeaway</h4>
<ul>
<li>
<p><strong>Variable x Variable Coclustering</strong></p>
<ul>
<li>Objective: joint density estimation</li>
<li>Suitable for datasets with two variables, or a few variables (typically less than 10)</li>
<li>Relevant for comparison with alternative clustering approaches on bivariate toy datasets</li>
</ul>
</li>
<li>
<p><strong>Instances x Variables Coclustering</strong></p>
<ul>
<li>Objective: provide a meaningful summary of the dataset by describing each cluster of instances with representative variable parts</li>
<li>Similar to text x word coclustering, where each text cluster is characterized by its distribution over word clusters</li>
<li>Not suitable for datasets with very few variables; typically, two variables are too few</li>
</ul>
</li>
<li>
<p>Both methods focus on intrinsic correlations across variables, invariant to any monotonous transformation of the data</p>
</li>
<li>
<p>Sometimes, in bivariate datasets, visually natural clusters can be explained solely by the marginal distributions of each variable, even when the variables are uncorrelated.</p>
</li>
<li>
<p>These methods are particularly valuable when the data exhibits complex density structures or smooth transitions between dense regions, where traditional clustering may fail or be less meaningful.</p>
</li>
<li>
<p>When the data is inherently cluster-based, both clustering and coclustering approaches tend to produce comparable results, especially focusing on dense coclusters.</p>
</li>
</ul>


*Source: [discussion #1184](https://github.com/orgs/KhiopsML/discussions/1184)*

<a id="discussion-1185"></a>
## How do VxV and IxV coclustering compare on simple bivariate patterns?

<h3>Study: VxV versus IxV coclustering</h3>
<p>Both coclustering approaches can be applied to the same data.</p>
<p>In particular, in the bivariate case, it is tempting to use samples where clusters can be easily identified by humans, and to compare the results obtained by both approaches.</p>
<p>In this study, we apply both approaches to a series a bivariate patterns and analyse the results.</p>
<p>Python script for the study: <code>khiops_coclustering_study.py</code></p>
<p><a href="/assets/discussion-scripts/q-and-a/coclustering-da27770b/1185-study-vxv-versus-ixv-coclustering-1.py">khiops_coclustering_study.py</a></p>
<h4>Datasets</h4>
<p>We generate datasets using the <code>make_blobs</code> function from the Python Scikit-learn library which creates a list of isotropic Gaussian blobs with a standard deviation of 1.</p>
<p>Each dataset contains 1,000 points for two numerical variables, <code>a</code> and <code>b</code>, displayed using scatterplots, with <code>a</code> on the X-axis and <code>b</code> on the Y-axis.</p>
<p>Since Khiops coclustering models operate using the ranks of values rather than the raw values,
making the results invariant to any monotonic transformation of the data, we also display scatterplots based on the ranks of the values to facilitate the interpretation of the coclustering results.</p>
<p>The following patterns are used in this study:</p>
<ul>
<li>
<p>Circle: blob centered at [0, 0]</p>
</li>
<li>
<p>TriangleU: blobs centered at [10, 10], [-10, 10], [0, 0]</p>
</li>
<li>
<p>TriangleL: blobs centered at [10, 0], [0, 10], [0, 0]</p>
</li>
<li>
<p>Diagonal: blobs centered at [-10, -10], [0, 0], [10, 10]</p>
</li>
<li>
<p>NoisyDiagonal: blobs centered at [-3, -3], [0, 0], [3, 3]</p>
</li>
<li>
<p>NoisyDiagonal: blobs centered at [-2, -2], [0, 0], [2, 2]</p>
</li>
<li>
<p>Square: blobs centered at [10, 10], [-10, -10], [10, -10], [-10, 10]</p>
</li>
<li>
<p>Checkers: blobs centered on a 10 x 10 grid, with centers at [10i, 10j] for even (i + j)</p>
</li>
<li>
<p>NoisyCheckers: blobs centered on a 10 x 10 grid, with centers at [3i, 3j] for even (i + j)</p>
</li>
</ul>
<h4>Circle</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-circle-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-circle-2.png">
<p>Both approaches fail to detect any meaningful information. More specifically, during the model optimization process, no explored model performs significantly better than the null model, which assumes independence between the two variables.</p>
<p>This is consistent with the data distribution, which is based on a single isotropic Gaussian distribution.
The plot, based on a rank-based normalization of the values, visually aligns with the assumption of two independent variables.</p>
<p>This bivariate distribution can be explained by the marginal Gaussian distributions of <code>a</code> and <code>b</code> (see below), with no correlation between the two variables.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-circle-3.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-circle-4.png">
<h4>TriangleU</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-triangleu-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-triangleu-2.png">
<p>The VxV approach correctly identifies the pattern consisting of three dense coclusters, with <code>a</code> partitioned into three intervals and <code>b</code> into two intervals.
There is actually a good match between these dense coclusters and the natural clusters visually distinguishable in the scatterplots.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-triangleu-3.png">
<p>Surprisingly, the IxV approach only retrieves two clusters of instances, with <code>a</code> partitioned into five intervals and <code>b</code> into three intervals.</p>
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-triangleu-4.png">
<p>The coclusters have a fundamentally different nature, as they relate to clusters of instances correlated with clusters of intervals.
In fact, the two dense coclusters can be summarized as follows:</p>
<ul>
<li>
<p>First dense cocluster</p>
<ul>
<li>Relates to either small or large values of a and large values of b</li>
<li>Corresponds to the two upper natural clusters of the displayed pattern</li>
</ul>
</li>
<li>
<p>Second dense cocluster</p>
<ul>
<li>Relates to medium values of a and small values of b</li>
<li>Corresponds to the lower natural cluster of the displayed pattern</li>
</ul>
</li>
</ul>
<p>This dataset summary makes sense, but the fact that the two upper clusters are not separated is somewhat surprising.</p>
<h5>The Limits of IxV Coclustering</h5>
<p>The behavior can actually be explained with some deeper insight into this type of model.</p>
<p>In IxV coclustering, let's call <strong>inner variable</strong> the variables that describe each instance.</p>
<p>An IxV coclustering can be viewed as a VxV coclustering related to two categorical variables:</p>
<ul>
<li>
<p>The first variable, <code>Id</code>, represents the instances, with one distinct value per instance: the instance identifier.</p>
</li>
<li>
<p>The second variable, <code>VarPart</code>, represents the inner variable parts, with one value per part of each inner variable.</p>
</li>
<li>
<p>There is one observation per instance and per inner variable.</p>
</li>
</ul>
<p>In our previous example, we have:</p>
<ul>
<li>
<p>The <code>Id</code> variable with 1,000 distinct values.</p>
</li>
<li>
<p>The <code>VarPart</code> variable with 8 distinct values, related to the five intervals of a and the three intervals of b.</p>
</li>
<li>
<p>Altogether, there are 2,000 observations, given the values of the two inner variables describing each instance.</p>
</li>
</ul>
<p>The objective of IxV coclustering is thus to partition a contingency table of size 1,000 x 8, containing a total of 2,000 observations, where each value of the Id variable has only two observations.</p>
<p>The average expected frequency for each cell is approximately 2,000 / (1,000 * 8) ~ 0.25.</p>
<p>For comparison, consider the chi-square test of independence applied to contingency tables.
Small expected frequencies lead to poor approximation of the chi-square distribution of the test statistic.
A general rule of thumb is to have at least 5 as the smallest expected frequency in each cell.</p>
<p>In our case, the expected cell frequency of 0.25 is far too low to obtain an accurate model.</p>
<p>The IxV coclustering obtained under these conditions cannot be highly accurate, given the tiny number of observations per instance.
However, it still provides a meaningful summary of the data, making the best use of the available data while avoiding overfitting.</p>
<h5>The Limits of VxV Coclustering</h5>
<p>VxV coclustering yields accurate results in the case of two variables.<br>
It can be applied to datasets with more than two variables, but this introduces new challenges.</p>
<p>Suppose you have a dataset with <code>n</code> instances and <code>k</code> variables, each partitioned into only two parts, intervals or groups of values.<br>
The VxV coclustering resulting from the cross-product of the univariate partitions contains (2^k) coclusters.</p>
<p>For example, with <code>n</code> = 1,000 instances and <code>k</code> = 10 variables, we obtain (2^10 = 1024) coclusters, which means on average less than one observation per cocluster.
With such a sparsity, there is not enough data to produce a model better than the null model, which consists of a single cocluster.</p>
<p>Overall, no meaningful information can be retrieved using a VxV coclustering model when the number of variables becomes too high, typically beyond around (log_2(n)).</p>
<h4>TriangleL</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-trianglel-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-trianglel-2.png">
<p>As with the TriangleU pattern, the VxV approach correctly identifies the pattern consisting of three dense coclusters.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-trianglel-3.png">
<p>Once again, the IxV approach only retrieves two clusters of instances, with <code>a</code> and <code>b</code> each partitioned into two intervals.</p>
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-trianglel-4.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-trianglel-5.png">
<p>The two clusters obtained are of even poorer quality than before.<br>
Looking at the rank-based scatterplot, we understand that <code>a</code> is partitioned into two equal-frequency intervals, and <code>b</code> exploits quartiles, with the second interval corresponding to the last quartile.
This aligns with the optimization algorithm, which explores a series of starting solutions with univariate preprocessing based on 2, 4, 8, ... equal-frequency partitions.</p>
<p>Given this pattern and only two observations per instance, these raw results are probably the most accurate possible given the data and the limitations of the optimization algorithm.
IxV models are definitely not suitable for datasets with only two variables.</p>
<h4>Diagonal</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-diagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-diagonal-2.png">
<p>This pattern consists of three diagonal blobs, with highly correlated variables.<br>
It is easier than the triangle patterns and is easily retrieved by both the VxV and IxV approaches.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-diagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-diagonal-4.png">
<h4>NoisyDiagonal</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisydiagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisydiagonal-2.png">
<p>This pattern is similar to the diagonal pattern, with closer blobs.
Like the diagonal pattern, it is correctly identified by both the VxV and IxV approaches.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisydiagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisydiagonal-4.png">
<p>Note that the clusters are less separable than in the diagonal pattern.</p>
<ul>
<li>
<p>With the VxV coclustering, the three original blobs are primarily identified within the three dense diagonal coclusters, derived from the 25 coclusters resulting from a 5 x 5 intervals coclustering.</p>
</li>
<li>
<p>Similarly, with the IxV coclustering, three clusters of instances are identified, also based on a 5 x 5 partition of variables a and b.</p>
</li>
<li>
<p>These methods are particularly valuable when the data exhibits complex density structures or smooth transitions between dense regions, where traditional clustering may fail or be less meaningful.</p>
</li>
</ul>
<p>It is noteworthy that the objective of both coclustering approaches is to estimate piecewise constant densities within each cocluster.
Contrary to traditional clustering methods, clusters are only a by-product of the approach: only dense coclusters can be interpreted as traditional clusters.</p>
<h4>BlurredDiagonal</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-blurreddiagonal-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-blurreddiagonal-2.png">
<p>The three blobs are even closer than before, resulting in visually indistinguishable clusters.</p>
<p>The VxV coclustering correctly retrieves the joint density, although the connection between dense coclusters and clusters has disappeared.
The IxV coclustering provides a rough estimation of the joint density, using two clusters of instances.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-blurreddiagonal-3.png">
<img width="450" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-blurreddiagonal-4.png">
<p>Note that assuming data can be decomposed into distinct clusters is a strong hypothesis, which often does not hold for many real datasets where there is a smooth transition between dense regions.
In such cases, traditional clustering methods may not be appropriate or effective.
In contrast, density-based coclustering approaches aim to provide a summary of the dataset through piecewise constant estimation of the joint density. These methods are applicable regardless of the underlying distribution.
When the data is inherently cluster-based, both clustering and coclustering approaches are more likely to produce comparable results, with a particular emphasis on the dense coclusters identified by the coclustering methods.</p>
<h4>Square</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-square-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-square-2.png">
<p>Surprisingly, the four <em>natural</em> clusters, visually distinguishable in the scatterplots, are not retrieved by either the VxV or the IxV approaches.</p>
<p>In fact, as shown in the rank-based scatterplot, the two variables <code>a</code> and <code>b</code> are perceived as independent, and no correlation pattern can be identified.<br>
The visual pattern can be much more simply explained by the marginal distributions of <code>a</code> and <code>b</code>, each having two modes, resulting in a bivariate scatterplot that appears as four clusters.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-square-3.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-square-4.png">
<p>It is important to remember that coclustering models seek correlation patterns that are invariant to any monotonic transformation of the data.<br>
Therefore, some visual bivariate patterns may sometimes appear due to strong patterns in the marginal distributions of the variables, even when the variables are uncorrelated.</p>
<h4>Checkers</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-checkers-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-checkers-2.png">
<p>This complex pattern is correctly retrieved using the VxV approach.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-checkers-3.png">
<p>As expected, the IxV approach cannot retrieve such a complex pattern given the very few observations per instance.</p>
<h4>NoisyCheckers</h4>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisycheckers-1.png">
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisycheckers-2.png">
<p>This complex and noisy pattern is also correctly retrieved using the VxV approach. It is all the more remarkable that the underlying pattern is hardly visually distinguishable in the scatterplots.</p>
<p>This is close to the limit of reliable detection of correlation patterns, especially since the method is regularized against overfitting, preventing it from retrieving patterns in the case of independent variables.</p>
<img width="300" height="250" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1185-noisycheckers-3.png">
<p>As expected, the IxV approach cannot retrieve such a complex pattern given the very few observations per instance.</p>


*Source: [discussion #1185](https://github.com/orgs/KhiopsML/discussions/1185)*

<a id="discussion-1186"></a>
## Why does VxV coclustering become sparse in higher dimensions, and what protects IxV?

<h3>Clarification on Coclustering Approaches and Sparsity Issues</h3>
<p>V×V coclustering partitions each input variable and exploits the cross-product of all partitioned dimensions. Because its size grows exponentially with the number of variables, it can lead to extreme sparsity. I×V coclustering does not implicitly face the same combinatorial explosion for the following reasons:</p>
<h4>Data in a k-dimensional space</h4>
<p>When data is defined in a <strong>k-dimensional space</strong> (e.g., numerical space), if the space is <strong>fully populated</strong>, nothing can be learned.</p>
<h5>Extreme cases:</h5>
<ul>
<li>
<p><strong>k independent variables:</strong><br>
Both coclustering approaches, <strong>VxV</strong> and <strong>IxV</strong>, result in the null model because the variables are independent.</p>
</li>
<li>
<p><strong>k identical variables:</strong><br>
The dependency pattern is straightforward, as the data lies on a manifold of dimension 1.</p>
<ul>
<li>The <strong>VxV</strong> approach describes the data in its full k-dimensional space.</li>
<li>The <strong>IxV</strong> approach seeks clusters located on the data manifold, summarizing them by partitioning each dimension.</li>
</ul>
</li>
</ul>
<h4>The case of k identical variables</h4>
<h5>VxV Coclustering Approach</h5>
<ul>
<li>There are <strong>n observations</strong> in <strong>k dimensions</strong>.</li>
<li>Describing the position of each observation in the k-dimensional space is costly.</li>
<li>For example, splitting each dimension into <strong>I</strong> equal intervals results in <strong><span class="arithmatex">\(I^k\)</span></strong> coclustering cells.</li>
<li>To describe <strong>n</strong> instances, a multinomial distribution with <strong><span class="arithmatex">\(I^k\)</span></strong> outcomes is needed, with zero probability everywhere except for <strong>I</strong> outcomes.</li>
<li>This limits the precision of data summarization, especially as <strong>k</strong> increases (curse of dimensionality).</li>
</ul>
<h5>IxV Coclustering Approach</h5>
<ul>
<li>There are <strong>n * k observations</strong>, each represented as a pair <strong>(instance, variable value)</strong> in 2D space.</li>
<li>Splitting each dimension into <strong>I</strong> parts results in:
<ul>
<li><strong>I</strong> clusters of instances,</li>
<li><strong>I</strong> clusters of variable parts,</li>
<li>and a multinomial distribution with <strong><span class="arithmatex">\(I^2\)</span></strong> outcomes to describe the data, with zero probability everywhere except for <strong>I</strong> outcomes.</li>
</ul>
</li>
<li>This approach effectively captures strong dependencies across variables in a parsimonious way.</li>
</ul>
<h5>Experimental Illustration</h5>
<p>We consider datasets with <strong>2, 4, 8</strong> numerical variables uniformly distributed on [0, 1], generated with sizes from <strong>2 to 1024</strong> (powers of two). Each experiment is repeated 10 times.</p>
<h6><strong>VxV coclustering</strong> Results:</h6>
<p><img width="320" height="240" alt="VxV_Simulation_False_NUM_MeanPartitionSize" src="/assets/images/q-and-a/coclustering-da27770b/1186-vxv-coclustering-results-1.png"> <img width="320" height="240" alt="VxV_Simulation_False_NUM_VarNumber" src="/assets/images/q-and-a/coclustering-da27770b/1186-vxv-coclustering-results-2.png"></p>
<p>Synthesis:</p>
<ul>
<li>When data is small, the null model (single part per variable) is optimal.</li>
<li>With more data, models improve, but the number of parts per variable increases slowly.</li>
<li>For <strong>8 variables</strong>, at least <strong>128 instances</strong> are needed to exploit all variables.</li>
<li>The mean number of parts per variable increases with data size but suffers from the curse of dimensionality (up to 20 parts for 2 variables, but only 3 for 8 variables).</li>
</ul>
<h6><strong>IxV coclustering</strong>  results:</h6>
<img width="320" height="240" alt="Simulation_False_NUM_MeanPartitionSize" src="/assets/images/q-and-a/coclustering-da27770b/1186-ixv-coclustering-results-1.png">
<p>Synthesis:</p>
<ul>
<li>When data is small, the null model (single part per variable and single cluster per dimension) is optimal.</li>
<li>Performs less accurately with only <strong>2 variables</strong> (only 2 observations per instance), and poorly in the case of more complex patterns.</li>
<li>With <strong>1000 instances</strong>, it builds more than <strong>30 parts per variable</strong>, more than ten times the VxV approach for the same number of variables.</li>
</ul>
<h4>Summary</h4>
<ul>
<li>
<p><strong>VxV coclustering:</strong><br>
Describes the data manifold in <strong>k-dimensional space</strong>.</p>
<ul>
<li>The data size must grow exponentially with <strong>k</strong> due to the curse of dimensionality.</li>
<li>Suitable for <strong>small dimensions</strong>.</li>
</ul>
</li>
<li>
<p><strong>IxV coclustering:</strong><br>
Focuses on the <strong>intrinsic dimension</strong> of the data manifold.</p>
<ul>
<li>Suitable for manifold of intrinsic dimension far less than <strong>k</strong>, summarizing it via instance clusters and variable parts.</li>
</ul>
</li>
</ul>
<p>Estimating joint density remains challenging. If the <strong>intrinsic dimension</strong> of the manifold is too high, <strong>nothing</strong> can be effectively learned, regardless of the modeling approach.</p>


*Source: [discussion #1186](https://github.com/orgs/KhiopsML/discussions/1186)*

<a id="discussion-1187"></a>
## What does an IxV coclustering analysis look like on a real dataset \(Iris\)?

<h3>Exploratory analysis of the Iris dataset using Instances x Variables Coclustering</h3>
<p>We present an exploratory analysis of the Iris dataset using Instances x Variables Coclustering.</p>
<p>Python script for the study: <a href="http://iris_coclustering_study.py">iris_coclustering_study.py</a></p>
<p><a href="/assets/discussion-scripts/q-and-a/coclustering-da27770b/1187-exploratory-analysis-of-the-iris-dataset-using-instances-x-v-1.py">iris_coclustering_study.py</a></p>
<h4>Iris dataset</h4>
<p>The Iris dataset consists of 150 instances of flowers, described by one categorical variable, <strong>Class</strong>, and four numerical variables, <strong>PetalLength</strong>, <strong>PetalWidth</strong>, <strong>SepalLength</strong>, <strong>SepalWidth</strong>.</p>
<p>The <strong>Class</strong> variable has three values: <code>Iris-setosa</code>, <code>Iris-versicolor</code> and <code>Iris-virginica</code>.</p>
<p>Below is an extract from this dataset.</p>
<table>
<thead>
<tr>
<th>Class</th>
<th>PetalLength</th>
<th>PetalWidth</th>
<th>SepalLength</th>
<th>SepalWidth</th>
</tr>
</thead>
<tbody>
<tr>
<td>Iris-setosa</td>
<td>1.4</td>
<td>0.2</td>
<td>5.1</td>
<td>3.5</td>
</tr>
<tr>
<td>Iris-setosa</td>
<td>1.5</td>
<td>0.2</td>
<td>4.6</td>
<td>3.1</td>
</tr>
<tr>
<td>Iris-versicolor</td>
<td>4.7</td>
<td>1.4</td>
<td>7.0</td>
<td>3.2</td>
</tr>
<tr>
<td>Iris-versicolor</td>
<td>3.9</td>
<td>1.4</td>
<td>5.2</td>
<td>2.7</td>
</tr>
<tr>
<td>Iris-virginica</td>
<td>6.0</td>
<td>2.5</td>
<td>6.3</td>
<td>3.3</td>
</tr>
<tr>
<td>Iris-virginica</td>
<td>5.1</td>
<td>1.9</td>
<td>5.8</td>
<td>2.7</td>
</tr>
<tr>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</tbody>
</table>
<h4>Instances x Variables Coclustering</h4>
<p>A co-clustering of instances x variables involves two dimensions:</p>
<ul>
<li>
<p>A dimension for the instances</p>
</li>
<li>
<p>A dimension for variable parts</p>
</li>
</ul>
<p>This second dimension corresponds to the set of variables describing each instance: these are the inner variables, specific to this dimension.
Each inner variable is partitioned into a set of variable parts, which serve as the vocabulary used to describe each instance.</p>
<p>Thus, on one hand, we have a partition of the instances, and on the other hand, a partition of the variable parts. The co-clustering of instances x variables tends to group instances into clusters if they are described by the same variable parts.</p>
<p>This approach is analogous to text x word co-clustering, where texts are grouped into clusters if they are described by the same clusters of words.</p>
<h4>IxV Coclustering of the Iris dataset</h4>
<p>The IxV coclustering optimize the following model parameters:</p>
<ul>
<li>
<p>Partition of the variables</p>
</li>
<li>
<p>Clusters of instances</p>
</li>
<li>
<p>Clusters of variable parts</p>
</li>
<li>
<p>Coclusters</p>
</li>
</ul>
<h5>Partition of the Variables</h5>
<p>The descriptive variables are partitioned as follows:</p>
<table>
<thead>
<tr>
<th>Variable</th>
<th>Type</th>
<th>Parts</th>
<th>Partition</th>
<th>Frequencies</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Class</strong></td>
<td>Categorical</td>
<td>3</td>
<td>{Iris-setosa} <br> {Iris-versicolor} <br> {Iris-virginica}</td>
<td>50 <br> 50 <br> 50</td>
</tr>
<tr>
<td><strong>PetalLength</strong></td>
<td>Numerical</td>
<td>3</td>
<td>]-inf, 2.4] <br> ]2.4, 4.75] <br> ]4.75, +inf[</td>
<td>50 <br> 55 <br> 45</td>
</tr>
<tr>
<td><strong>PetalWidth</strong></td>
<td>Numerical</td>
<td>3</td>
<td>]-inf, 0.8] <br> ]0.8, 1.75] <br> ]1.75, +inf[</td>
<td>50 <br> 46 <br> 54</td>
</tr>
<tr>
<td><strong>SepalLength</strong></td>
<td>Numerical</td>
<td>3</td>
<td>]-inf, 5.45] <br> ]5.45, 6.85] <br> ]6.85, +inf[</td>
<td>52 <br> 17 <br> 81</td>
</tr>
<tr>
<td><strong>SepalWidth</strong></td>
<td>Numerical</td>
<td>2</td>
<td>]-inf, 3.35] <br> ]3.35, +inf[</td>
<td>36 <br> 114</td>
</tr>
</tbody>
</table>
<p>Given these partitions, the original Iris instances can be considered as text documents, described by words based on variable parts.</p>
<table>
<thead>
<tr>
<th>Instance</th>
<th>Class</th>
<th>PetalLength</th>
<th>PetalWidth</th>
<th>SepalLength</th>
<th>SepalWidth</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>{Iris-setosa}</td>
<td>]-inf, 2.4[</td>
<td>]-inf, 0.8[</td>
<td>]-inf, 5.45[</td>
<td>]3.35, +inf[</td>
</tr>
<tr>
<td>2</td>
<td>{Iris-setosa}</td>
<td>]-inf, 2.4[</td>
<td>]-inf, 0.8[</td>
<td>]-inf, 5.45[</td>
<td>]-inf, 3.35[</td>
</tr>
<tr>
<td>3</td>
<td>{Iris-versicolor}</td>
<td>]2.4, 4.75[</td>
<td>]0.8, 1.75[</td>
<td>]6.85, +inf[</td>
<td>]-inf, 3.35[</td>
</tr>
<tr>
<td>4</td>
<td>{Iris-versicolor}</td>
<td>]2.4, 4.75[</td>
<td>]0.8, 1.75[</td>
<td>]-inf, 5.45[</td>
<td>]-inf, 3.35[</td>
</tr>
<tr>
<td>5</td>
<td>{Iris-virginica}</td>
<td>]4.75, +inf[</td>
<td>]1.75, +inf[</td>
<td>]5.45, 6.85]</td>
<td>]-inf, 3.35[</td>
</tr>
<tr>
<td>6</td>
<td>{Iris-virginica}</td>
<td>]4.75, +inf[</td>
<td>]1.75, +inf[</td>
<td>]5.45, 6.85]</td>
<td>]-inf, 3.35[</td>
</tr>
<tr>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</tbody>
</table>
<h5>Clusters of instances and of variables parts</h5>
<p>Given the new description of the instances, the instances are partitionned into clusters on one dimension, and the variable parts are partitioned into clusters of variables part in the other dimension of the coclustering.</p>
<p>There are three clusters of instances.</p>
<table>
<thead>
<tr>
<th>Cluster</th>
<th>Frequency</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Ci1</code></td>
<td>50</td>
</tr>
<tr>
<td><code>Ci2</code></td>
<td>50</td>
</tr>
<tr>
<td><code>Ci3</code></td>
<td>50</td>
</tr>
</tbody>
</table>
<p>And four clusters of variable parts.</p>
<table>
<thead>
<tr>
<th>Cluster</th>
<th>Variable parts</th>
<th>Frequencies</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Cvp1</code></td>
<td>Class {Iris-setosa} <br> PetalLength ]-inf, 2.4] <br> PetalWidth ]-inf, 0.8] <br> SepalLength ]-inf, 5.45] <br> SepalWidth ]3.35, +inf[</td>
<td>50 <br> 50 <br> 50 <br> 52 <br> 36</td>
</tr>
<tr>
<td><code>Cvp2</code></td>
<td>Class {Iris-virginica} <br> PetalLength ]4.75, +inf[ <br> PetalWidth ]1.75, +inf[ <br> SepalLength ]6.85, +inf[</td>
<td>50 <br> 55 <br> 46 <br> 17</td>
</tr>
<tr>
<td><code>Cvp3</code></td>
<td>Class {Iris-versicolor} <br> PetalLength ]2.4, 4.75] <br> PetalWidth ]0.8, 1.75]</td>
<td>50 <br> 45 <br> 54</td>
</tr>
<tr>
<td><code>Cvp4</code></td>
<td>SepalLength ]5.45, 6.85] <br> SepalWidth ]-inf, 3.35]</td>
<td>81 <br> 114</td>
</tr>
</tbody>
</table>
<h5>Coclusters</h5>
<p>We have a total of 5 observations per instance, one for each variable (e.g., (<code>1</code>, <code>SepalLength ]-inf, 5.45[</code>)), which gives 150 * 5 = 750 observations.</p>
<p>These 750 observations are distributed across the 3 x 4 coclustering matrix, with the following frequencies per cocluster:</p>
<table>
<thead>
<tr>
<th></th>
<th><code>Cvp1</code></th>
<th><code>Cvp2</code></th>
<th><code>Cvp3</code></th>
<th><code>Cvp4</code></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Ci1</code></td>
<td>8</td>
<td>8</td>
<td>144</td>
<td>90</td>
</tr>
<tr>
<td><code>Ci2</code></td>
<td>5</td>
<td>160</td>
<td>5</td>
<td>80</td>
</tr>
<tr>
<td><code>Ci3</code></td>
<td>225</td>
<td>0</td>
<td>0</td>
<td>25</td>
</tr>
</tbody>
</table>
<h5>Interpretation using Dense Coclusters</h5>
<img width="600" height="350" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1187-interpretation-using-dense-coclusters-1.png">
<p>The coclustering matrix exhibits significant contrasts compared to the case where instances and variable parts are independent.</p>
<p>It is visualized below with colors assigned according to the contribution to the mutual information between the two dimensions:</p>
<ul>
<li>
<p>Red for dense coclusters, where the observed frequency is above the expected frequency under independence,</p>
</li>
<li>
<p>Blue when the observed frequency is below the expected frequency,</p>
</li>
<li>
<p>White when the observed frequency is very small or close to the expected frequency.</p>
</li>
</ul>
<p>In the case of the Iris dataset, there is one dense cocluster per cluster of instances, which facilates their interpretation.</p>
<ul>
<li><code>Ci1</code> contains 50 instances, over-represented across  the variables parts
<ul>
<li>Class {Iris-versicolor}</li>
<li>PetalLength ]2.4, 4.75]</li>
<li>PetalWidth ]0.8, 1.75]</li>
</ul>
</li>
<li><code>Ci2</code> contains 50 instances, over-represented across  the variables parts
<ul>
<li>Class {Iris-virginica}</li>
<li>PetalLength ]4.75, +inf[</li>
<li>PetalWidth ]1.75, +inf[</li>
<li>SepalLength ]6.85, +inf[</li>
</ul>
</li>
<li><code>Ci3</code> contains 50 instances, over-represented across  the variables parts
<ul>
<li>Class {Iris-setosa}</li>
<li>PetalLength ]-inf, 2.4]</li>
<li>PetalWidth ]-inf, 0.8]</li>
<li>SepalLength ]-inf, 5.45]</li>
<li>SepalWidth ]3.35, +inf[</li>
</ul>
</li>
</ul>
<p>Overall, we can summarize the Iris dataset using three clusters, focusing on the variables Class, PetalLength, and PetalWidth.
The first cluster mainly consists of flowers of class Iris-versicolor, with medium-sized petals.
The second cluster consists primarily of flowers of class Iris-virginica, with large petals.
The third cluster includes flowers of class Iris-setosa, with small petals.</p>
<p>The last two variables SepalLength and SepalWidth are less important for characterizing the clusters.</p>
<h5>Additional Visual Evidence for Cluster Interpretation</h5>
<img width="600" height="500" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1187-additional-visual-evidence-for-cluster-interpretation-1.png">
<p>We present a scatter plot of the most explanatory variables, with <strong>PetalWidth</strong> on the X-axis, <strong>PetalLength</strong> on the Y-axis, and shapes used to indicate the <strong>Class</strong> of each instance.
The intervals of these two variables are represented by vertical or horizontal dashed lines.
Each dot corresponds to an instance, with the color indicating the cluster to which the instance belongs.
This scatter plot demonstrates a good alignment between the clusters and the variable parts associated with these explanatory variables.</p>
<img width="600" height="500" alt="Image" src="/assets/images/q-and-a/coclustering-da27770b/1187-additional-visual-evidence-for-cluster-interpretation-2.png">
<p>We also show a scatter plot using the less important variables <strong>SepalWidth</strong> and <strong>SepalLength</strong>.
In this case, the correspondence between the clusters and SepalLength and SepalWidth is much less clear, as indicated by the dataset summary provided through the IxV coclustering.</p>
<h5>Relation with Variable x Variable Coclustering</h5>
<h5>VxV Coclustering</h5>
<p>Variable x Variable Coclustering involves two or more dimensions, one for each variable.
Each variable is partitioned into intervals (for numerical variables) or groups of values (for categorical variables).
The entire data space is then partitioned into a grid of co-clusters, resulting from the cross-product of the univariate partitions.
This results in density estimation models, assuming the density is constant within each co-cluster.</p>
<h5>Bivariate analysis</h5>
<p>In the case of bivariate analysis, VxV coclustering provides a reliable and accurate joint density estimator.
For the Iris dataset, some VxV coclustering results are based on up to 4 parts per variable.</p>
<p>Conversely, IxV coclustering is not suitable when only two variables are involved, as it results in only two observations per instance.
This is insufficient for accurate density estimation, and IxV coclustering systematically uses fewer parts.</p>
<h5>Multivariate analysis</h5>
<p>With more variables, the IxV coclustering approach offers a good summary of the dataset, as demonstrated in the exploratory study of the Iris dataset.</p>
<p>In contrast, VxV coclustering suffers from sparsity as the number of variables increases.
For example, with only two parts per variable and <code>k</code> variables, the resulting coclustering consists of <code>2^k</code> coclusters.
Furthermore, visualization tools become much more difficult to utilize with more than two dimensions.</p>
<p>In the case of the Iris dataset, VxV coclustering results in a 3 x 3 x 3 x 2 x 1 cocluster grid, with SepalWidth partitioned into a single interval.
This can be compared to IxV approaches, which build 3 clusters of instances distributed across 4 clusters of variable parts, based on 3, 3, 3, 3, and 2 parts per variable, offering a finer partitioning of the descriptive variables.</p>
<h5>Key Takeaways</h5>
<p><strong>VxV coclustering</strong> provides detailed joint density estimates, but the quality of the estimation decreases with data sparsity as the number of variables increases.
Additionally, the usefulness of visualization tools diminishes with higher dimensions.</p>
<p><strong>IxV coclustering</strong> offers a robust summary of datasets, especially when there are a sufficient number of variables.
However, it is not suitable for precise density estimation in bivariate cases.</p>


*Source: [discussion #1187](https://github.com/orgs/KhiopsML/discussions/1187)*
