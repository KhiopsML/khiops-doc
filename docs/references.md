---
hide: toc
---

# Bibliography { #publications }

!!! info "How to cite Khiops"
    If you use **Khiops** in your research, papers, or projects, please cite our main reference article:
    <br>
    **Khiops: An End-to-End Frugal AutoML and XAI Machine Learning Solution for Large Multi-Table Databases** - [download:octicons-link-external-16:][key_paper_khiops]{:target="_blank"}

    ??? quote "BibTeX Citation"
        ```bibtex
            @inproceedings{boulle2025khiopscaid,
            author    = {Marc Boull{\'e} and Nicolas Voisine and Bruno Guerraz and Carine Hue and Felipe Olmos and Vladimir Popescu and St{\'e}phane Gouache and St{\'e}phane Bouget and Alexis Bondu and Luc Aur{\'e}lien Gauthier and Yassine Nair Benrekia and Fabrice Cl{\'e}rot and Vincent Lemaire},
            title     = {Khiops: An End-to-End, Frugal {AutoML} and {XAI} Machine Learning Solution for Large, Multi-Table Databases},
            booktitle = {Proceedings of the Conference on Artificial Intelligence for Defense (CAID)},
            year      = {2025},
            month     = {November},
            address   = {Rennes, France},
            url       = {https://caid-conference.eu}
            }
        ```

---

To go further, here is a selection of **scientific papers** organized as a reading path designed to clarify the AutoML pipeline.
We highly recommend reading them in the suggested order, after exploring the documentation provided on this website.

!!! note "More than a hundred articles about Khiops are available [on this page:octicons-link-external-16:][home_page_marc]{:target="_blank"}. "

[home_page_marc]: http://www.marc-boulle.fr/author/Marc.Boulle-eng.html

## Suggested Reading Path

The <span style="color:gray">**gray**</span> entries indicate complementary material that can be read later on, without hindering your overall understanding of the pipeline.

### Optimal Encoding

1. **Discretization models:** MODL: a Bayes optimal discretization method for continuous attributes - [download:octicons-link-external-16:][paper_discretization]{:target="_blank"}
2. **Grouping models:** A Bayes optimal approach for partitioning the values of categorical attributes - [download:octicons-link-external-16:][paper_grouping]{:target="_blank"}
3. <span style="color:gray">**The regression case:** A New Probabilistic Approach In Rank Regression with Optimal Bayesian Partitioning - [download:octicons-link-external-16:][paper_regression]{:target="_blank"}</span>

### Auto Feature Engineering

1. **Multi-table data:** A scalable robust and automatic propositionalization approach for Bayesian classification of large mixed numerical and categorical data - [download:octicons-link-external-16:][paper_multitable]{:target="_blank"}
2. <span style="color:gray">**Decision trees:** A Bayes Evaluation Criterion for Decision Trees - [download:octicons-link-external-16:][paper_tree]{:target="_blank"}</span>
3. <span style="color:gray">**Pair discretization:** Optimum simultaneous discretization with data grid models in supervised classification: a Bayesian model selection approach - [download:octicons-link-external-16:][paper_pair]{:target="_blank"}</span>

### Parsimonious Training

1. **Fractional Naive Bayes (FNB):** Non-convex optimization for a parsimonious weighted selective naive Bayes classifier - [download:octicons-link-external-16:][paper_fnb]{:target="_blank"}
2. **Previous versions (Khiops <v10):** Compression-Based Averaging of Selective Naive Bayes Classifiers - [download:octicons-link-external-16:][paper_snb]{:target="_blank"}



[key_paper_khiops]: assets/papers/2508.20519v3.pdf
[paper_discretization]: assets/papers/BoulleML06.pdf
[paper_fnb]: assets/papers/2409.11100v1.pdf
[paper_grouping]: assets/papers/BoulleJMLR05.pdf
[paper_multitable]: assets/papers/BoulleEtAlML19.pdf
[paper_pair]: assets/papers/BoulleADAC09.pdf
[paper_regression]: assets/papers/HueEtAlJMLR07.pdf
[paper_snb]: assets/papers/BoulleJMLR07.pdf
[paper_tree]: assets/papers/VoisineEtAlAKDM09.pdf
