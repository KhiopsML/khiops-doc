# Fundamentals of modeling

<a id="discussion-474"></a>
## How does Khiops handle datasets with imbalanced classes?

<h3>Handling class imbalance in Khiops</h3>
<p><strong>Khiops is robust to class imbalance</strong>, so rebalancing techniques are generally not required.</p>
<p>However, class imbalance often necessitates collecting large amounts of data to gather sufficient information about the minority class. This can result in very large datasets with billions of records and significantly longer training times. In such cases, rebalancing the dataset can be <em>beneficial</em>.</p>
<p>The standard approach is <strong>to retain all examples from the minority class and undersample the majority class</strong>. This strategy reduces computation time while preserving critical information. Never oversample the minority class, as duplicate instances lead to significant overfitting.</p>
<p><strong>Best practices for rebalancing:</strong></p>
<ul>
<li>Retain all individuals in the minority class.</li>
<li>Undersample the majority class only as much as necessary to fit within the available computational resources, ensuring sufficient information is retained for training. In most cases, having up to 100 times more examples than the minority class is sufficient.</li>
</ul>
<p><strong>Impact on model performance and scores:</strong></p>
<ul>
<li>Score ranking: The ranking of scores (used for ranking or thresholding) on a non-rebalanced test set remains consistent. Metrics such as ROC curves and AUC are minimally impacted.</li>
<li>Predicted probabilities are completely skewed and unusable because the training set has an artificially higher representation of the minority class. This is typically not an issue, as most applications prioritize score rankings over probabilities.</li>
<li>Calibration: If accurate probability estimates are required, apply a calibration method to adjust the predicted probabilities.</li>
</ul>


