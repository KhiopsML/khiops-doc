# Khiops application

If you intend to use remote resources with the Khiops desktop application, you will have to install additionally the Khiops drivers.

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