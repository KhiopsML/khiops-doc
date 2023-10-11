# Khiops Visualization

The visualisation tool is available standalone. You can find all versions on the [the following link][windows visu] or download the latest stable version below:

[windows visu]: https://github.com/khiopsrelease/kv-release/releases/tag/v10.2.8

<a href="https://github.com/khiopsrelease/kv-release/releases/download/v10.2.8/khiops-visualization-Setup-10.2.8.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
</a>
<a href="https://github.com/khiopsrelease/kv-release/releases/download/v10.2.8/khiops-visualization-10.2.8.dmg">
        <button class="btn btn-light btn-sm">
          Download for Mac OS
        </button>
</a>  
<a href="https://github.com/khiopsrelease/kv-release/releases/download/v10.2.8/khiops-visualization_10.2.8_amd64.deb">
        <button class="btn btn-light btn-sm">
          Download for Ubuntu
        </button>
</a>
<a href="https://github.com/khiopsrelease/kv-release/releases/download/v10.2.8/khiops-visualization-10.2.8.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          Download for CentOS
        </button>
</a>

## Introduction
The results of the Khiops analysis are stored in a dedicated report (with extension .khj) with a JSON file structure. The user can parse this report to build her custom visualization, but the most useful insights can be easily accessed through a dedicated interactive visualization interface. The interface is invoked by double-clicking on the icon of a khj file or by launching Khiops visualization and opening the file from the "File" menu.

The interface is organized as a set of tabs, each showing specific information in dedicated panels. Some panels come with (hopefully) self-explanatory controls; information about a control can be obtained by pointing the mouse on it. The list of controls and their function is given at the end of this document.

As supervised and non-supervised (hereafter descriptive) analyses have different goals and produce different kinds of results, the visualization interface and the content of the tabs are slightly different for both analyses.


## Descriptive analysis visualisation
The report is organized in the following tabs :

- Preparation
- Preparation 2D (only in case of constructed bivariate variables)
- Project information

Unless otherwise specified, we used the Adult database for the figures below.

For the figures below, unless otherwise specified, we used the Adult database.

### Preparation tab
The general layout of this tab is as follows (see the two figures below): Panel A shows some information related to the data and the analysis (left) and the histogram of the target modalities (right). Panel B stores the list of the variables as a table together with some descriptive statistics information. 

Clicking on a line of the table in panel B displays the histogram of the corresponding variable in panel C and information about the variable (Name and derivation rule(if any)) in panel D. Clicking on a bin of the histogram displays information about this bin in panel E. 

Categorical and numerical variables have different histograms.

For categorical variables, the number of bins is automatically set to its optimal value from an MDL approach.
In the case of a variable with many categories, a specific bin ("Default group index") may gather many modalities and be shown with a different color. This specific bin is given the name of its most populated modality, and clicking on the bin makes its content available in panel E. As it may gather many small modalities, it may appear as the dominant bin of the distribution, and the name might be misleading, therefore the different color.
The Coverage/Frequency toggle allows the display of either the coverage (in %, linear scale) or the populations (in log scale).

<img style="width: -webkit-fill-available;" src="/assets/images/Categorical preparation.png" ;></img>

The figure above shows the histogram of the variable "native_country" with 41 modalities. The default group is selected, and its content is displayed in panel E.

For numerical variables, the bounds of the bins are also automatically set to their optimal value from an MDL approach.

<img style="width: -webkit-fill-available;" src="/assets/images/Numerical preparation.png" ;></img>

Different representations of the histogram are available. The y-axis shows the density and can be plotted in linear or log scale.
The x-axis can also be plotted in linear or log scale; for the log scale representation, the variable range is split in (up to) three areas :

- the bins in the negative range, excluding any bin containing zero (even as a bound)
- the bins containing zero (one or two bins, if zero is a bound)
- the bins in the positive range, excluding any bin containing zero (even as a bound)

The log scale for the negative range is log10(-x), running to infinity toward the left.
The log scale for the positive range is log10(x), running to infinity towards the right.
The bins containing zero are given an arbitrary width, set to 1/10 of the figure.
This allows the plotting of informative histograms of challenging heavy-tailed distributions such as the Cauchy distribution. 


### Preparation 2D
The general layout is similar to the Preparation tab, except for panel C, which shows the bivariate discretization of the pair selected in panel B.
This discretization is the cartesian product of the parts of each variable. By default, the information displayed on the subtab "Matrix" is the mutual information between both groupings, allowing to analyze the correlations between the variables of the pair. Other information, such as the frequencies in each cell, can be selected from the menu.
The subtab "Cells" displays the information about the cell statistics as a table.

