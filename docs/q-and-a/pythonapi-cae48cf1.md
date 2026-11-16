# Python API and development

<a id="discussion-825"></a>
## How can you create custom features with the Khiops Python API?

<h3>Example: Building a ratio feature</h3>
<p>Custom features can be added by using the Khiops dictionary API, which is included in the Khiops Core API.
For an introduction to the concept of Khiops dictionaries, we can refer to <a href="https://khiops.org/api-docs/">https://khiops.org/api-docs/</a> on the official Khiops web site. For starting using and defining Khiops dictionaries, we can start from <a href="https://khiops.org/tutorials/kdic_intro/">https://khiops.org/tutorials/kdic_intro/</a>.</p>
<p>To answer to the original example question, a ratio-like feature can be defined by using the <a href="https://khiops.org/api-docs/kdic/math-rules/#divide"><code>Divide</code></a> rule, as in the following example, where the credit utilization rate of each customer is computed as the ratio between the account balance and the credit line,
in the <code>CreditInformation</code> dictionary file:</p>
<div class="highlight">
<pre><code class="language-kdic"><span class="kd">Dictionary</span><span class="w">  </span><span class="nc">CreditInformation</span>
<span class="p">{</span>
<span class="w">  </span><span class="kt">Categorical</span><span class="w">  </span><span class="na">CustomerId</span><span class="w">    </span><span class="p">;</span>
<span class="w">  </span><span class="kt">Categorical</span><span class="w">  </span><span class="na">CreditId</span><span class="w">    </span><span class="p">;</span>
<span class="w">  </span><span class="kt">Numerical</span><span class="w">  </span><span class="na">AccountBalance</span><span class="w">    </span><span class="p">;</span>
<span class="w">  </span><span class="kt">Numerical</span><span class="w">  </span><span class="na">CreditLine</span><span class="w">    </span><span class="p">;</span>
<span class="w">  </span><span class="kt">Numerical</span><span class="w">  </span><span class="na">CreditUtilizationRate</span><span class="w">   </span><span class="o">=</span><span class="w"> </span><span class="nf">Divide</span><span class="p">(</span><span class="na">AccountBalance</span><span class="p">,</span><span class="w"> </span><span class="na">CreditLine</span><span class="p">)</span><span class="w">  </span><span class="p">;</span>
<span class="p">};</span>
</code></pre>
</div>
<p>Such a dictionary can be constructed via the <a href="https://khiops.org/api-docs/python-api/"><code>core</code> API</a> of the Khiops Python library:</p>
<div class="highlight">
<pre><code class="language-python"><span class="c1"># Perform the necessary imports</span>
<span class="kn">from</span><span class="w"> </span><span class="nn">khiops</span><span class="w"> </span><span class="kn">import</span> <span class="n">core</span> <span class="k">as</span> <span class="n">kh</span>

<span class="c1"># Build empty dictionary domain object</span>
<span class="n">credit_information_dict_domain</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">DictionaryDomain</span><span class="p">()</span>

<span class="c1"># Build empty dictionary object; specify its name</span>
<span class="n">credit_information_dict</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Dictionary</span><span class="p">()</span>
<span class="n">credit_information_dict</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;CreditInformation&quot;</span>

<span class="c1"># Build customer ID variable; specify its name and type</span>
<span class="n">customer_id</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Variable</span><span class="p">()</span>
<span class="n">customer_id</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;CustomerId&quot;</span>
<span class="n">customer_id</span><span class="o">.</span><span class="n">type</span> <span class="o">=</span> <span class="s2">&quot;Categorical&quot;</span>

<span class="c1"># Build credit ID variable; specify its name and type</span>
<span class="n">credit_id</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Variable</span><span class="p">()</span>
<span class="n">credit_id</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;CreditId&quot;</span>
<span class="n">credit_id</span><span class="o">.</span><span class="n">type</span> <span class="o">=</span> <span class="s2">&quot;Categorical&quot;</span>

<span class="c1"># Build account balance variable; specify its name and type</span>
<span class="n">account_balance</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Variable</span><span class="p">()</span>
<span class="n">account_balance</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;AccountBalance&quot;</span>
<span class="n">account_balance</span><span class="o">.</span><span class="n">type</span> <span class="o">=</span> <span class="s2">&quot;Numerical&quot;</span>

<span class="c1"># Build credit line variable; specify its name and type</span>
<span class="n">credit_line</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Variable</span><span class="p">()</span>
<span class="n">credit_line</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;CreditLine&quot;</span>
<span class="n">credit_line</span><span class="o">.</span><span class="n">type</span> <span class="o">=</span> <span class="s2">&quot;Numerical&quot;</span>

