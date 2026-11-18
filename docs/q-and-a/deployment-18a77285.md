# Deployment and integration

<a id="discussion-520"></a>
## Can Khiops be deployed on Hadoop?

<h3>Deploying Khiops on Hadoop</h3>
<p>Khiops has been used for several years in production on Hadoop using specialized tools we have developed. However, these components are not yet part of its open-source distribution.</p>
<p><strong>Overview of the technical solution</strong></p>
<p>We have developed the following components to enable Khiops integration with Hadoop ecosystems:</p>
<ul>
<li><strong>HDFS driver for Khiops</strong>: A dedicated driver enabling Khiops to read and write directly from HDFS, with full support for multipart files;</li>
<li><strong>Khiops4Spark</strong>: A Spark wrapper that enables Khiops to run on Hadoop clusters through <code>spark-submit</code> command;</li>
<li><strong>Khiops4Yarn</strong>: A Yarn wrapper that allows Khiops to operate directly within Hadoop’s resource management framework.</li>
</ul>
<p>Khiops, as a native MPI (Message Passing Interface) program, works exactly the same on a multicore machine or on a multinode cluster. When deployed on multiple machines, Khiops efficiently leverages the CPU, memory, and I/O resources of each allocated node, ensuring optimal performance at scale. The Spark and Yarn wrappers manage the communication with their respective resource managers, which in turn allocate resources that will be used by Khiops.</p>
<p>If you’re interested in deploying Khiops in such environments or have specific use cases, please reach out via our <a href="https://khiops.org/contact/">contact form</a> for further information.</p>


*Source: [discussion #520](https://github.com/orgs/KhiopsML/discussions/520)*

<a id="discussion-852"></a>
## Can a trained Khiops model be converted to SQL scripts or PMML?

<h3>Deploying Khiops models with dictionaries</h3>
<p>Khiops does <strong>not</strong> provide an export of models to SQL or PMML. The main reason is that <strong>a full Khiops model cannot be faithfully represented in these formats</strong>.</p>
<p>Khiops relies on a rich dictionary layer and native multi-table modeling (keys, aggregations, derived variables, discretizations, value groups, special-value handling). <strong>Standard PMML cannot express many of these operations</strong>, and generating equivalent SQL would lead to extremely complex, environment-dependent code that would be difficult to validate and maintain.</p>
<p>For these reasons, <strong>the project focuses on end-to-end deployment using dictionaries, through the Khiops engine and the Khiops Native Interface, which guarantee consistent and reliable scoring across environments.</strong></p>


*Source: [discussion #852](https://github.com/orgs/KhiopsML/discussions/852)*
