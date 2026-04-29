# Installation of remote files drivers and vendors SDK

Khiops can read and write remote files for the following storage types : **AWS S3, Google Cloud Storage (GCS) and Azure**, right after the installation of a few prerequisites.

## Khiops drivers

- **Drivers under pip**:
  
  They can be installed on all platforms (supported Linux distributions, Mac OS and Windows).
  ```commandline
  # In a Python virtual environment
 
  pip install khiops-driver-s3 khiops-driver-gcs khiops-driver-azure
  ```

- **Drivers under Conda**:

  They can be installed on platforms where Conda can be used
  ```commandline
  # In a Conda virtual environment ("conda_env" in the example)

  conda install -y -n conda_env \
  khiops-driver-s3=={{ KHIOPS_S3_DRIVER_VERSION }} \
  khiops-driver-gcs=={{ KHIOPS_GCS_DRIVER_VERSION }} \
  khiops-driver-azure=={{ KHIOPS_AZURE_DRIVER_VERSION }} 
  ```

- **Drivers as system packages**:
  
  They can be installed on the supported Linux distributions only

!!! info "Supported Linux distributions" 
    - Rocky Linux 9
    - Debian 11, 12 and 13
    - Ubuntu 20.04, 22.04 and 24.04 (LTS) on x86-64 architectures
    - Ubuntu 22.04 and 24.04 (LTS) on ARM architectures.

  *Ubuntu / Debian*
  ```commandline
    if [ -f /etc/os-release ]; then . /etc/os-release; fi \
    && wget -O khiops-gcs.deb https://github.com/KhiopsML/khiopsdriver-gcs/releases/download/{{ KHIOPS_GCS_DRIVER_VERSION }}/khiops-driver-gcs_{{ KHIOPS_GCS_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb \
    && wget -O khiops-s3.deb https://github.com/KhiopsML/khiopsdriver-s3/releases/download/{{ KHIOPS_S3_DRIVER_VERSION }}/khiops-driver-s3_{{ KHIOPS_S3_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb \    
    && wget -O khiops-azure.deb https://github.com/KhiopsML/khiopsdriver-azure/releases/download/{{ KHIOPS_AZURE_DRIVER_VERSION }}/khiops-driver-azure_{{ KHIOPS_AZURE_DRIVER_VERSION }}-1-${VERSION_CODENAME}.amd64.deb \
    && (sudo dpkg -i --force-all khiops-gcs.deb khiops-s3.deb khiops-azure.deb || true) \
    && sudo apt-get -f -y install \
    && rm -f khiops-gcs.deb khiops-s3.deb khiops-azure.deb
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

## The Khiops Python library additional dependencies (vendors SDK for Python)

If you are using the Khiops Python library you will have to install a vendor-specific SDK.

This can be done during the [**installation**](../pip) of the Khiops Python library.

```commandline
  pip install khiops[s3] # for a specific storage type only
  pip install khiops[s3,gcs,azure] # for all the supported storage types
```