<span class="c1"># Built credit utilization rate variable; specify its name and type</span>
<span class="n">credit_utilization_rate</span> <span class="o">=</span> <span class="n">kh</span><span class="o">.</span><span class="n">Variable</span><span class="p">()</span>
<span class="n">credit_utilization_rate</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="s2">&quot;CreditUtilizationRate&quot;</span>
<span class="n">credit_utilization_rate</span><span class="o">.</span><span class="n">type</span> <span class="o">=</span> <span class="s2">&quot;Numerical&quot;</span>

<span class="c1"># Add variable construction rule</span>
<span class="n">credit_utilization_rate</span><span class="o">.</span><span class="n">rule</span> <span class="o">=</span> <span class="s2">&quot;Divide(AccountBalance, CreditLine)&quot;</span>

<span class="c1"># Add variables to the credit information dictionary</span>
<span class="k">for</span> <span class="n">variable</span> <span class="ow">in</span> <span class="p">[</span>
    <span class="n">customer_id</span><span class="p">,</span> <span class="n">credit_id</span><span class="p">,</span> <span class="n">account_balance</span><span class="p">,</span> <span class="n">credit_line</span><span class="p">,</span> <span class="n">credit_utilization_rate</span>
<span class="p">]:</span>
    <span class="n">credit_information_dict</span><span class="o">.</span><span class="n">add_variable</span><span class="p">(</span><span class="n">variable</span><span class="p">)</span>

<span class="c1"># Add credit information dictionary to the dictionary_domain</span>
<span class="n">credit_information_dict_domain</span><span class="o">.</span><span class="n">add_dictionary</span><span class="p">(</span><span class="n">credit_information_dict</span><span class="p">)</span>

<span class="c1"># Write the credit information dictionary domain to a file on disk</span>
<span class="n">credit_information_dict_domain</span><span class="o">.</span><span class="n">export_khiops_dictionary_file</span><span class="p">(</span>
    <span class="s2">&quot;/path/to/credit_information.kdic&quot;</span>
<span class="p">)</span>
</code></pre>
</div>
<p>Thus, a Khiops dictionary file with the <code>.kdic</code> extension and the precise contents shown above is
written on the storage to the specified path.</p>


*Source: [discussion #825](https://github.com/orgs/KhiopsML/discussions/825)*

<a id="discussion-933"></a>
## Why doesn’t Khiops expose a random seed parameter?

<h3>Variance Analysis, Parameters and Reproducibility via Khiops</h3>
<h4>Evaluating the Variance of Prediction Results</h4>
<ul>
<li>This is of natural interest in data mining.</li>
<li>It is usually addressed using techniques such as cross-validation or bootstrapping, where the analysis method is applied on multiple samples.</li>
</ul>
<h4>Evaluating the Variance of an Algorithm with Respect to Its Parameters</h4>
<ul>
<li>This process is called sensitivity analysis.</li>
<li>It is particularly important for new techniques and research purposes.</li>
<li>It mainly concerns user-defined technical parameters (e.g., the width or shape of a kernel) to provide recommendations for their optimal choices.</li>
<li>Generally, random seeds are not considered as user parameters, but it can be interesting to study the variance of results with respect to the random seed.
<ul>
<li>High variance related to the random seed usually indicates instability, which is undesirable.</li>
</ul>
</li>
</ul>
<h4>Khiops Parameters</h4>
<ul>
<li>Khiops does not have such technical parameters</li>
<li>Khiops is an AutoML solution designed to be as simple as possible to use.</li>
<li>Only a minimal set of user parameters are available:
<ul>
<li>Problem specification: dictionary, database, target variable.</li>
<li>Business constraints:
<ul>
<li>Trade-off between accuracy, modeling, training, and deployment time (e.g., number of generated features, trees...).</li>
<li>Interpretability constraints (e.g., maximum number of selected variables, maximum number of part per preprocessed variable...).</li>
</ul>
</li>
<li>Others as needed.</li>
</ul>
</li>
<li>Technical parameters are never exposed to the user.
<ul>
<li>They may be available as hidden parameters for the Khiops team, for research purposes.</li>
</ul>
</li>
</ul>
<h4>Reproducibility of Results</h4>
<ul>
<li>Importance:
<ul>
<li>For the user: ensuring that running the same workflow produces consistent results.</li>
<li>For debugging: reproducing issues reported by users.</li>
<li>For extensive non-regression testing performed by the Khiops team.</li>
</ul>
</li>
<li>How:
<ul>
<li>Fixing the random seed for each algorithm (preprocessing, feature engineering, SNB, etc.).</li>
<li>Managing seeds in parallelized algorithms to ensure consistent results regardless of the number of cores used.</li>
<li>Using stable sorting methods.</li>
<li>Fixing advanced compiler options to ensure stability across different operating systems.</li>
<li>etc.</li>
</ul>
</li>
</ul>


*Source: [discussion #933](https://github.com/orgs/KhiopsML/discussions/933)*
