# Copyright (c) 2023-2026 Orange. All rights reserved.
# This software is distributed under the BSD 3-Clause-clear License, the text of which is available
# at https://spdx.org/licenses/BSD-3-Clause-Clear.html or see the "LICENSE" file for more details.

"""
Iris Clustering Study

This script performs clustering analysis on the Iris dataset using Khiops. It trains unsupervised models,
variable-variable coclustering, and instance-variable coclustering models. The script visualizes the clustering
results, extracts boundaries and clusters, and saves the visualizations and statistics for further analysis.
"""

import warnings
import os
import pandas as pd
import plotly.express as px
from khiops import core as kh
from khiops.tools import download_datasets
import plotly.graph_objects as go


# ============================================================================
# Configuration
# ============================================================================

# File paths (relative to script location)
RESULT_DIR = "result"
LOG_FILE = os.path.join(RESULT_DIR, "khiops_training_log.txt")
TASK_FILE = os.path.join(RESULT_DIR, "khiops_task_file.khtk")

# Khiops training parameters
DIC_NAME = "Iris"
VARIABLE_NAMES = ["Class", "PetalLength", "PetalWidth", "SepalLength", "SepalWidth"]
CLASS_NAME = "Class"

# Visualization parameters
PLOT_WIDTH = 600
PLOT_HEIGHT = 500


# ============================================================================
# Functions
# ============================================================================

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
        field_separator='\t',
        log_file_path=LOG_FILE,
        task_file_path=TASK_FILE,
    )

def train_coclustering_v_v_model(
    dictionary_file: str,
    variable_names: list,
    data_file: str,
    output_file: str,
) -> None:
    """
    Train a Khiops coclustering model.

    Parameters
    ----------
    dictionary_file : str
        Path to the Khiops dictionary file.
    variable_names: list
        List of variable names.
    data_file : str
        Path to the input data CSV file.
    output_file : str
        Path where the trained model will be saved.
    """
    kh.train_coclustering(
        dictionary_file,
        DIC_NAME,
        data_file,
        variable_names,
        output_file,
        field_separator='\t',
        log_file_path=LOG_FILE,
        task_file_path=TASK_FILE,
    )


