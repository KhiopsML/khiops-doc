# Installation Options

Khiops was originally launched as a desktop application. As we move to open source, we are diversifying the installation options to meet different needs:

  - **Python Library**:
    - Packaging via [`conda`][conda]
    - Packaging via [`pip`][pip]
    - Running our [khiops-notebook][notebooks] container
  - **Desktop Version**: Maintaining its original form for easy GUI access.

  [conda]: #with-conda
  [pip]: #with-pip
  [notebooks]: #with-jupyter
  [nocode]: nocode.md

We fully support the following operating systems:

- Ubuntu 18.04 or later (x86-64) 
- CentOS 7 and 8 (x86-64)
- Windows 7 or later (x86-64)
- macOS 10 or later,  for Intel (`conda` + `docker`) and :material-apple: Apple Silicon (`conda` **exclusively**)

<br>

## Install Khiops using conda <small>  🚧 Beta 🚧 </small> {#with-conda data-toc-label="Install Khiops via conda"}

The `conda` contains all the necessary components. 

=== "All x86-64 OS"
    ``` sh
    conda install -c khiops khiops
    ```

=== ":material-apple: Apple Silicon (ARM64)"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```

[:material-cursor-default-click-outline: See the Conda Installation Page](/setup/conda/){ .md-button .md-button--primary }

<br>

## Install Khiops using pip {#with-pip data-toc-label="Install Khiops via pip"}

Installing Khiops using pip requires installing the `khiops-core` binary first.

=== "Ubuntu"
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB="$(mktemp)" && \
    wget -O "$TEMP_DEB" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+${CODENAME}_amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB && \
    pip install --no-cache-dir 'khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1'
    ```


=== "Windows"
    You need to download and install the Khiops Application first:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

    Then, you can run the following `pip` command:
    ```sh
    pip install 'khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1'
    ```

=== "CentOS"
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" -y && \
    rm -f $TEMP_RPM && \
    pip install --no-cache-dir 'khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1'
    ```

[:material-cursor-default-click-outline: See the Pip Installation Page](/setup/pip/){ .md-button .md-button--primary }

<br>

## Run Khiops with Jupyter Docker Stacks <small>  🚧 Beta 🚧 </small> { #with-jupyter  data-toc-label="Using Khiops on Jupyter notebooks"}

For a quick and easy way to get started with Khiops, you can use our container. 

```bash
docker pull khiopsml/khiops-notebook
```

[:material-cursor-default-click-outline: See the Docker notebooks Installation Page](/setup/khiops-notebook/){ .md-button .md-button--primary }

<br>
  
## Install Khiops Desktop

This version contains a Graphical User Interface (GUI). 


=== "Windows"
    You need to download and install the Khiops Application first:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>
    
=== "Ubuntu"
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+${CODENAME}_amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops_10.1.1-0+${CODENAME}_amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```


=== "CentOS"
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" "$TEMP_DEB_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_DEB_KHIOPS    ```
    ```
    
[:material-cursor-default-click-outline: See the Khiops Desktop Installation Page](/setup/nocode/){ .md-button .md-button--primary }