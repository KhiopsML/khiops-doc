# Installation of remote files drivers and vendors SDK

Khiops can read and write remote files for the following storage types : **AWS S3, Google Cloud Storage (GCS) and Azure**, right after the installation of a few prerequisites.

## Khiops drivers

=== "Pip packages"
  
    They can be installed on all platforms (supported Linux distributions, Mac OS and Windows).
    ```commandline
        # In a Python virtual environment
     
        pip install khiops-driver-s3 khiops-driver-gcs khiops-driver-azure
    ```

=== "Conda packages"

    They can be installed on platforms where Conda can be used
    ```commandline
        # In a Conda virtual environment ("conda_env" in the example)
    
        conda install -y -n conda_env \
        khiops-driver-s3=={{ KHIOPS_S3_DRIVER_VERSION }} \
        khiops-driver-gcs=={{ KHIOPS_GCS_DRIVER_VERSION }} \
        khiops-driver-azure=={{ KHIOPS_AZURE_DRIVER_VERSION }} 
    ```

=== "System packages"
  
    They can be installed on the supported Linux distributions only

    !!! info "Supported Linux distributions" 
        - Rocky Linux 9
        - Debian 11, 12 and 13
        - Ubuntu 20.04, 22.04 and 24.04 (LTS) on x86-64 architectures
        - Ubuntu 22.04 and 24.04 (LTS) on ARM architectures.

    *Ubuntu / Debian*
    ```commandline
        if [ -f /etc/os-release ]; then . /etc/os-release; fi && \
        wget -O khiops-gcs.deb https://github.com/KhiopsML/khiopsdriver-gcs/releases/download/{{ KHIOPS_GCS_DRIVER_VERSION }}/khiops-driver-gcs_{{ KHIOPS_GCS_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb && \
        wget -O khiops-s3.deb https://github.com/KhiopsML/khiopsdriver-s3/releases/download/{{ KHIOPS_S3_DRIVER_VERSION }}/khiops-driver-s3_{{ KHIOPS_S3_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb && \
        wget -O khiops-azure.deb https://github.com/KhiopsML/khiopsdriver-azure/releases/download/{{ KHIOPS_AZURE_DRIVER_VERSION }}/khiops-driver-azure_{{ KHIOPS_AZURE_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb && \
        (sudo dpkg -i --force-all khiops-gcs.deb khiops-s3.deb khiops-azure.deb || true) && \
        sudo apt-get -f -y install && \
        rm -f khiops-gcs.deb khiops-s3.deb khiops-azure.deb
    ```
    *Rocky Linux*
    ```commandline
          ROCKY_VERSION=$(rpm -E %{rhel}) && \  
          wget -O khiops-gcs.rpm "https://github.com/KhiopsML/khiopsdriver-gcs/releases/download/{{ KHIOPS_GCS_DRIVER_VERSION }}/khiops-driver-gcs_{{ KHIOPS_GCS_DRIVER_VERSION }}-1.el${ROCKY_VERSION}.x86_64.rpm" && \
          wget -O khiops-s3.rpm "https://github.com/KhiopsML/khiopsdriver-s3/releases/download/{{ KHIOPS_S3_DRIVER_VERSION }}/khiops-driver-s3_{{ KHIOPS_S3_DRIVER_VERSION }}-1.el${ROCKY_VERSION}.x86_64.rpm" && \
          wget -O khiops-azure.rpm "https://github.com/KhiopsML/khiopsdriver-azure/releases/download/{{ KHIOPS_AZURE_DRIVER_VERSION }}/khiops-driver-azure_{{ KHIOPS_AZURE_DRIVER_VERSION }}-1.el${ROCKY_VERSION}.x86_64.rpm" && \
          sudo yum install  -y && \
          rm -f khiops-gcs.rpm khiops-s3.rpm khiops-azure.rpm
    ```

## The Khiops Python library additional dependencies

If you intend to use remote resources while working with the Khiops Library you will have to install additional dependencies:

    - the aformentioned Khiops drivers
    - a vendor-specific Python SDK

=== "Pip packages"

    This can be done in one step during the [**pip installation**](../pip) of the Khiops Python library.
    
    ```commandline
      pip install khiops[s3] # for a specific storage type only
      pip install khiops[s3,gcs,azure] # for all the supported storage types
    ```

=== "Conda packages"
 
    For s3
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)
    
    conda install -y -n conda_env \
        "boto3>=1.17.39,<=1.35.69" "khiops-driver-s3"
    ```

    For gcs
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)

    conda install -y -n conda_env \
        "google-cloud-storage>=1.37.0" "khiops-driver-gcs"
    ```

    For azure
    ```commandline
    # In a Conda virtual environment ("conda_env" in the example)

    conda install -y -n conda_env \
        "azure-core>=1.39.0,<2.0.0" \
        "azure-storage-blob>=12.28.0,<13.0.0" \
        "azure-storage-file-share>=12.24.0,<13.0.0" \
        "khiops-driver-azure"
    ```