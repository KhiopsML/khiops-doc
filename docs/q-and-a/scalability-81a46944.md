# Scalability and large datasets

<a id="discussion-934"></a>
## Can users disable Khiops’ memory requirement checks?

<h5>Context</h5>
<p>Khiops sometimes prevents the execution of a data mining workflow, citing a lack of memory based on a rough estimate of the required memory. After using a machine with significantly more available RAM, we often notice that far less memory was actually used during the process. Allowing Khiops to run the task regardless of the available resources would be more convenient. After all, if I know my data well, Khiops simply prevents me from analyzing it in a too conservative manner. And if the program crashes, well, that's what can happen with all alternative methods, such as Scikit-Learn: why bother?</p>
<h3>Khiops Policy Regarding Resource Management</h3>
<h4>Main Objective: Never Crash</h4>
<ul>
<li>Khiops is an AutoML solution designed to be as simple and robust as possible to use.
<ul>
<li>The only user parameters concern the specification of the data analysis problem or business constraints, such as modeling speed, accuracy, or interpretability.</li>
<li>Technical parameters are never exposed to the user.</li>
</ul>
</li>
<li>The tool is intended for use in an industrial context.
<ul>
<li>It should never crash, regardless of the scale or complexity of the data to analyze, or the available resources.</li>
<li>Business constraints and deadlines for delivering scores are of key importance.</li>
</ul>
</li>
<li>Importance
<ul>
<li>A crash is likely to be highly costly for an operational team.</li>
<li>It is impossible to determine whether the crash originates from a bug or a lack of resources.</li>
<li>Testing and trials by running a task under different resource configurations (number of machines, cores, available disk, RAM) are not compatible with industrial constraints.</li>
</ul>
</li>
</ul>
<h4>Khiops Policy Regarding Resources</h4>
<ul>
<li>Khiops exploits available resources as much as possible to maximize the speed of task execution.</li>
<li>How:
<ul>
<li>Each internal algorithm evaluates the minimum necessary resources to run the task.</li>
<li>Given that, Khiops uses as many cores as possible, provided sufficient RAM is globally available.</li>
<li>If all data cannot fit into memory, Khiops splits the data:
<ul>
<li>Into chunks of instances for algorithms that can be decomposed on instances (e.g., deployment).</li>
<li>Into chunks of variables for algorithms that can be decomposed on variables (e.g., preprocessing).</li>
</ul>
</li>
<li>If there is not enough memory even after applying the splitting strategy:
<ul>
<li>The user is provided with an estimate of the minimum additional memory required.  -</li>
</ul>
</li>
</ul>
</li>
<li>This allows for out-of-core processing:
<ul>
<li>For example, analyzing a 9 GB dataset using one core and 512 MB RAM.</li>
<li>See <a href="https://khiops.org/learn/hardware_adaptation/#lets-run-an-experiment">Khiops Hardware Adaptation</a>.</li>
</ul>
</li>
</ul>
<h4>Why It Sometimes Fails</h4>
<ul>
<li>Estimating the necessary resources in advance is challenging due to many unknown data characteristics:
<ul>
<li>Number of selected instances in case of a selection criterion.</li>
<li>Number of missing values.</li>
<li>Data sparsity (e.g., texts).</li>
<li>Number of distinct values for numerical or categorical variables.</li>
<li>Length of categorical values.</li>
<li>Number of informative variables.</li>
<li>Number of secondary records per main record.</li>
<li>Etc.</li>
</ul>
</li>
<li>The principle for these evaluations is to iteratively gather information about the data after each analysis pass:
<ul>
<li>Basic statistics for the number of main instances and target variable values.</li>
<li>Descriptive statistics.</li>
<li>Preprocessing metrics.</li>
<li>Etc.</li>
</ul>
</li>
<li>Although Khiops can manage very large datasets using its out-of-core strategy, the number of main instances may still be too large.
<ul>
<li>Example: If there are 100 million instances in the main table:
<ul>
<li>Needs 100 million values simultaneously for univariate preprocessing: at least 800 MB.</li>
<li>Requires provisioning enough RAM for complex algorithms used in data preprocessing.
<ul>
<li>Example: around 100 bytes per value for double-linked lists, including value, criterion contribution, merging structures.</li>
<li>Total requirement: approximately 10 GB.</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li>If a numerical variable is actually a boolean with only two distinct values, the resource requirement may be excessively high.
<ul>
<li>Conversely, if a variable is truly continuous with as many distinct values as instances, the resource needs are different.</li>
<li>This can happen with a single variable added to a Khiops dictionary (e.g., using the Random rule) or generated automatically (e.g., variance of a secondary variable).</li>
</ul>
</li>
</ul>
<h4>How to Improve This</h4>
<ul>
<li>Estimating required resources remains a challenge; please report extreme cases where this estimation is clearly too conservative.</li>
<li>This issue is most likely to occur when a huge number of instances are kept for analysis.
<ul>
<li>Use sampling or instance selection to reduce the data volume.</li>
<li>Remember that increasing the number of instances may improve results but with diminishing returns:
<ul>
<li>10,000 to 100,000 instances: likely beneficial.</li>
<li>100,000 to 1,000,000: may be relevant in some cases.</li>
<li>1,000,000 to 10,000,000: will significantly increase processing time and cost, with unlikely improvements.</li>
</ul>
</li>
</ul>
</li>
</ul>