<img style="width: -webkit-fill-available;" src="/assets/images/Preparation 2D.png" ;></img>

### Project information
This tab shows information related to the project, particularly the content of the "Short description" field.

<img style="width: -webkit-fill-available;" src="/assets/images/Project info.png" ;></img>

## Supervised analysis
There are two different reports depending on the categorical or numerical nature of the target variable.

### Classification
The target variable is categorical.

The report is organized in the following tabs :

- Preparation
- Tree Preparation (only in case of constructed decision tree variables)
- Preparation 2D (only in case of constructed bivariate variables)
- Modeling
- Evaluation
- Project information

For the figures below, we used the Adult database, with "education" as a target variable (excluding "education num" from the predictors) and randomly selecting 70% of the data for the train set and the remaining 30% for the test set.

#### Preparation
Panel A shows some information related to the data and the analysis (left) and the histogram of the target modalities (right). Panel B stores the list of the variables as a table together with some descriptive statistics information. 
Clicking on a line of the table in panel B displays the information about the parts obtained from the optimal supervised grouping of the selected variable in panel C and information about the variable (Name and derivation rule(if any)) in panel D. Panel C shows the histogram of the group populations (top) and the distribution of the target modalities conditional to the group (bottom) for each group.

Group population histogram can be displayed in linear or log scale from the menu above the figure.
For the target modalities conditional to the group histogram, displayed target modalities can be selected from the "Values" menu, and the histogram can be displayed as probabilities or lift ("Probabilities/Lift" toggle).

Clicking on a bin of the population histogram or the corresponding target conditional histogram displays information about the selected group in panel E.

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Preparation.png" ;></img>

#### Tree Preparation
Decision trees are treated as categorical variables with as many modalities as terminal leaves.
The general layout of panels A, B, and C and the information they display are similar to the Preparation tab.
Panel D shows the content of a selected group of leaves as a table of the leaves in the group and their target modalities statistics. Clicking on a leaf displays information about this leaf in panel E: subtab "Leaf infos" shows the histogram of the target modalities conditional to this leaf, together with the leaf population and leaf purity; subtab "Leaf rules" gives the list of tests leading to this leaf, starting from the root node.
The left panel (panel F) is a hypertree visualization of the selected decision tree. Only terminal leaves are clickable; clicking on a leaf dynamically points to the relevant leaf and group of leaves information in the other panels. The population and purity of the leaves can be visualized by their size and color density. This can be toggled on and off, and the "values" menu allows to select some of the target modalities only.

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Tree Preparation.png" ;></img>

#### Preparation 2D
The general layout is similar to the Preparation tab, except for panel C, which shows the bivariate supervised discretization of the pair selected in panel B.
This discretization is the cartesian product of the parts for each variable. By default, the information displayed on the subtab "Matrix" is the mutual information between a cell of the cartesian product and a modality of the target variable (selected from the "Target" menu), allowing analysis of the information brought by the variables as a pair to the target variable. Other information, such as the frequencies in each cell, can be selected from the menu.
The subtab "Cells" displays the information about the cell statistics as a table.
Clicking on a cell displays the target modalities histogram conditional to this cell (bottom of panel C) and the information about the parts of the selected cell in panel E.

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Preparation 2D.png" ;></img>

#### Modeling
The general layout is similar to the Preparation tab. Panel B shows information related to those variables used in the model only. The tables show each variable's level, weight (in the weighted naive Bayes model), and importance (computed as the geometric mean of the level and the weight).

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Modeling.png" ;></img>

#### Evaluation
This tab gathers information about the performance of the model.
Panel A shows which datasets are concerned by the analysis. 
Panel B gives some performance indicators for the model: accuracy, compression rate, the area under the lift curve (AUC), and Gini coefficient.
Panel C shows the lift curves: the target modality can be chosen from the menu at the top, and the "Filter curves" menu allows to choose which curves are displayed. The lift curve plots the target modality coverage as a function of the population selected according to the model score.
Panel D shows a confusion matrix ($modality is the predicted modality). 

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Evaluation.png" ;></img>


#### Project information
This tab shows information related to the project, particularly the content of the "Short description" field.

<img style="width: -webkit-fill-available;" src="/assets/images/Classification Project info.png" ;></img>

