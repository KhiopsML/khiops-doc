# Cloud Storage

Khiops seamlessly integrates with cloud storage services, enabling **direct reading and writing** of datasets stored in 
**AWS S3 buckets, Google Cloud Storage (GCS) buckets and Azure storage (in files and blobs)**. 
By using Khiops dedicated cloud storage drivers, you can process large-scale datasets **without having to manually download or transfer files**, significantly improving efficiency and scalability in cloud-based workflows.

With these drivers, Khiops treats cloud storage **just like a local filesystem**, meaning that all Khiops commands and workflows remain unchanged—only the dataset paths need to be adjusted.

Refer to the [Cloud-ready Khiops Python library installation section](../setup/drivers-and-sdk-for-library.md) or [Cloud-ready Khiops application section](../setup/drivers-and-sdk-for-application.md) if needed. The current section documents the usage of the remote file storage facilities. 

## Using Khiops with Google Cloud Storage (GCS)

Khiops can read and write datasets stored in GCS buckets using the `khiopsdriver-gcs` package. Once configured, you can reference GCS paths directly in Khiops commands, scenarios and the GUI (where applicable) using the format `gs://<bucket-name>/path/to/file.csv`.

To verify that Khiops can use the remote-storage driver, run:

```sh
khiops -s
```

You should see an output indicating that the GCS driver is loaded and ready to use for data files following the `gs` URI scheme, as follows:


```sh
Khiops {{ KHIOPS_VERSION }}

Drivers:  
	GCS driver ({{ KHIOPS_GCS_DRIVER_VERSION }}) for URI scheme 'gs'	    
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
report_path = "gs://mydatabucket/khiops_samples/Adult/AnalysisResults.khj"

# Train the predictor
_, model_path = kh.train_predictor(
    dictionary_file_path,
    "Adult",
    data_table_path,
    "class",
    report_path,
    max_trees=0,
)
```

## Using Khiops with AWS S3 Storage 

To start using Khiops with your data on S3, install the S3 driver package alongside Khiops.

To verify that Khiops can use the remote-storage driver, run:

```sh
khiops -s
```

You should see an output indicating that the S3 driver is loaded and ready to use for data files following the `s3` URI scheme, as follows:


```sh
Khiops {{ KHIOPS_VERSION }}

Drivers:
    S3 driver ({{ KHIOPS_S3_DRIVER_VERSION }}) for URI scheme 's3'
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
report_path = "s3://mydatabucket/khiops_samples/Adult/AnalysisResults.khj"

# Train the predictor
_, model_path = kh.train_predictor(
    dictionary_file_path,
    "Adult",
    data_table_path,
    "class",
    report_path,
    max_trees=0,
)
```

## Using Khiops with Azure Storage

To start using Khiops with your data on Azure, install the Azure driver package alongside Khiops.

To verify that Khiops can use the remote-storage driver, run:

```sh
khiops -s
```

You should see an output indicating that the Azure driver is loaded and ready to use for data files following the `https` URI scheme as used by Azure, as follows:


```sh
Khiops {{ KHIOPS_VERSION }}

Drivers:
    Azure driver ({{ KHIOPS_AZURE_DRIVER_VERSION }}) for URI scheme 'https'
Environment variables:
    None
Internal environment variables:
    None
```

### Authentication

To access data stored in Azure storage Blob containers or File shares, you need valid authentication credentials. 
Khiops supports all the standard Azure authentication options. However, only the `AZURE_STORAGE_CONNECTION_STRING` environment variable is currently fully operational for every component, from the Khiops executables to the Khiops Python library.

`AZURE_STORAGE_CONNECTION_STRING` contains a list of parameters like the `AccountName`, `AccountKey` and other technical parameters.

**You must always copy / paste its value from the "Azure portal" in the "Security + networking > Access keys" of a "Storage account"** instead of trying to craft a connection string by yourself.
```sh
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;End" 
```

### Using Azure URIs in Khiops

Please remember that the Azure paths supported by Khiops can either be, 

- file-oriented : `https://<storage account name>.file.core.windows.net/<share name>/path/to/file.csv` 
- or blob-oriented : `https://<storage account name>.blob.core.windows.net/<container name>/path/to/file.csv`

They can be used in the desktop application (GUI), Python scripts, or within Khiops scenarios. For example:

**Low-Level Khiops Usage:**
```sh
khiops -b -i https://khiopsaccount1.file.core.windows.net/my_share/khiops_samples/scenario.kh
```

**Python Sample:**

```python
# Imports
import os
from khiops import core as kh

# Set the file URIs
dictionary_file_path = "https://khiopsaccount1.file.core.windows.net/my_share/khiops_samples/Adult/Adult.kdic"
data_table_path = "https://khiopsaccount1.file.core.windows.net/my_share/khiops_samples/Adult/Adult.kdic"
report_path = "https://khiopsaccount1.file.core.windows.net/my_share/khiops_samples/Adult/AnalysisResults.khj"

# Train the predictor
_, model_path = kh.train_predictor(
    dictionary_file_path,
    "Adult",
    data_table_path,
    "class",
    report_path,
    max_trees=0,
)
```