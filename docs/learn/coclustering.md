  
## This is not clustering 

Among unsupervised approaches, **clustering** algorithms are undoubtedly the best known. But make no mistake, **coclustering** is a very different problem. To clarify the distinction between clustering and coclustering, let's start by distinguishing their respective objectives. 

!!! example "Objective of clustering"
    Group the rows of a *data set* into homogeneous *groups of individuals*.

<figure markdown>
<picture>
  <source srcset="/assets/images/exemple_clustering.webp" type="image/webp">
  <img style="width:70%;" src="/assets/images/exemple_clustering.png" alt="exemple_clustering" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

As shown in this figure, clustering algorithms are used to find **homogeneous subpopulations** within a **data set**. These algorithms are generally based on a **distance**, which can take various forms and which is used to identify groups: (i) as far away as possible from each other; (i) whose individuals are as close as possible to each other. In practice, the choice of this distance has a significant impact on clustering results, as it constitutes a kind of **apriori knowledge** used to simplify the problem and make algorithms computationally efficient. It should also be noted that clustering algorithms generally involve choosing the **number of groups** to be formed, with no guarantee that there are actually identifiable sub-populations in the dataset.

!!! example "Objective of coclustering"
    Group *rows* and *columns* of a *matrix* to study the *dependency* between its two dimensions.  

<figure markdown>
<picture>
  <source srcset="/assets/images/exemple_coclustering.webp" type="image/webp">
  <img style="width:70%;" src="/assets/images/exemple_coclustering.png" alt="exemple_coclustering" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

coclustering algorithms simultaneously group the **rows** and **columns** of a matrix, usually a **contingency matrix** describing the co-occurrences of two categorical variables. This contingency matrix contains the number of individuals for each modality combination of the two categorical variables studied. The intersection (i.e. the cartesian product) of the groups formed on the two dimentions of the matrix constitute a set of **coclusters** (represented by the bins in the figure above). A cocluster characterizes a **sub-part** of the matrix by aggregating the information it contains, i.e. the number of individuals whose combinations of modalities on the two variables belong to the cocluster. Finally, a coclustering model gives an aggregated view of a contingency matrix describing the **dependency** between the two variables under study, and it can be seen as a model of the **joined density** of the two variables.  



!!! info "What you need to know"
    Like **clusterring**, **coclustering** is a powerful tool for exploratory annalysis, but these two types of approach apply to different kinds of **data** (as shown in the figure below) and their **objectives** are not the same.

<figure markdown>
<picture>
  <source srcset="/assets/images/data_clustering_coclustering.webp" type="image/webp">
  <img style="width:95%;" src="/assets/images/data_clustering_coclustering.png" alt="data_clustering_coclustering" loading="lazy"> 
</picture>
  <figcaption>Two different kinds of data used</figcaption>
</figure> 

## A wide range of applications

The coclustering problem is also known as **biclustering**, because only two dimensions of the input matrix are involved. As such, coclustering is a relatively **limited** problem, restricted to the study of two categorical variables.

!!! success "MODL generalizes coclustering"
    - Extension to **numerical variables**.
    - **Mixing** numerical and categorical variables.
    - Generalization to **more than two** variables.


Thanks to the extensions allowed by the MODL formalism, coclustering can be applied to a **large range of applications** involving data of very different kinds. Here are just a few examples:    
 
- **Time series** can be [studied:octicons-link-external-16:][coclustering_timeseries]{:target="_blank"} using Khiops coclustering by **encoding each measurement** of the series with the following three variables: (i) the identifier of the time series (*id*: categorical); (ii) the measurement value (*x*: numerical); (iii) a time variable representing the time of day (*t*: numerical). In this case, the coclustering algorithm discretizes the three dimensions jointly, clustering time series on the *id* dimension, and forming intervals of values on the other two dimensions *x* and *t*. The following figure shows an example of a group formed using household electricity consumption, which is a very chaotic kind of time series. Each group of series is then represented by a joint density describing the distrition of *measurements* as a function of *time* (left-hand side of the figure below). Being very chaotic, the time series belonging to this group would have been considered **far** from each other by a clustering algorithm based on a **distance**, such as the Euclidean distance (right-hand side of the figure below). Finally, this example illustrates one of the advantages of Khiops coclustering, which does not require a priori choosing a distance function.

[coclustering_timeseries]: https://www.researchgate.net/profile/Asma-Dachraoui-2/publication/283548750_Realistic_and_Very_Fast_Simulation_of_Individual_Electricity_Consumptions/links/563e799b08aec6f17ddaaa0b/Realistic-and-Very-Fast-Simulation-of-Individual-Electricity-Consumptions.pdf

<figure markdown>
<picture>
  <source srcset="/assets/images/ex_coclustering_timeseries.webp" type="image/webp">
  <img style="width:75%;" src="/assets/images/ex_coclustering_timeseries.png" alt="ex_coclustering_timeseries" loading="lazy"> 
</picture>
  <figcaption>An example of a time series group</figcaption>
</figure> 

