# Cloud Storages

Khiops seamlessly integrates with cloud storage services, enabling **direct reading and writing of datasets stored in AWS S3 and Google Cloud Storage (GCS)** buckets. By using Khiops dedicated cloud storage drivers, you can process large-scale datasets **without having to manually download or transfer files**, significantly improving efficiency and scalability in cloud-based workflows.

With these drivers, Khiops treats cloud storage **just like a local filesystem**, meaning that all Khiops commands and workflows remain unchanged—only the dataset paths need to be adjusted.

!!! info "Driver Installation Support"
    On **Windows** and *macOS*, Khiops drivers are only supported through Conda. If you are using another installation method on these operating systems, consider switching to a Conda environment to enable driver support.
    On **Linux**, Khiops drivers are supported through both Conda (Python only) and by using the binary installation method (compatible with the [Khiops Application][nocode] and Python via pip). 

[nocode]: ../setup/nocode.md

## Using Khiops with Google Cloud Storage (GCS)

Khiops can read and write datasets stored in GCS buckets using the `khiopsdriver-gcs` driver. Once configured, you can reference GCS paths directly in Khiops commands, scenarios and the GUI (where applicable) using the format `gs://<bucket-name>/path/to/file.csv`.

### Installation

If you installed Khiops through Conda as recommended, you can install the driver as follows:

```sh
conda install -c khiops khiops-driver-gcs
```

??? warning "If you installed Khiops using `pip` **on Linux**... "
    === "Ubuntu / Debian"

        ```sh
        CODENAME=$(lsb_release -cs) && \
        TEMP_DEB="$(mktemp)" && \
        wget -O "$TEMP_DEB" "https://github.com/KhiopsML/khiopsdriver-gcs/releases/download/{{ KHIOPS_GCS_DRIVER_VERSION }}/khiops-driver-gcs_{{ KHIOPS_GCS_DRIVER_VERSION }}-1-${CODENAME}.amd64.deb" && \
        sudo dpkg -i "$TEMP_DEB && \
        rm -f $TEMP_DEB
        ```

    === "Rocky Linux"

        ```sh
        sudo yum update -y && sudo yum install wget -y && \
        ROCKY_VERSION=$(rpm -E %{rhel}) && \
        TEMP_RPM="$(mktemp).rpm" && \
        wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiopsdriver-gcs/releases/download/{{ KHIOPS_GCS_DRIVER_VERSION }}/khiops-driver-gcs_{{ KHIOPS_GCS_DRIVER_VERSION }}-1.el${ROCKY_VERSION}.x86_64.rpm" && \
        sudo yum install "$TEMP_RPM" -y && \
        rm -f $TEMP_RPM
        ```

To verify the installation, run:

```sh
khiops -s
```

You should see an output indicating that the GCS driver is loaded and ready to use for data files following the URI `gs` scheme, as follows:


```sh
Khiops {{ KHIOPS_VERSION }}

Drivers:
    'GCS driver' for URI scheme 'gs'
Environment variables:
    None
Internal environment variables:
    None
```

### Authentication

To access data stored in GCS buckets, you need valid authentication credentials. Khiops uses the standard [**Application Default Credentials**][cloud-auth] for authentication. Set up your local environment with these credentials using the `gcloud` CLI:

[cloud-auth]:https://cloud.google.com/docs/authentication/provide-credentials-adc?hl=fr

```sh
gcloud init
gcloud auth application-default login
```

With these credentials in place, Khiops can access your GCS data seamlessly.

### Using GCS URIs in Khiops

Once installed, Khiops can directly read and write GCS paths in the format `gs://<bucket-name>/path/to/file.csv` from the desktop application (GUI), Python scripts, or within Khiops scenarios. For example:

**Low-Level Khiops Usage:**
```sh
khiops -b -i gs://mydatabucket/khiops_samples/scenario.kh
```

**Python Sample:**

```python
# Imports
import os
from khiops import core as kh

# Set the file paths
dictionary_file_path = "gs://mydatabucket/khiops_samples/Adult/Adult.kdic"
data_table_path = "gs://mydatabucket/khiops_samples/Adult/Adult.kdic"
results_dir = "khiops_output"

# Train the predictor
kh.train_predictor(
    dictionary_file_path,
    "Adult",
    data_table_path,
    "class",
    results_dir,
    max_trees=0,
)
```

## Using Khiops with AWS S3 Storage 

To start using Khiops with your data on S3, install the S3 driver package alongside Khiops. If you installed Khiops through Conda as recommended, you can install the driver as follows:

```sh
conda install -c khiops khiops-driver-s3
```

??? warning "If you installed Khiops using `pip` **on Linux**..."
    === "Ubuntu / Debian"

        ```sh
        CODENAME=$(lsb_release -cs) && \
        TEMP_DEB="$(mktemp)" && \
        wget -O "$TEMP_DEB" "https://github.com/KhiopsML/khiopsdriver-s3/releases/download/{{ KHIOPS_S3_DRIVER_VERSION }}/khiops-driver-s3_{{ KHIOPS_S3_DRIVER_VERSION }}-1-${CODENAME}.amd64.deb" && \
        sudo dpkg -i "$TEMP_DEB && \
        rm -f $TEMP_DEB
        ```

    === "Rocky Linux"

        ```sh
        sudo yum update -y && sudo yum install wget -y && \
        ROCKY_VERSION=$(rpm -E %{rhel}) && \
        TEMP_RPM="$(mktemp).rpm" && \
        wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiopsdriver-s3/releases/download/{{ KHIOPS_S3_DRIVER_VERSION }}/khiops-driver-s3_{{ KHIOPS_S3_DRIVER_VERSION }}-1.el${ROCKY_VERSION}.x86_64.rpm" && \
        sudo yum install "$TEMP_RPM" -y && \
        rm -f $TEMP_RPM
        ```

To verify the installation, run:

```sh
khiops -s
```

You should see an output indicating that the GCS driver is loaded and ready to use for data files following the URI `s3` scheme, as follow:


```sh
Khiops {{ KHIOPS_VERSION }}

Drivers:
    'S3 driver' for URI scheme 's3'
Environment variables:
    None
Internal environment variables:
    None
```

### Authentication 

To access data stored in S3 buckets, you need valid authentication credentials. Khiops supports the same configuration options as the **AWS CLI**, accepting credentials and configuration options provided via [configuration files][cli-configure-files] or environment variables.

[cli-configure-files]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

**File-Based Configuration:**

Create a `config` file in the $HOME/.aws folder:

```unixconfig
[default]
region=us-east-1
endpoint_url = https://my-server.cloudprovider.com
```

Create a `credentials` file in the same folder:

```unixconfig
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Environment Variables:**

Alternatively, you can set the configuration options and credentials via environment variables:

```sh
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=https://my-server.cloudprovider.com
```

### Using S3 URIs in Khiops

Once installed, Khiops can directly read and write S3 paths in the format `s3://<bucket-name>/path/to/file.csv` from the desktop application (GUI), Python scripts, or within Khiops scenarios. For example:

**Low-Level Khiops Usage:**
```sh
khiops -b -i s3://mydatabucket/khiops_samples/scenario.kh
```

**Python Sample:**

```python
# Imports
import os
from khiops import core as kh

# Set the file URIs
dictionary_file_path = "s3://mydatabucket/khiops_samples/Adult/Adult.kdic"
data_table_path = "s3://mydatabucket/khiops_samples/Adult/Adult.kdic"
results_dir = "khiops_output"

# Train the predictor
kh.train_predictor(
    dictionary_file_path,
    "Adult",
    data_table_path,
    "class",
    results_dir,
    max_trees=0,
)
```