*Source: [discussion #474](https://github.com/orgs/KhiopsML/discussions/474)*

<a id="discussion-488"></a>
## Since Khiops does not have hyperparameters, how can I manage overfitting?

<h3>How Khiops controls model complexity</h3>
<p>Khiops avoids overfitting through its core design, which is based on the MDL (Minimum Description Length) principle. This formalism balances the complexity of a model with its ability to explain the data, making Khiops particularly robust.</p>
<p><strong>Here’s why Khiops excels at avoiding overfitting:</strong></p>
<ul>
<li><strong>Statistically significant patterns only:</strong> Khiops selects only patterns supported by sufficient data, automatically rejecting noise.</li>
<li><strong>No arbitrary parameters:</strong> By avoiding user-defined hyperparameters, Khiops streamlines workflows and reduces the risk of overfitting caused by over-tuning.</li>
</ul>
<p><strong>How Khiops achieves this:</strong></p>
<p>Unlike standard models that rely on regularization parameters to control the trade-off between complexity and generalization, <strong>Khiops achieves this balance intrinsically through a mechanism rooted in information theory</strong>. <a href="https://khiops.org/learn/modl/">Our original formalism</a> penalizes unnecessary complexity by favoring models that explain the data as simply as possible.
This ensures that every variable, interval, or aggregate is justified by the amount of information it provides, without requiring external tuning. For instance:</p>
<ul>
<li>A complex derived feature from multi-table data is included only if it significantly improves the model.</li>
<li>Similarly, for the encoding of a variable, an interval or a group will only be added if it provides sufficient information to justify its inclusion.</li>
</ul>
<p><strong>Khiops naturally handles noisy datasets by ignoring irrelevant patterns:</strong></p>
<ul>
<li>When enough meaningful data is present, noise doesn’t affect the model (even if highly present).</li>
<li>If the dataset contains too much noise and insufficient data, Khiops will prudently return one single interval.</li>
</ul>
<p>While this cautious behavior is a key advantage, it also means that <strong>Khiops performs better and better with more data</strong> (building powerful models requires enough data to <em>justify</em> more complex constructs).</p>
<p><strong>Illustration</strong></p>
<p>The graph below shows how Khiops’ MODL approach handles the discretization of the “crenel pattern” <em>Class = Sign(Sinus(100πx))</em>, with 10% misclassified instances (as described in <a href="http://www.marc-boulle.fr/publications/BoulleML06.pdf">Boulle, 2006</a>, Figure 18). The <em>x-axis</em> represents the number of instances available in the dataset, while the <em>y-axis</em> shows the number of intervals created by the discretization process. This example is particularly illustrative because it demonstrates how MODL balances complexity and informativity, even in the presence of noise, while avoiding overfitting.</p>
<ul>
<li><strong>Insufficient or noisy data</strong>: When there are too few instances or excessive noise, Khiops keeps only one interval, avoiding unnecessary complexity (such numerical variables will be ignored in the final model as they are considered uninformative).</li>
<li><strong>Optimal intervals</strong>: As more data becomes available, Khiops adjusts dynamically, creating an optimal number of intervals to reflect the data’s structure.</li>
<li><strong>No overfitting</strong>: The number of intervals does not grow indefinitely. In this example, Khiops concludes that 100 intervals are sufficient. Adding more data does not produce spurious intervals, which prevents overfitting</li>
</ul>
<p><img src="/assets/images/q-and-a/fundamentals-cf50f290/488-how-khiops-controls-model-complexity-1.png" alt="Capture d’écran 2024-12-10 à 14 02 06"></p>


*Source: [discussion #488](https://github.com/orgs/KhiopsML/discussions/488)*

<a id="discussion-509"></a>
## How does Khiops handle target value grouping, and why is it useful for classification tasks?

<h3>Target value grouping in Khiops</h3>
<p>Khiops’ target value grouping functionality is designed to address challenges when dealing with a large number of target classes. When the number of classes is high, it can be difficult to discriminate between all classes, especially with insufficient number of instances (i.e. with sparse input data).</p>
<p>To address this, Khiops reduces data sparsity by grouping target classes. In practice:</p>
<ol>
<li><strong>Univariate Preprocessing</strong>: Target class groupings occur during the preprocessing step. Khiops determines the optimal grouping of target values for each variable based on the correlations between the data. The grouped classes are treated as distinguishable from other groups, but classes within the same group are considered indistinguishable.</li>
<li><strong>Class-level predictions</strong>: The Selective Naive Bayes (SNB) predictor uses the univariate preparations to make precise, class-by-class predictions. While groupings simplify univariate preprocessing, the final model still predicts probabilities for individual classes, not groups.</li>
</ol>
<p><strong>Example: Grouped Target Probabilities</strong></p>
<p>In the following example, the explanatory variable x has two distinct values {v1, v2}, and the target variable y has eight classes {A, B, C, D, E, F, G, H}, which are clustered into three groups during preprocessing.</p>
<p>For x = v1:</p>
<div class="highlight">
<pre><code>- P(y ∈ {A, B} | x = v1) = 0.1  
- P(y ∈ {C, D, E, F} | x = v1) = 0.75 
- P(y ∈ {G, H} | x = v1) = 0.15
</code></pre>
</div>
<p>For x = v2:</p>
<div class="highlight">
<pre><code>P(y ∈ {A, B} | x = v2) = 0.6  
P(y ∈ {C, D, E, F} | x = v2) = 0.1
P(y ∈ {G, H} | x = v2) = 0.3
</code></pre>
</div>
<p>In this example, the classifier identifies that distinguishing between groups ({A, B}, {C, D, E, F}, {G, H}) is feasible, but it cannot reliably separate classes within the same group during univariate preparation.</p>
<p>Because this grouping is done independently for each explanatory variable, a different grouping could occur for another explanatory variable z. For example:</p>
<p>For z = v0:</p>
<div class="highlight">
<pre><code>P(y ∈ {A, D, H} | z = v0) = 0.6  
P(y ∈ {B, C, E, F, G} | z = v0) = 0.4
</code></pre>
</div>
<p>The SNB predictor later uses this variable-specific grouped information from all explanatory variables to make precise, individual class predictions.</p>
<p><strong>Additional Insights</strong></p>
<p>In some cases, it may be beneficial to globally reduce the number of target classes for the entire problem. The univariate preparation reports generated by Khiops can help data miners identify frequently occurring groupings, guiding decisions about merging or removing target classes altogether.</p>


*Source: [discussion #509](https://github.com/orgs/KhiopsML/discussions/509)*

<a id="discussion-510"></a>
## Why is it better to provide raw data to Khiops instead of preprocessed or encoded data?

<h3>Khiops automatically encodes variables</h3>
<p>Khiops is specifically designed to work directly with raw data, minimizing the need for manual preprocessing. In fact, <strong>it is strongly recommended to avoid preparing your data</strong> to prevent loss of information, whether it concerns variable encoding, missing values, or data flattening (propositionalization).</p>
<p>Khiops employs the <em>MODL</em> formalism, based on the MDL (Minimum Description Length) principle, to encode variables optimally:</p>
<ul>
<li><strong>Categorical</strong> variables: Khiops automatically groups values into clusters based on their correlation with the target variable.</li>
<li><strong>Numerical</strong> variables: Khiops uses discretization to partition values into intervals, ensuring that each interval represents a meaningful range of data relative to the target variable.</li>
</ul>
<p>This optimal encoding is inherently tied to the modeling process and adapts dynamically to the data, making manual encoding methods unnecessary (and less effective !).</p>
<p><strong><em>Example: Why Encoding Isn’t Necessary</em></strong></p>
<p>Imagine a dataset with a categorical variable &quot;city&quot; containing hundreds of unique values. In a traditional workflow:</p>
<ul>
<li>One-hot encoding &quot;city&quot; would create hundreds of binary columns, resulting in a sparse and computationally expensive matrix.</li>
<li>Frequency encoding might lose context, treating &quot;city&quot; as independent from the target variable.</li>
</ul>
<p>With Khiops:</p>
<ul>
<li>&quot;City&quot; is automatically grouped into meaningful clusters (e.g., based on correlations with the target variable’s distribution), preserving interpretability and maximizing predictive power.</li>
</ul>
<p>Similarly, for a numerical variable &quot;age&quot;, Khiops would:</p>
<ul>
<li>Dynamically determine intervals (e.g., [0-18], [19-35], [36-50], [50-97]) based on the correlation between &quot;age&quot; and the target variable.</li>
<li>Avoid creating unnecessary intervals, ensuring a balance between simplicity and accuracy.</li>
</ul>
<p><strong>Handling Missing Values</strong></p>
<p>Khiops also treats missing values as part of the data, recognizing that they can carry meaningful information. Missing values are not discarded or imputed arbitrarily. Instead, Khiops assigns them to their own group or interval if they are informative for the target variable. This approach ensures that missing data is leveraged effectively, rather than being treated as noise or ignored outright.</p>
<p><strong>Scientific Basis</strong></p>
<p>Khiops’ preprocessing capabilities are grounded in rigorous statistical principles. The MODL formalism:</p>
<ul>
<li>Automatically balances model complexity and predictive information to prevent overfitting.</li>
<li>Dynamically adapts to the structure of the data, selecting groupings or intervals only when they provide significant predictive value.</li>
<li>Avoids arbitrary preprocessing decisions by tying encoding directly to the learning objective.</li>
</ul>
<p>For more details and examples, see this <a href="https://khiops.org/advanced/Notebooks/No_data_Cleaning/">notebook tutorial</a> or read about <a href="https://khiops.org/learn/preprocessing/">Optimal Encoding</a>.</p>
<p>This approach ensures that manual preprocessing is unnecessary (in fact, it is often counterproductive).</p>


*Source: [discussion #510](https://github.com/orgs/KhiopsML/discussions/510)*