*Source: [discussion #934](https://github.com/orgs/KhiopsML/discussions/934)*

<a id="discussion-1006"></a>
## How to efficiently train and deploy a model on a huge, imbalanced database?

<h3>Training a Model with a Huge Database</h3>
<h4>Context of Big Data</h4>
<p>When dealing with a real data mining problem, you may have a huge database, potentially containing
terabytes of data. This is likely to happen in the case of a multi-table database, where your main
analyzed instances are described with detailed records stored in secondary tables.<br>
Furthermore, the target classes may be highly imbalanced, as in a customer churn detection problem.</p>
<p>For example, if your entity is a customer, you may have many logs per customer:</p>
<ul>
<li>Purchase details in marketing</li>
<li>Call detail records in telecommunications</li>
<li>Web navigation logs</li>
<li>...</li>
</ul>
<p>At Orange telecommunications, there are tens of millions of customers in France, each with
thousands of logs in secondary tables, amounting to tens of billions of logs at terabyte scale.</p>
<h4>Objective</h4>
<p>The objective is to train a model efficiently.</p>
<p>You need to build a flat analysis dataset, with instances in rows and variables in columns, to train
your model. Given the multi-table database, you have to construct features per instance from the
secondary records to obtain your flat analysis dataset.</p>
<p>Processing the whole database while constructing many features is not an option, given the
prohibitive computational resources required.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>For example, if you have a database of 10 million customers, with 100 logs per customer, and want
to construct 100,000 features per customer, you need:</p>
<ul>
<li>8 TB of disk space to store your analysis dataset: 10 million × 100,000 features = 1,000 billion
values, at approximately 8 bytes per value</li>
<li>100,000 billion read and computation operations from log values, as each constructed value is
computed from 100 logs on average</li>
</ul>
<p>This type of analysis is possible with Khiops, but it will require very large computational resources (disk, RAM, CPU).</p>
</div>
<h4>Methodology for Training and Deploying a Model</h4>
<p>You need to extract an analysis dataset from the whole database to perform your data mining study
efficiently.</p>
<p>Three steps are necessary:</p>
<ul>
<li>Extract an analysis dataset from the whole database</li>
<li>Perform your data mining study on the analysis dataset, to evaluate different modeling scenarios
and choose the best one</li>
<li>Deploy the best model on the whole database, to get predictions for all instances</li>
</ul>
<p>The first and last steps are data-intensive, as they involve scanning the whole database, while the
second step is computationally intensive, as it involves many tests and trials of modeling scenarios.</p>
<h4>Analysis Dataset</h4>
<p>The analysis dataset needs to be:</p>
<ul>
<li>Representative of the data under study</li>
<li>Large enough to reduce the variance of the results</li>
<li>A reasonable size, to enable fast analysis times</li>
</ul>
<h5>Representative</h5>
<p>Your dataset must fall within the same perimeter as your study. For example, if the business
objective is a marketing campaign targeting young customers in big cities, your analysis dataset must
be within the same perimeter.</p>
<p>Within this perimeter, your instances must be chosen at random. For example, if you need an analysis
dataset containing 100,000 instances, do not take the first 100,000 instances from your database, or
those with the first 100,000 identifiers. You really need a random sample.</p>
<h5>Large Enough</h5>
<p>Your analysis dataset must be large enough to provide reliable results, in order to determine whether
the business objectives are fulfilled with good confidence.</p>
<p>As a rule of thumb, the standard deviation of an evaluation criterion (e.g. accuracy) is around
<span class="arithmatex">\(\frac{1}{\sqrt{n}}\)</span> for a sample of size <span class="arithmatex">\(n\)</span>.</p>
<p>For example, in a political poll involving tens of millions of voters, samples are usually taken of
size <span class="arithmatex">\(n = 1{,}000\)</span>, implying a margin of error of around 3% (<span class="arithmatex">\(\frac{1}{\sqrt{1000}} \approx 0.03\)</span>).</p>
<p>The following table indicates error margins for several sample sizes:</p>
<table>
<thead>
<tr>
<th>Sample size</th>
<th>Error margin</th>
</tr>
</thead>
<tbody>
<tr>
<td>100</td>
<td>10%</td>
</tr>
<tr>
<td>1,000</td>
<td>3%</td>
</tr>
<tr>
<td>10,000</td>
<td>1%</td>
</tr>
<tr>
<td>100,000</td>
<td>0.3%</td>
</tr>
<tr>
<td>1,000,000</td>
<td>0.1%</td>
</tr>
</tbody>
</table>
<p>Choosing a sample size of between 1,000 and 10,000 looks like a good trade-off, as it provides good
confidence in the evaluation criteria, with a small error margin, while remaining fast to process
during the data mining study.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>If your dataset involves categorical variables with many values (e.g. first name or city zip code),
a larger sample may be necessary to capture enough occurrences of each value and potentially
extract more information from these variables.</p>
</div>
<h5>Case of Unbalanced Datasets</h5>
<p>The rule of thumb applies to balanced datasets: see Q&amp;A <a href="https://github.com/orgs/KhiopsML/discussions/474">https://github.com/orgs/KhiopsML/discussions/474</a>.
In the case of unbalanced datasets with a rare minority class (e.g. churner), you should ensure the requested sample size is met
for the rare class. For example, in a churn study with around 1% churners in your database, to have between <strong>1,000</strong> and <strong>10,000</strong> churners in your sample,  as recommended, you need a sample of size between <strong>100,000</strong> and <strong>1,000,000</strong>.</p>
<p>In this case, it might be a good idea to extract an <strong>enriched analysis dataset</strong> from the analysis
dataset, containing all instances of the rare class and a subset of the frequent ones. As a rule of
thumb, a sample of approximately 10 times the number of rare instances is a good trade-off. The
quality of your model will be roughly the same, while being far faster to train.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Using an enriched analysis dataset can speed up training, but the evaluation criteria will be
biased, as the proportion of churners will differ from that in the whole database. To obtain a
correct evaluation, you can use the whole analysis dataset, with the correct proportion of
churners, to evaluate the model trained on the enriched analysis dataset.</p>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>For example, in a churn study involving an analysis dataset of size 100,000 with 1,000 churners,
you can extract an enriched analysis sub-dataset containing all 1,000 churners and around 10,000
non-churners. You obtain a sub-dataset about 10 times smaller, which is far faster to process
than the whole analysis dataset.</p>
</div>
<h5>Reasonable Size</h5>
<p>A data mining study involves many tests and trials using your analysis dataset.</p>
<p>You must first divide your analysis dataset into:</p>
<ul>
<li><strong>Train dataset</strong>: to train the model</li>
<li><strong>Test dataset</strong>: to obtain a fair evaluation of the model's performance on the whole database</li>
</ul>
<p>The training phase involves several scans of the data, for data preparation, modeling, and
evaluation. This process must be repeated to evaluate different modeling scenarios, with varying
numbers of constructed features in the multi-table setting, varying numbers of trees, etc. To be
able to evaluate many modeling scenarios rapidly, you should adopt a fail-fast strategy and allow
train-test round trips to complete as quickly as possible.</p>
<p>Note that the requirements in time, energy, and cloud costs are at least proportional to the sample
size.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>For example, with a training database of 10 million instances, the training time with a sample of
size 100,000 will be at least 100 times smaller than with the whole database. You need to extract
the analysis dataset once and for all, to avoid scanning the whole database each time you evaluate
a new modeling scenario.</p>
</div>
<h4>Using Khiops for the Whole Process</h4>
<h5>Extraction of the Analysis Dataset</h5>
<p>When you extract an analysis dataset from the whole database, you need to extract a representative
sample of your analyzed instances, together with their secondary records for each secondary table of
the multi-table schema.</p>
<p>With Khiops, you simply perform a <strong>Deploy model</strong> applied to the whole database to extract your
analysis dataset:</p>
<ul>
<li>In the <strong>data dictionary</strong> (<code>.kdic</code>), use all native variables (not derived) and do not use any
derived variables, in order to obtain tables with exactly the same structure</li>
<li>Define the perimeter of your study using a <strong>selection variable</strong> that describes the instances to
collect
<ul>
<li>e.g. to select customers under 40 years old, use a derivation rule such as:<div class="highlight">
<pre><code class="language-kdic"><span class="kd">Unused</span><span class="w"> </span><span class="kt">Numerical</span><span class="w"> </span><span class="na">InPerimeter</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="nf">LE</span><span class="p">(</span><span class="na">age</span><span class="p">,</span><span class="w"> </span><span class="mf">40</span><span class="p">);</span>
</code></pre>
</div>
</li>
</ul>
</li>
<li>Use a <strong>sampling percentage</strong> to obtain an analysis dataset of the desired size</li>
</ul>
<p>In the case of a multi-table database, you simply specify one file per secondary table to obtain the
secondary records for the selected instances.</p>
<h5>Training a Model on the Analysis Dataset</h5>
<p>With your analysis dataset, you can perform your data mining study, evaluate different modeling
scenarios, and choose the best one.</p>
<p>With Khiops, use <strong>Train model</strong> with the default 70% train-test split, and evaluate training
scenarios by increasing complexity, starting with few constructed features (e.g. 1,000 constructed
features and no trees), up to at most 100,000 features and 1,000 trees.</p>
<p>In the case of an unbalanced dataset, you can extract an enriched analysis dataset to speed up
training. For example, to extract all churners and 10% of the other instances, use a selection
variable such as:</p>
<div class="highlight">
<pre><code class="language-kdic"><span class="c1">// Return 1 if the class is &quot;Churner&quot;, 1 otherwise if Random() is less than or equal to 0.1, 0 otherwise</span>
<span class="kd">Unused</span><span class="w"> </span><span class="kt">Numerical</span><span class="w"> </span><span class="na">InEnrichedSample</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="nf">If</span><span class="p">(</span><span class="nf">EQc</span><span class="p">(</span><span class="na">Class</span><span class="p">,</span><span class="w"> </span><span class="s">&quot;Churner&quot;</span><span class="p">),</span><span class="w"> </span><span class="mf">1</span><span class="p">,</span><span class="w"> </span><span class="nf">LE</span><span class="p">(</span><span class="nf">Random</span><span class="p">(),</span><span class="w"> </span><span class="mf">0.1</span><span class="p">));</span>
</code></pre>
</div>
<p>In the case of a huge dataset with highly unbalanced classes, even the analysis dataset may be too large to process efficiently.
In this case, you can directly extract the enriched analysis dataset by combining a <strong>selection variable</strong> and a <strong>sampling percentage</strong> within the same <strong>Deploy model</strong> run.</p>
<p>Choose the best modeling scenario with the best evaluation criteria, and verify that the business
objectives are fulfilled.</p>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Do not spend too much time refining the trained model if you already obtain a good enough
evaluation criterion. Improving test accuracy by 0.2% may not be worthwhile if it is well below
the error margin related to the size of your dataset. Do not forget all the business objectives of
your study, such as interpretability, deployment time, and costs, which may be more important than
a small improvement in accuracy.</p>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Remember that the scoring process is just one step within a project, which may involve subsequent
steps with large variance. For example, the effectiveness of a marketing campaign is likely to vary
considerably depending on the quality of the messages sent to customers.</p>
</div>
<h5>Deploying the Model on the Whole Database</h5>
<p>With Khiops, you simply perform a <strong>Deploy model</strong> applied to the whole database to build a score
for all customers within your perimeter.</p>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>A simpler model will be faster and cheaper to deploy on the whole database, and may be sufficient
for your business objectives.</p>
</div>


*Source: [discussion #1006](https://github.com/orgs/KhiopsML/discussions/1006)*

<a id="discussion-1104"></a>
## Elephant instances in multi\-table databases

<h3>Elephant instances in multi-table databases</h3>
<h4>Definition</h4>
<p>In multi-table databases, a main entity (for example, a customer) is described by many records in one or more secondary tables (for example, purchase logs).</p>
<p>&quot;Elephant instances&quot; are entities with so many secondary records that loading them into memory is impractical or impossible. Common examples are telecommunication subscribers with massive call detail records (CDRs) and users whose navigation or event logs on a website or app grow extremely large. This most often occurs in B2B contexts where a few entities produce far more records than typical.</p>
<h4>Problems caused by elephant instances</h4>
<p>Feature engineering usually computes variables for each main entity by loading the entity together with all its secondary records and summarizing them (e.g., number of logs, number of distinct products, total amount, per-day or per-category aggregates).</p>
<p>This process can fail for two main reasons:</p>
<ul>
<li>insufficient memory to store all secondary records;</li>
<li>insufficient spare (working) memory for the computations themselves.</li>
</ul>
<p>When frameworks cannot handle these cases they may crash or stop processing, which is unacceptable for production pipelines and critical scoring systems.</p>
<h4>How Khiops handles elephant instances</h4>
<p>Khiops is designed to process multi-table data robustly and to avoid crashes or pipeline interruptions when elephant instances occur. It applies different strategies depending on the situation.</p>
<h5>Instances too large to load into memory</h5>
<p>Native variables are fields stored on the main entity record (e.g., customer attributes) and do not require loading secondary tables.</p>
<p>If an instance cannot be loaded, Khiops keeps only the native variables from the main entity; all engineered features are marked missing because they could not be computed.</p>
<p>Khiops emits a warning with detailed information regarding lack of memory to load elephant instances.</p>
<div class="highlight">
<pre><code>warning : Database ./customer_dataset.txt : Record 340 : Single instance [USER_000340] requires too much memory (more than 812.0 MB of RAM)
after reading 4,915,210 secondary records out of 5,105,000 : only the native variables are kept, the others are defined as missing values
</code></pre>
</div>
<h5>Instances that fit but lack working memory for computation</h5>
<p>If the instance can be loaded but there is not enough spare memory to compute features, Khiops may skip feature computation for that instance and keep only native variables (engineered features set to missing).</p>
<p>Khiops emits a warning with detailed information regarding lack of memory to process elephant instances.</p>
<div class="highlight">
<pre><code>warning : Database ./customer_dataset.txt : Record 550 : Single instance [USER_000550] requires too much memory (more than 967.0 MB of RAM)
after reading 4,105,000 secondary records and calculating the values of 35 variables out of at least 3353 : 
only the native variables are kept, the others are defined as missing values
</code></pre>
</div>
<h5>Instances handled by multiple passes (time trade-off)</h5>
<p>When memory is tight but recoverable, Khiops will free memory periodically and compute features iteratively across several passes. All derived variables can be computed at the cost of additional computation time.</p>
<p>Khiops notifies the user that computation completed using multiple passes to save RAM.</p>
<div class="highlight">
<pre><code>warning : Database ./customer_dataset.txt : Record 730 : Single instance [USER_000730] containing 3,507,000 secondary records : 
all derived variables have been computed using RAM sparingly at the expense of computation time (6 additional passes)        
</code></pre>
</div>
<h5>Instances that should be noticed</h5>
<p>When an instance is large but handled normally, Khiops still emits a warning so the data miner is informed.</p>
<p>Khiops issues a notice to highlight unusually large instances for review.</p>
<div class="highlight">
<pre><code>warning : Database ./customer_dataset.txt : Record 890 : Single instance [USER_000890] containing 397,620 secondary records
</code></pre>
</div>
<h4>Recommendations</h4>
<p>To reduce the occurrence or impact of elephant instances consider:</p>
<ul>
<li>Increase available RAM where possible.</li>
<li>Reduce parallelism (fewer workers/cores) to increase RAM per worker.</li>
<li>Pre-aggregate by time window or sample older/less relevant records.</li>
<li>Use approximate algorithms (HyperLogLog, Count-Min Sketch) for large-cardinality or heavy-hitter estimates.</li>
</ul>


*Source: [discussion #1104](https://github.com/orgs/KhiopsML/discussions/1104)*