- **Graphs** are an expressive form of data, which can be employed to describe complex systems such as a telecom network, by encoding the interactions between each of the devices that make it up, or the customers of a telephone operator, by characterizing the interactions between users. Khiops coclustering is an excellent tool for exploring the structure of [large graphs:octicons-link-external-16:][coclustering_graph]. For example, the **arcs of a directed graph** can be encoded by the following two categorical variables: (i) the identifier of the source node; (ii) and the identifier of the target node. In this case, the coclustering algorithm jointly builds groups of source nodes and groups of target nodes, describing the joint density of oriented arcs. The following figure shows an example of how Khiops coclustering can be used to partition a graph. It's important to note that Khiops identifies both groups of nodes that are **strongly connected** to each other, and groups of nodes in which the **interconnections are abnormally weak** compared to the rest of the graph. By extension, [temporal graphs:octicons-link-external-16:][coclustering_temporal_graph] can also be studied by the Khiops coclusring, simply by adding a third **time** variable to the description of the arcs. For example, daily self-service bicycle trips were studied in the city of Paris.


[coclustering_graph]:http://www.marc-boulle.fr/publications/BoulleOPTE04.pdf

[coclustering_temporal_graph]: http://www.marc-boulle.fr/publications/GuigouresEtAlADAC18.pdf


<figure markdown>
<picture>
  <source srcset="/assets/images/ex_coclustering_graph.webp" type="image/webp">
  <img style="width:75%;" src="/assets/images/ex_coclustering_graph.png" alt="ex_coclustering_graph" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure> 

- **Textual data** can also be analyzed using coclustering, especially to uncover relationships between *documents* and the *words* they contain. For example, in a collection of documents, each word can be encoded by two categorical variables: (i) the identifier of the document to which it belongs, and (ii) the word itself. The coclustering algorithm then simultaneously groups sets of documents and sets of words, revealing both underlying **themes or topics** and **document groups** that share common **vocabulary**, while also highlighting the words that characterize each group. Unlike traditional clustering algorithms, Khiops coclustering does **not require** predefining the **number** of topics and document groups, nor even a **distance** between texts (only the co-occurrence of words in texts matters). It is particularly useful for exploring large text collections, such as scientific articles, forums, or social media data, providing a structured and intuitive view of the relationships between content and vocabulary. 


## Intuitions 


!!! question "How is the best model selected?"
    Even for unsupervised approaches, MODL avoids overfitting by selecting the most probable model given the data.

<figure markdown>
<picture>
  <source srcset="/assets/images/coclustering-model-selection.webp" type="image/webp">
  <img style="width:90%;" src="/assets/images/coclustering-model-selection.png" alt="coclustering model selection" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure> 

Like other algorithms based on the MODL (Minimum Description Length) approach, **co-clustering** involves selecting the most probable model given the data. 
During training, a compromise is made to select the best model. 
On one hand, **overly detailed models** are discarded because they tend to **overfit**, capturing noise rather than significat patterns (right side of the figure above). 
On the other hand, **coarse models** are avoided because they **underfit**, missing important dependencies between variables (left side of the figure above).

The optimization criterion used to navigate this trade-off combines two antagonistic components:

- **Prior**: penalizes complex models to prevent overfitting, thanks to its **hierarchical and uniform** structure.
- **Likelihood**: plays the oposite role by favoring models that accurately describe the data.

The most probable model represents a balance point between these opposing objectives, allowing it to properly explain the data — i.e., the dependencies between variables — without unnecessary complexity or overfitting risk. This automatic model selection is entirely driven by the optimization criterion, without requiring the user to specify the number of coclusters which is deduced from data. More generally, MODL coclustering is hyper-parameter free and does not rely on a predefined distance measure, avoiding biases that could influence the results.

!!! question "What is a valuable cocluster in MODL's eyes?"
    Coclustering models describe how data deviate from the independence assumption.

Co-clustering models aim to describe how the training data **deviate** from the **assumption of independence** between variables. 
Coclusters are formed to capture sub-parts of data that are either over-represented or under-represented relative to this independence hypothesis.
The **likelihood** term of the MODL optimization criterion seeks to **maximize this contrast**, effectively highlighting dependencies and structures that differ from what would be expected under independence. Conversely, the **prior** term ensures **robustness** and prevents overfitting by penalizing overly complex models.

The figure below illustrates **when a cocluster provides valuable information** within a coclustering model. Consider a candidate cocluster formed by (i) a group of rows representing 5% of the observations and (ii) a group of columns representing 20%. Under the independence assumption, the expected number of observations in this cocluster would be 1% (calculated by multiplying the probabilities of belonging to each group). If the observed count in this cocluster **deviates** from this expectation — either over-represented or under-represented — it indicates that forming this cocluster **captures meaningful information** about the relationship between the variables described by the model.

<figure markdown>
<picture>
  <source srcset="/assets/images/cocluster-selection.webp" type="image/webp">
  <img style="width:90%;" src="/assets/images/cocluster-selection.png" alt="cocluster interest" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! info "The MODL formalism offers a number of guarantees for data exploration"
    - Pas de choix a priori sur le **nombre de groupes**
    - Garantie de ne **pas former de groupe** en cas **d'indépendance** des variables
    - Garantie contre le **surajustement**


## Modèle parameter 

## Optimisation criterion 

## Algorithme 




