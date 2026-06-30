# Cloud-ready Khiops Python library

The Khiops library can read and write remote files for the following storage types : **AWS S3, Google Cloud Storage (GCS) and Azure**, after the installation of a few prerequisites.

=== "Pip packages"

    The installation of all the prerequisites can be done in one step during the [**Pip installation**](../pip) of the Khiops Python library.
    
    ```commandline
      # In a dedicated virtual environment (recommended)
      pip install khiops[s3] # for a specific storage type only
      pip install khiops[s3,gcs,azure] # for all the supported storage types
    ```

=== "Conda packages"

    If you intend to use remote resources while working with the Khiops Library under Conda, you will have to install the vendor-specific Python SDK(s) and the Khiops driver(s). 

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