  
## This is not clustering 

Among unsupervised approaches, **clustering** algorithms are undoubtedly the best known. But make no mistake, **co-clustering** is a very different problem. To clarify the distinction between clustering and co-clustering, let's start by distinguishing their respective objectives: 

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

Coclustering algorithms simultaneously group the **rows** and **columns** of a matrix, usually a **contingency matrix** describing the co-occurrences of two categorical variables. This contingency matrix contains the number of individuals for each modality combination of the two categorical variables studied. The intersection (i.e. the cartesian product) of the groups formed on the two dimentions of the matrix constitute a set of **coclusters** (represented by the bins in the figure above). A cocluster characterizes a **sub-part** of the matrix by aggregating the information it contains, i.e. the number of individuals whose combinations of modalities on the two variables belong to the cocluster. Finally, a coclustering model gives an aggregated view of a contingency matrix describing the **dependency** between the two variables under study, and it can be seen as a model of the **joined density** of the two variables.  



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

!!! example "MODL generalizes coclustering"
    - Extension to **numerical variables**.
    - **Mixing** numerical and categorical variables.
    - Generalization to **more than two** variables.


Thanks to the extensions allowed by the MODL formalism, coclustering can be applied to a **large range of applications** involving data of very different kinds. Here are just a few examples:    
 
**Time series**: Khiops coclustering can be applied to time series by **encoding each measurement** of the series with the following three variables: (i) the identifier of the time series (**id**: categorical); (ii) the measurement value (**x**: numerical); (iii) a time variable representing the time of day (**t**: numerical). In this case, the coclustering algorithm discretizes the three dimensions jointly, clustering time series on the *id* dimension, and forming intervals of values on the other two dimensions *x* and *t*. The following figure shows an example of a group formed using household electricity consumption, which is a very chaotic kind of time series. Each group of series is then represented by a joint density describing the distrition of *measurements* as a function of *time* (left-hand side of the figure below). Being very chaotic, the time series belonging to this group would have been considered **far** from each other by a clustering algorithm based on a **distance**, such as the Euclidean distance (right-hand side of the figure below). Finally, this example illustrates one of the advantages of Khiops coclustering, which does not require a priori choosing a distance function.

<figure markdown>
<picture>
  <source srcset="/assets/images/ex_coclustering_timeseries.webp" type="image/webp">
  <img style="width:75%;" src="/assets/images/ex_coclustering_timeseries.png" alt="ex_coclustering_timeseries" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure> 

- Graphs -> détection de cliques et d'anti-cliques
     
<figure markdown>
<picture>
  <source srcset="/assets/images/ex_coclustering_graph.webp" type="image/webp">
  <img style="width:75%;" src="/assets/images/ex_coclustering_graph.png" alt="ex_coclustering_graph" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure> 


## Intuition du critère 

!!! example "MODL sécurise l'utilisation du coclustering"
    - Pas de choix a priori sur le **nombre de groupes**
    - Garantie de ne **pas former de groupe** en cas **d'indépendance** des variables
    - Garantie contre le **surajustement**


## Modèle parameter 

## Optimisation criterion 

## Algorithme 




