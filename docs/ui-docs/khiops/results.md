# Results

![](../../assets/images-khiops-guides/khiops/image23.png)

**Result files directory**: name of the directory where the results files are stored (default: empty). By default, the results files are stored in the directory of the train database. If a result directory is specified, it can be:

- an absolute path (example "c:\\project\\scenario1"): the results files are stored in this directory

- a local path (example "scenario1"): the results files are stored in a sub-directory of the train database directory

- a relative path (example ".\\scenario1"): the results files are stored in a sub-directory of current directory (Khiops executable start directory)

**Result files prefix**: (default: empty). This prefix is added before the name of each result file.

**Short description**: (default: empty). Brief description to summarize the current analysis, which will be included in the reports.

The following result file names allow to specify the name of each report or model resulting from an analysis. When a file name is missing, the corresponding report is not produced.

**Preparation report**: name of the data report file produced after the univariate data analysis on the train database (default: PreparationReport.xls).

**2D preparation report**: name of the report file produced after the bivariate data analysis on the train database (default: Preparation2DReport.xls).

**Modeling dictionary file**: name of the dictionary file that contains the trained predictors (default: Modeling.kdic). This dictionary file can then be used to deploy the predictors on new data.

**Modeling report**: name of the report file produced once the predictors have been trained (default: ModelingReport.xls).

**Train evaluation report**: name of the report file produced after the evaluation of the predictors on the train database (default: TrainEvaluationReport.xls).

**Test evaluation report**: name of the report file produced after the evaluation of the predictors on the test database (default: TestEvaluationReport.xls).

**JSON report**: name of the JSON file that contains the results of all the reports (default: AllReports.khj). The JSON file is useful to inspect the modeling results from any external tool. For example, the khiops-python library enables to exploit any Khiops modeling results from python.
