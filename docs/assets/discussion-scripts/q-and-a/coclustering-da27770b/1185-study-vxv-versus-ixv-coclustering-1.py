# Copyright (c) 2023-2026 Orange. All rights reserved.
# This software is distributed under the BSD 3-Clause-clear License, the text of which is available
# at https://spdx.org/licenses/BSD-3-Clause-Clear.html or see the "LICENSE" file for more details.

"""
Khiops Coclustering Study

This script analyzes the behavior of variable-variable and instances-variable coclustering
on bivariate patterns using synthetic data. It performs the following:
- Generate synthetic blob data
- Train Khiops models for univariate histograms
- Train variable-variable coclustering models
- Train instances-variable coclustering models
- Visualize the results

Allows studying various bivariate patterns with or without value ranking.
"""

import warnings
import os
import pandas as pd
import plotly.express as px
from khiops import core as kh
from sklearn import datasets


# ============================================================================
# Configuration
# ============================================================================

# Data generation parameters
N_SAMPLES = 1000
RANDOM_SEED = 30

# File paths (relative to script location)
INPUT_DATA_DIR = "data"
RESULT_DIR = "result"
LOG_FILE = os.path.join(RESULT_DIR, "khiops_training_log.txt")
TASK_FILE = os.path.join(RESULT_DIR, "khiops_task_file.khtk")

# Khiops training parameters
DIC_NAME = "Bivariate"

# Visualization parameters
PLOT_WIDTH = 600
PLOT_HEIGHT = 500


# ============================================================================
# Functions
# ============================================================================


def generate_dictionary_file() -> None:
    """
    Generate the dictionary file used throughout the pipeline.

    :param dictionary_file:
    :return:
    """
    if not os.path.exists(INPUT_DATA_DIR):
        os.makedirs(INPUT_DATA_DIR)
    dictionary_file_name = os.path.join(INPUT_DATA_DIR, DIC_NAME + ".kdic")
    with open(dictionary_file_name, "w") as f:
        f.write("Dictionary " + DIC_NAME + "(index)\n")
        f.write("{\n")
        f.write("	Categorical	index		;	\n")
        f.write("	Numerical	a		;	\n")
        f.write("	Numerical	b		;	\n")
        f.write("};\n")



def generate_synthetic_data(output_file: str, pattern_centers: list, use_value_ranks: bool = False) -> pd.DataFrame:
    """
    Generate synthetic blob data and save to CSV.

    Parameters
    ----------
    output_file : str
        Path where the CSV file will be saved.
    pattern_centers : list
        List of center points to use in the synthetic data.

    Returns
    -------
    pd.DataFrame
        Generated data with columns 'index', 'a', 'b'.
    """
    # Generate blob data
    X, _ = datasets.make_blobs(n_samples=N_SAMPLES, random_state=RANDOM_SEED,
                               centers=pattern_centers)

    # Create DataFrame
    data = X
    df = pd.DataFrame(
        {
            "index": range(len(data)),
            "a": data[:, 0],
            "b": data[:, 1],
        }
    )
    # Replace 'a' and 'b' with their ranks
    if use_value_ranks:
        df['a'] = df['a'].rank(method='average')
        df['b'] = df['b'].rank(method='average')

    # Format index as categorical variable with prefix
    df["index"] = df["index"].astype(str)
    df["index"] = df["index"].apply(lambda x: f"pid_{x}")
    df = df.sort_values(by="index")

    # Save to CSV
    df.to_csv(output_file, index=False)
    return df


def train_unsupervised_model(
    dictionary_file: str,
    data_file: str,
    output_file: str,
) -> None:
    """
    Train a Khiops unsupervized model.

    Parameters
    ----------
    dictionary_file : str
        Path to the Khiops dictionary file.
    data_file : str
        Path to the input data CSV file.
    output_file : str
        Path where the trained model will be saved.
    """
    kh.train_predictor(
        dictionary_file,
        DIC_NAME,
        data_file,
        "",
        output_file,
        field_separator=',',
        log_file_path=LOG_FILE,
        task_file_path=TASK_FILE,
    )

def train_coclustering_v_v_model(
    dictionary_file: str,
    data_file: str,
    output_file: str,
) -> None:
    """
    Train a Khiops coclustering model.

    Parameters
    ----------
    dictionary_file : str
        Path to the Khiops dictionary file.
    data_file : str
        Path to the input data CSV file.
    output_file : str
        Path where the trained model will be saved.
    """
    kh.train_coclustering(
        dictionary_file,
        DIC_NAME,
        data_file,
        ["a", "b"],
        output_file,
        field_separator=',',
        log_file_path=LOG_FILE,
        task_file_path=TASK_FILE,
    )