### Regression
The target variable is numerical. The report is organized in the following tabs :

- Preparation
- Modeling
- Evaluation
- Project information

For the figures below, we used the Adult database, with "education" as a target variable (excluding "education num" from the predictors) and randomly selecting 70% of the data for the train set and the remaining 30% for the test set.

#### Preparation
Panel A shows some information related to the data and the analysis.
Panel B stores the list of the variables as a table together with some descriptive statistics information. 
Clicking on a line of the table in panel B displays the information about the parts obtained from the optimal supervised grouping of the selected variable in panel C and information about the variable (Name and derivation rule(if any)) in panel D.

The top of Panel C shows the histogram of the group populations obtained from the optimal supervised grouping for the predictive variable.
The bottom of panel C shows the optimal grouping of the (predictive variable and target variable) pair. 
Note that the discretization of the target variable depends on the predictive variable, which is helpful for interpretation purposes.
By default, the mutual information brought by each cell is given (red means positive association and blue negative association); other information can be selected from the menu.
The toggle Standard/Frequency selects a representation mode
- in "Standard" mode, the span of the group is proportional to the number of modalities in the group for categorical variables or constant for numerical variables
- in "Frequency" mode, the span of a group is proportional to its population

Clicking on a cell of the Cartesian product shows information about the selected group in panel E.

<img style="width: -webkit-fill-available;" src="/assets/images/Regression Preparation.png" ;></img>


#### Modeling
The general layout is similar to the Preparation tab. Panel B shows information related to those variables used in the model only. The table shows each variable's level, weight (in the weighted naive Bayes model), and importance (computed as the geometric mean of the level and the weight).

<img style="width: -webkit-fill-available;" src="/assets/images/Regression Modeling.png" ;></img>

#### Evaluation
This tab gathers information about the performance of the model.
Panel A shows which datasets are concerned by the analysis. 
Panel B gives some performance indicators for the model: rmse, mae, [nlpd][NLPD] (negative log predictive density) and their equivalents for rank regression (e.g. the [rank negative log predictive density][rnldp]).
Panel C shows the [REC][REC] curves: the target modality can be chosen from the menu at the top, and the "Filter curves" menu allows to choose which curves are displayed.

<img style="width: -webkit-fill-available;" src="/assets/images/Regression Evaluation.png" ;></img>

[nlpd]: https://en.wikipedia.org/wiki/Negative_log_predictive_density
[rnldp]: https://www.jmlr.org/papers/volume8/hue07a/hue07a.pdf
[REC]: https://dl.acm.org/doi/10.5555/3041838.3041844

####  Project information
This tab shows informations related to the project, in particular, the content of the "Short description" field.

<img style="width: -webkit-fill-available;" src="/assets/images/Regression Project info.png" ;></img>

## Controls elements

Control elements appear at the top right of the panels.

<img style="width: -webkit-fill-available;" src="/assets/images/Control.png" ;></img>

At the top right of the screen, 
<img src="/assets/images/Control General.png" ;></img>
from left to right :

- allows setting some environment variables such as the number of significant digits or the clear/dark mode. These settings are kept across sessions ;
- allows to copy the figure of a selected panel (select a panel by clicking on it; a selected panel appears with a light blue border). This can be pasted into any other document ;
- allows the copy of the data of a selected panel.

At the top right of panel A <img  src="/assets/images/Control Panel A.png" ;></img> from left to right:

- allows to open a bar plot of the levels of the variables in decreasing order ;
- allows to open a search box on the variable names (fill at least two characters) ;
- allows to fit the table to the panel size ;
- allows to fit the columns of the table to their content ;
- allows to select/unselect columns to the table ;
- allows to open the panel in full screen. 

The control <img  src="/assets/images/Control Panel A 2.png" ;></img> at the top right of the full screen, the panel allows to go back to the multi-panel interface.

At the top right of panel B
<img  src="/assets/images/Control Panel B.png" ;></img>
allows to modify the horizontal scale of the histogram (by default, all groups appear in the figure, which may be messy when there are many groups).

Additional elements apply to bivariate cartesian product visualizations.

<img  src="/assets/images/Control 2D.png" ;></img>

On the left side of the panel (in full-screen mode, here), from top to bottom:

- allows to zoom in on the figure (horizontal and vertical sliders allow to move in the figure) ;
- allows to reset the figure to its original scale ;
- allows to zoom out of the figure
- allows to transpose the figure.