def train_coclustering_i_v_model(
    dictionary_file: str,
    variable_names: list,
    data_file: str,
    output_file: str,
) -> None:
    """
    Train a Khiops coclustering model.

    Parameters
    ----------
    dictionary_file : str
        Path to the Khiops dictionary file.0
    variable_names: list
        List of variable names.
    data_file : str
        Path to the input data CSV file.
    output_file : str
        Path where the trained model will be saved.
    """
    # Select the variables to use the the analysis
    dictionary_domain = kh.read_dictionary_file(dictionary_file)
    dictionary = dictionary_domain.get_dictionary(DIC_NAME)
    dictionary.use_all_variables(False)
    for name in variable_names:
        dictionary.get_variable(name).used = True

    # Train the coclustering model
    kh.train_instance_variable_coclustering(
        dictionary_domain,
        DIC_NAME,
        data_file,
        output_file,
        field_separator='\t',
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
        cluster_variable="Instance index",
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
    coclustering_results = kh.coclustering_results.read_coclustering_results_file(model_file)
    coclustering_report = coclustering_results.coclustering_report

    # Case of Instances x Variables coclustering
    if is_i_v_coclustering:
        variables_dimension = coclustering_report.get_dimension("Variables")

        # Retrieve the sub-dimensions of variables
        inner_variables = variables_dimension.variable_part_dimensions

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


def visualize_data(data: pd.DataFrame, data_visu_file: str, x_variable_name: str, y_variable_name: str, title: str, display: bool = False) -> None:
    """
    Create and display a scatter plot of data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame
    x_variable_name: str
        Name of the x variable.
    y_variable_name: str
        Name of the y variable.
    data_visu_file : str
        Path to the file where the figure will be saved.
    display : bool, optional
        Whether to display the figure or not.
    """
    # Create the scatter plot
    fig = px.scatter(
        data,
        x=x_variable_name,
        y=y_variable_name,
        title=title,
        labels={x_variable_name: x_variable_name, y_variable_name: y_variable_name},
    )

    # Update layout
    fig.update_layout(
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    # Show and save the figure (engine=None only to remove a deprecation warning)
    if display:
        fig.show()
    fig.write_image(data_visu_file, engine=None)


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

    # Filter out rows where Value is ' * ', which correspond to the default cluster
    clusters_filtered = clusters[clusters['Value'] != ' * '].copy()

    # Convert 'Value' column to int
    clusters_filtered['Value'] = clusters_filtered['Value'].astype(int)

    # Sort by 'Value'
    clusters_ordered = clusters_filtered.sort_values(by='Value').reset_index(drop=True)

    # Keep data in its original order (no change needed)
    data_ordered = data.copy().reset_index(drop=True)

    # Concatenate along columns (axis=1)
    merged = pd.concat([data_ordered, clusters_ordered], axis=1)
    return merged


def visualize_density(data: pd.DataFrame, density_visu_file: str,
                      x_variable_name, y_variable_name, title: str,
                      x_lines: list = None, y_lines: list = None, display: bool = False) -> None:
    """
    Create and display a scatter plot of density with optional vertical and horizontal lines.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame
    density_visu_file : str
        Path to the file where the figure will be saved.
    x_variable_name: str
        Name of the x variable.
    y_variable_name: str
        Name of the y variable.
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
        x=x_variable_name,
        y=y_variable_name,
        title="VxV Coclustering, " + title,
        labels={x_variable_name: x_variable_name, y_variable_name: y_variable_name},
    )

    # Add vertical lines if x_lines is provided
    if x_lines:
        for x in x_lines:
            fig.add_shape(
                type="line",
                x0=x,
                y0=data[y_variable_name].min(),
                x1=x,
                y1=data[y_variable_name].max(),
                line=dict(color="black", width=1, dash="dash"),
            )

    # Add horizontal lines if y_lines is provided
    if y_lines:
        for y in y_lines:
            fig.add_shape(
                type="line",
                x0=data[x_variable_name].min(),
                y0=y,
                x1=data[x_variable_name].max(),
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
    fig.write_image(density_visu_file, engine=None)


def visualize_clusters(data: pd.DataFrame, clusters_visu_file: str,
                       x_variable_name: str, y_variable_name: str, class_name: str,
                       title: str, x_lines: list = None, y_lines: list = None, display: bool = False) -> None:
    """
    Create and display a scatter plot of clusters with optional vertical and horizontal lines.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with 'a', 'b' features and 'Cluster' column.
    clusters_visu_file : str
        Path to the file where the figure will be saved.
    x_variable_name: str
        Name of the x variable.
    y_variable_name: str
        Name of the y variable.
    class_name : str
        Name of the class.
    title : str
        Title of the plot.
    x_lines : list, optional
        List of x-values where vertical lines should be drawn (default is None).
    y_lines : list, optional
        List of y-values where horizontal lines should be drawn (default is None).
    display : bool, optional
        Whether to display the figure or not.
    """

    # Define marker symbols
    symbols = ['triangle-up', 'star', 'triangle-down', 'square', 'circle', 'diamond', 'cross', 'x']

    # Create the scatter plot
    fig = px.scatter(
        data,
        x=x_variable_name,
        y=y_variable_name,
        color="Cluster",
        symbol=class_name,
        symbol_sequence=symbols,
        title="IxV Coclustering, " + title,
        labels={x_variable_name: x_variable_name, y_variable_name: y_variable_name}
    )

    # Increase symbol size for main scatter plot
    fig.update_traces(marker=dict(size=9))

    # Disable legend for all original data traces
    for trace in fig.data:
        trace.showlegend = False

    # Get unique categories
    unique_clusters = data['Cluster'].unique()
    unique_classes = data[class_name].unique()

    # Create symbol map dynamically
    symbol_map = {class_val: symbols[i % len(symbols)] for i, class_val in enumerate(unique_classes)}

    # Add legend for clusters (by color)
    for i, cluster in enumerate(unique_clusters):
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]),
            name=f'Cluster: {cluster}',
            showlegend=True
        ))

    # Add legend for classes (by shape, in black)
    for class_val, symbol in symbol_map.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, symbol=symbol, color='black'),
            name=f'Class: {class_val}',
            showlegend=True
        ))

    # Add vertical lines if x_lines is provided
    if x_lines:
        for x in x_lines:
            fig.add_shape(
                type="line",
                x0=x,
                y0=data[y_variable_name].min(),
                x1=x,
                y1=data[y_variable_name].max(),
                line=dict(color="black", width=1, dash="dash"),
            )

    # Add horizontal lines if y_lines is provided
    if y_lines:
        for y in y_lines:
            fig.add_shape(
                type="line",
                x0=data[x_variable_name].min(),
                y0=y,
                x1=data[x_variable_name].max(),
                y1=y,
                line=dict(color="black", width=1, dash="dash"),
            )

    # Update layout
    fig.update_layout(
        legend_title_text="Clusters and Classes",
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    # Show and save the figure
    if display:
        fig.show()
    fig.write_image(clusters_visu_file, engine=None)


def iris_study():
    """
    Performs an Iris dataset analysis, including data visualization,
    coclustering, and statistical logging.
    """

    def log_message(message):
        """
        Prints a message to stdout and writes it to the log file.
        """
        print(message)
        if log_file:
            log_file.write(message + '\n')

    def log_bivariate_stats(coclustering_file, name1, name2, is_i_v_coclustering):
        """
        Logs statistics on bivariate coclustering results.
        """
        # Extract stats from the coclustering file if present
        if os.path.isfile(coclustering_file):
            # Extract number of intervals per variable
            x_boundaries = extract_boundaries(coclustering_file, name1, is_i_v_coclustering)
            y_boundaries = extract_boundaries(coclustering_file, name2, is_i_v_coclustering)
            log_message("\t\t" + name1 + "\t" + str(len(x_boundaries)-1))
            log_message("\t\t" + name2 + "\t" + str(len(y_boundaries)-1))

            # Extract number of clusters in the case of IxV coclustering
            if is_i_v_coclustering:
                coclustering_cluster_file = coclustering_file.replace(".khcj", ".clusters.txt")
                extract_clusters(coclustering_file, coclustering_cluster_file)
                clusters = load_clusters(coclustering_cluster_file)
                log_message("\t\tClusters\t" + str(clusters['Cluster'].nunique()))
        # Default stats otherwise
        else:
            log_message("\t\t" + name1 + "\t1")
            log_message("\t\t" + name2 + "\t1")
            if is_i_v_coclustering:
                log_message("\t\tClusters\t1")

    # Define file paths
    results_dir =  os.path.join(RESULT_DIR)
    dic_file_name = os.path.join(kh.get_samples_dir(), DIC_NAME, DIC_NAME + ".kdic")
    input_data_file = os.path.join(kh.get_samples_dir(), DIC_NAME, DIC_NAME + ".txt")
    unsupervised_file = os.path.join(results_dir, DIC_NAME + "Unsupervised.khj")
    coclustering_v_v_file = os.path.join(results_dir, DIC_NAME + "CoclusteringVxV.khcj")
    coclustering_i_v_file = os.path.join(results_dir, DIC_NAME + "CoclusteringIxV.khcj")
    log_file_name = os.path.join(results_dir, DIC_NAME + ".log")

    # Download datasets if necessary, to get the Iris dataset,
    if not os.path.isfile(input_data_file):
        download_datasets()

    # Define and create necessary directories
    data_visu_dir = os.path.join(results_dir, "data")
    v_v_dir = os.path.join(results_dir, "VxV")
    i_v_dir = os.path.join(results_dir, "IxV")
    v_v_2_dir = os.path.join(results_dir, "VxV_Bivariate")
    i_v_2_dir = os.path.join(results_dir, "IxV_Bivariate")
    for dir in [data_visu_dir, v_v_dir, i_v_dir, v_v_2_dir, i_v_2_dir]:
        if not os.path.exists(dir):
            os.makedirs(dir)

    # Open log file
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    log_file = open(log_file_name, "w")

    log_message("=" * 70)
    log_message("COCLUSTERING STUDY: " + DIC_NAME)
    log_message("=" * 70)

    # Load data
    df_data = pd.read_csv(input_data_file, sep="\t")

    # Train Khiops unsupervised model VxV model
    log_message("Training unsupervised model...")
    train_unsupervised_model(dic_file_name, input_data_file, unsupervised_file)

    # Train Khiops coclustering VxV model
    log_message("Training coclustering VxV model...")
    train_coclustering_v_v_model(dic_file_name, VARIABLE_NAMES, input_data_file, coclustering_v_v_file)

    # Train Khiops coclustering IxV model
    log_message("Training coclustering IxV model...")
    train_coclustering_i_v_model(dic_file_name, VARIABLE_NAMES, input_data_file, coclustering_i_v_file)

    # Analyze each variable pair
    for i in range(len(VARIABLE_NAMES)):
        for j in range(i):
            name1 = VARIABLE_NAMES[i]
            name2 = VARIABLE_NAMES[j]
            if name1 == CLASS_NAME or name2 == CLASS_NAME:
                continue
            print(name1 + " " + name2)
            full_name = DIC_NAME + "_" + name1 + "_" + name2

            # Visualize the data
            log_message("\tVisualizing data results...")
            data_visu_file = os.path.join(data_visu_dir, full_name + "Data.png")
            visualize_data(df_data, data_visu_file, name1, name2, DIC_NAME)

            # Extract boundaries from global VxV coclustering
            log_message("\tExtracting VxV density boundaries...")
            x_boundaries = extract_boundaries(coclustering_v_v_file, name1, False)
            y_boundaries = extract_boundaries(coclustering_v_v_file, name2, False)
            log_bivariate_stats(coclustering_v_v_file, name1, name2, False)

            # Visualize the density results
            log_message("\tVisualizing results...")
            coclustering_v_v_density_file = os.path.join(v_v_dir, full_name + "DensityVxV.png")
            visualize_density(df_data, coclustering_v_v_density_file, name1, name2, DIC_NAME,
                              x_lines=x_boundaries, y_lines=y_boundaries)

            # Extract clusters and boundaries from the global IxV coclustering
            log_message("\tExtracting clusters and boundaries...")
            coclustering_i_v_cluster_file = os.path.join(i_v_dir, full_name + "ClustersIxV.txt")
            extract_clusters(coclustering_i_v_file, coclustering_i_v_cluster_file)
            x_boundaries = extract_boundaries(coclustering_i_v_file, name1, True)
            y_boundaries = extract_boundaries(coclustering_i_v_file, name2, True)
            log_bivariate_stats(coclustering_i_v_file, name1, name2, True)

            # Load and merge data
            log_message("Loading and merging data...")
            clusters = load_clusters(coclustering_i_v_cluster_file)
            data = pd.read_csv(input_data_file, sep = '\t')
            df_merged = merge_data_with_clusters(clusters, data)
            log_message(f"Merged data contains {len(df_merged)} samples.")
            log_message(f"Number of clusters: {df_merged['Cluster'].nunique()}\n")

            # Visualize the results
            log_message("Visualizing results...")
            coclustering_i_v_visu_file = os.path.join(i_v_dir, full_name + "ClustersIxV.png")
            visualize_clusters(df_merged, coclustering_i_v_visu_file,
                               name1, name2, CLASS_NAME, DIC_NAME, x_lines=x_boundaries, y_lines=y_boundaries)

            # Train a bivariate coclustering VxV model for stats only
            log_message("\tTraining bivariate coclustering VxV model...")
            coclustering2_v_v_file = os.path.join(v_v_2_dir, full_name + "CoclusteringVxV.khcj")
            train_coclustering_v_v_model(dic_file_name, [name1, name2], input_data_file, coclustering2_v_v_file)
            log_bivariate_stats(coclustering2_v_v_file, name1, name2, False)

            # Train a bivariate coclustering IxV model for stats only
            log_message("\tTraining bivariate coclustering IxV model...")
            coclustering2_i_v_file = os.path.join(i_v_2_dir, full_name + "CoclusteringIxV.khcj")
            train_coclustering_i_v_model(dic_file_name, [name1, name2], input_data_file, coclustering2_i_v_file)
            log_bivariate_stats(coclustering2_i_v_file, name1, name2, True)

    log_message("\n" + "=" * 70)
    log_message("PROCESS COMPLETED SUCCESSFULLY")
    log_message("=" * 70)

    # Close log file
    log_file.close()

def main():
    iris_study()

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        main()