def train_coclustering_i_v_model(
    dictionary_file: str,
    data_file: str,
    output_file: str,
) -> None:
    """
    Train a Khiops coclustering model.

    Parameters
    ----------
    dictionary_file : str
        Path to the Khiops dictionary file.
    data_file : str
        Path to the input data CSV file.
    output_file : str
        Path where the trained model will be saved.
    """
    kh.train_instance_variable_coclustering(
        dictionary_file,
        DIC_NAME,
        data_file,
        output_file,
        field_separator=',',
        log_file_path=LOG_FILE,
        task_file_path=TASK_FILE,
    )


def extract_clusters(model_file: str, output_file: str) -> None:
    """
    Extract clusters from a trained Khiops model.

    Parameters
    ----------
    model_file : str
        Path to the trained Khiops model file.
    output_file : str
        Path where the clusters will be saved.
    """
    kh.extract_clusters(
        model_file,
        cluster_variable="index",
        clusters_file_path=output_file,
    )

def extract_boundaries(model_file: str, variable_name: str, is_i_v_coclustering: bool) -> list:
    """
    Extract boundaries from a trained coclustering model for a specific variable.

    Parameters
    ----------
    model_file : str
        Path to the trained Khiops model file.
    variable_name : str
        Name of the variable for which to extract boundaries.
    is_i_v_coclustering : bool
        Whether the variable is part of a var part dimension in Instances x Variables coclustering
    """
    boundaries = []

    # Read coclustering results from the file
    try:
        # Read coclustering results from the file
        coclustering_results = (
            kh.coclustering_results.read_coclustering_results_file(model_file)
        )
        coclustering_report = coclustering_results.coclustering_report
    
    except (OSError, ValueError) as exc:
        print(f"Could not read coclustering results from {model_file!r}: {exc}")
        return boundaries

    # Case of Instances x Variables coclustering
    if is_i_v_coclustering:
        variables_dimension = coclustering_report.get_dimension("Variables")

        # Retrieve the sub-dimensions of variables
        inner_variables = variables_dimension.inner_variable_dimensions 

        # Loop through sub-dimensions to find the one matching the target variable
        for variable in inner_variables:
            if variable.name == variable_name and variable.type == "Numerical":
                for i, part in enumerate(variable.parts):
                    # Append the lower bound of the first part
                    if i == 0:
                        boundaries.append(part.lower_bound)
                    # Append the upper bound of the part
                    boundaries.append(part.upper_bound)
    # Case of Variable x Variable coclustering
    else:
        variable = coclustering_report.get_dimension(variable_name)
        for i, part in enumerate(variable.parts):
            # Append the lower bound of the first part
            if i == 0:
                boundaries.append(part.lower_bound)
            # Append the upper bound of the part
            boundaries.append(part.upper_bound)
    return boundaries


