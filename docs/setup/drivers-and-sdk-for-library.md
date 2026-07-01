# Cloud Storage Drivers for Khiops Python

The Khiops Python library can read and write remote files from the following storage services after a few prerequisites are installed: **AWS S3, Google Cloud Storage (GCS), and Microsoft Azure**.

=== "Pip packages"

    All prerequisites can be installed in one step during the [**Pip installation**](pip.md) of the Khiops Python library.
    
    ```commandline
        # In a dedicated virtual environment (recommended)
        pip install khiops[s3] # for a specific storage service only
        pip install khiops[s3,gcs,azure] # for all supported storage services
    ```

=== "Conda packages"

    To use remote resources with the Khiops Python library under Conda, install the vendor-specific Python SDKs and the corresponding Khiops drivers.

    For AWS S3
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)
    
    conda install -y -n conda_env \
        "boto3>=1.17.39,<=1.35.69" "khiops-driver-s3"
    ```

    For GCS
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)

    conda install -y -n conda_env \
        "google-cloud-storage>=1.37.0" "khiops-driver-gcs"
    ```

    For Azure
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)

    conda install -y -n conda_env \
        "azure-core>=1.39.0,<2.0.0" \
        "azure-storage-blob>=12.28.0,<13.0.0" \
        "azure-storage-file-share>=12.24.0,<13.0.0" \
        "khiops-driver-azure"
    ```