def load_data(data_file: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Parameters
    ----------
    data_file : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    return pd.read_csv(data_file)


def visualize_data(data: pd.DataFrame, data_visu_file: str, title: str, display: bool = False) -> None:
    """
    Create and display a scatter plot of data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with 'a', 'b' features
    data_visu_file : str
        Path to the file where the figure will be saved.
    display : bool, optional
        Whether to display the figure or not.
    """
    # Create the scatter plot
    fig = px.scatter(
        data,
        x="a",
        y="b",
        title=title,
        labels={"a": "Feature a", "b": "Feature b"},
    )

    # Update layout
    fig.update_layout(
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    # Show and save the figure
    if display:
        fig.show()
    fig.write_image(data_visu_file)


def load_clusters(clusters_file: str) -> pd.DataFrame:
    """
    Load cluster assignments from a tab-separated file.

    Parameters
    ----------
    clusters_file : str
        Path to the clusters file.

    Returns
    -------
    pd.DataFrame
        Cluster assignments with 'Value' and 'Cluster' columns.
    """
    return pd.read_csv(clusters_file, sep="\t")


def merge_data_with_clusters(clusters: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    """
    Merge cluster assignments with the original data.

    Parameters
    ----------
    clusters : pd.DataFrame
        DataFrame with 'Value' and 'Cluster' columns.
    data : pd.DataFrame
        DataFrame with 'index' column and features.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with all original features and cluster assignments.
    """
    merged = pd.merge(clusters, data, left_on="Value", right_on="index")
    return merged


def visualize_density(data: pd.DataFrame, density_visu_file: str, title: str, x_lines: list = None, y_lines: list = None, display: bool = False) -> None:
    """
    Create and display a scatter plot of density with optional vertical and horizontal lines.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with 'a', 'b' features and 'Cluster' column.
    density_visu_file : str
        Path to the file where the figure will be saved.
    x_lines : list, optional
        List of x-values where vertical lines should be drawn (default is None).
    y_lines : list, optional
        List of y-values where horizontal lines should be drawn (default is None).
    display : bool, optional
        Whether to display the figure or not.
    """
    # Create the scatter plot
    fig = px.scatter(
        data,
        x="a",
        y="b",
        title="VV Coclustering, " + title,
        labels={"a": "Feature a", "b": "Feature b"},
    )

    # Add vertical lines if x_lines is provided
    if x_lines:
        for x in x_lines:
            fig.add_shape(
                type="line",
                x0=x,
                y0=data["b"].min(),
                x1=x,
                y1=data["b"].max(),
                line=dict(color="black", width=1, dash="dash"),
            )

    # Add horizontal lines if y_lines is provided
    if y_lines:
        for y in y_lines:
            fig.add_shape(
                type="line",
                x0=data["a"].min(),
                y0=y,
                x1=data["a"].max(),
                y1=y,
                line=dict(color="black", width=1, dash="dash"),
            )

    # Update layout
    fig.update_layout(
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    # Show and save the figure
    if display:
        fig.show()
    fig.write_image(density_visu_file)


def visualize_clusters(data: pd.DataFrame, clusters_visu_file: str, title: str, x_lines: list = None, y_lines: list = None, display: bool = False) -> None:
    """
    Create and display a scatter plot of clusters with optional vertical and horizontal lines.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with 'a', 'b' features and 'Cluster' column.
    clusters_visu_file : str
        Path to the file where the figure will be saved.
    title : str
        Title of the plot.
    x_lines : list, optional
        List of x-values where vertical lines should be drawn (default is None).
    y_lines : list, optional
        List of y-values where horizontal lines should be drawn (default is None).
    display : bool, optional
        Whether to display the figure or not.
    """
    # Create the scatter plot
    fig = px.scatter(
        data,
        x="a",
        y="b",
        color="Cluster",
        title="IV Coclustering, " + title,
        labels={"a": "Feature a", "b": "Feature b"},
    )

    # Add vertical lines if x_lines is provided
    if x_lines:
        for x in x_lines:
            fig.add_shape(
                type="line",
                x0=x,
                y0=data["b"].min(),
                x1=x,
                y1=data["b"].max(),
                line=dict(color="black", width=1, dash="dash"),
            )

    # Add horizontal lines if y_lines is provided
    if y_lines:
        for y in y_lines:
            fig.add_shape(
                type="line",
                x0=data["a"].min(),
                y0=y,
                x1=data["a"].max(),
                y1=y,
                line=dict(color="black", width=1, dash="dash"),
            )

    # Update layout
    fig.update_layout(
        legend_title_text="Cluster",
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    # Show and save the figure
    if display:
        fig.show()
    fig.write_image(clusters_visu_file)

def study_pattern(name: str, pattern_centers: list, use_value_ranks : bool = False):
    """
    Study a pattern by generating synthetic data, training Khiops coclustering models,
    and visualizing the results.

    Parameters
    ----------
    name : str
        Name of the pattern to study.
    pattern_centers : list
        List of centers of bivariate blobs, with 'a' and 'b' features.
        Example: [[0, 0], [10, 10]]
    use_value_ranks : bool, optional
        Whether to use value-ranking or not.

    The study includes:
    - Generating synthetic data
    - Training a Khiops coclustering variable x variable model
    - Training a Khiops coclustering instances x variables model
      - Extracting clusters and boundaries per partitioned feature
      - Merging results with original data
      - Visualizing the clusters
    """

    def log_message(message):
        """
        Print message to stdout and write to log file.
        """
        print(message)
        if log_file:
            log_file.write(message + '\n')

    # File paths
    suffix = ""
    title_suffix = ""
    if use_value_ranks:
        suffix = ".ranks"
        title_suffix = " ( ranks)"
    results_dir =  os.path.join(RESULT_DIR, name + suffix)
    dic_file_name = os.path.join(INPUT_DATA_DIR, DIC_NAME + ".kdic")
    input_data_file = os.path.join(INPUT_DATA_DIR, name + suffix + ".csv")
    data_visu_file = os.path.join(results_dir, name + "Data.png")
    unsupervised_file = os.path.join(results_dir, name + "Unsupervised.khj")
    coclustering_v_v_file = os.path.join(results_dir, name + "CoclusteringVxV.khcj")
    coclustering_v_v_density_file = os.path.join(results_dir, name + "DensityVxV.png")
    coclustering_i_v_file = os.path.join(results_dir, name + "CoclusteringIxV.khcj")
    coclustering_i_v_cluster_file = os.path.join(results_dir, name + "ClustersIxV.csv")
    coclustering_i_v_visu_file = os.path.join(results_dir, name + "ClustersIxV.png")
    log_file_name = os.path.join(results_dir, name + ".log")

    # Open log file
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    log_file = open(log_file_name, "w")

    log_message("=" * 70)
    log_message("KHIOPS COCLUSTERING STUDY: " + name + title_suffix)
    log_message("=" * 70)

    # Generate dictionary file
    generate_dictionary_file()

    # Generate synthetic data
    log_message("\nGenerating synthetic data...")
    df_original = generate_synthetic_data(input_data_file, pattern_centers, use_value_ranks = use_value_ranks)
    log_message(f"Generated {len(df_original)} samples with features 'a' and 'b'.")

    # Visualize the data
    log_message("Visualizing data...")
    visualize_data(df_original, data_visu_file, name + title_suffix)

    # Train Khiops unsupervised model VxV model
    log_message("Training unsupervised model...")
    train_unsupervised_model(dic_file_name, input_data_file, unsupervised_file)

    # Train Khiops coclustering VxV model
    log_message("Training coclustering VxV model...")
    train_coclustering_v_v_model(dic_file_name, input_data_file, coclustering_v_v_file)

    # If coclustering results exist, process and visualize
    if not os.path.isfile(coclustering_v_v_file):
        log_message("WARNING: NO COCLUSTERING VxV FOUND")
    else:
        # Extract boundaries
        log_message("Extracting density boundaries...")
        a_boundaries = extract_boundaries(coclustering_v_v_file, "a", False)
        b_boundaries = extract_boundaries(coclustering_v_v_file, "b", False)

        # Visualize the results
        log_message("Visualizing results...")
        visualize_density(df_original, coclustering_v_v_density_file, name + title_suffix, x_lines=a_boundaries, y_lines=b_boundaries)


    # Train Khiops coclustering IxV model
    log_message("Training coclustering IxV model...")
    train_coclustering_i_v_model(dic_file_name, input_data_file, coclustering_i_v_file)

    # If coclustering results exist, process and visualize
    if not os.path.isfile(coclustering_i_v_file):
        log_message("WARNING: NO COCLUSTERING IxV FOUND")
    else:
        # Extract clusters and boundaries
        log_message("Extracting clusters and boundaries...")
        extract_clusters(coclustering_i_v_file, coclustering_i_v_cluster_file)
        a_boundaries = extract_boundaries(coclustering_i_v_file, "a", True)
        b_boundaries = extract_boundaries(coclustering_i_v_file, "b", True)

        # Load and merge data
        log_message("Loading and merging data...")
        clusters = load_clusters(coclustering_i_v_cluster_file)
        data = load_data(input_data_file)
        df_merged = merge_data_with_clusters(clusters, data)
        log_message(f"Merged data contains {len(df_merged)} samples.")
        log_message(f"Number of clusters: {df_merged['Cluster'].nunique()}\n")

        # Visualize the results
        log_message("Visualizing results...")
        visualize_clusters(df_merged, coclustering_i_v_visu_file, name + title_suffix, x_lines=a_boundaries, y_lines=b_boundaries)

    log_message("\n" + "=" * 70)
    log_message("PROCESS COMPLETED SUCCESSFULLY")
    log_message("=" * 70)

    # Close log file
    log_file.close()


def coclustering_study():
    """
    Run coclustering studies on different patterns with and without value ranks.
    """
    # Build a checkers pattern, with a noisy version
    checkers_pattern = []
    noisy_checkers_pattern = []
    for i in range(10):
        for j in range(10):
            if (i+j) % 2 == 0:
                checkers_pattern.append([10*i, 10*j])
                noisy_checkers_pattern.append([3*i, 3*j])

    # Study all patterns, using the values or their rank
    for use_value_ranks in [True, False]:
        study_pattern("Circle", [[0, 0]], use_value_ranks = use_value_ranks)
        study_pattern("TriangleU", [[10, 10], [-10, 10], [0, 0]], use_value_ranks = use_value_ranks)
        study_pattern("TriangleL", [[10, 0], [0, 10], [0, 0]], use_value_ranks = use_value_ranks)
        study_pattern("Diagonal", [[-10, -10], [0, 0], [10, 10]], use_value_ranks = use_value_ranks)
        study_pattern("NoisyDiagonal", [[-3, -3], [0, 0], [3, 3]], use_value_ranks=use_value_ranks)
        study_pattern("BlurredDiagonal", [[-2, -2], [0, 0], [2, 2]], use_value_ranks=use_value_ranks)
        study_pattern("Square", [[10, 10], [-10, -10], [10, -10], [-10, 10]], use_value_ranks = use_value_ranks)
        study_pattern("Checkers", checkers_pattern, use_value_ranks = use_value_ranks)
        study_pattern("NoisyCheckers", noisy_checkers_pattern, use_value_ranks = use_value_ranks)


def main():
    coclustering_study()

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        main()
