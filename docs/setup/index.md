# Installation Options {label="Overview"}

Khiops was originally developed as a desktop application. As we move to open source, we are diversifying the installation options to meet different needs:

  - **Khiops Python Library**:
    - Packaged via [`conda`][conda]
    - Packaged via [`pip`][pip]
    - Packaged in our [khiops-notebook][notebooks] container
  - **Khiops Desktop Application**: Maintained in its original form for easy local GUI access.

  [conda]: #with-conda
  [pip]: #with-pip
  [notebooks]: #with-jupyter
  [nocode]: nocode.md

<br>

Refer to the following table to select the appropriate installation method for your operating system.

Legend: :white_check_mark: supported, :warning: works with known limitations, :no_entry_sign: not supported yet.

| OS | :simple-anaconda: Conda | Binary + :simple-python: pip | :simple-docker: Khiops-notebook |  :material-remote-desktop: Desktop app    |
| ----------- | --------------------- | --------------------- | ----------------------- | -------------------------- |
| Windows 7 or later       | [:white_check_mark:][conda_page]  | [:white_check_mark:][pip_page]  | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| Ubuntu 18 LTS or later        | [:white_check_mark:][conda_page]  | [:white_check_mark:][pip_page]  | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| Debian 10 or later   | :no_entry_sign:  | [:white_check_mark:][pip_page] (10) :no_entry_sign: (11,12) | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode] (10) :no_entry_sign: (11, 12)  |
| CentOS 7 and 8    | [:white_check_mark:][conda_page]  | :no_entry_sign:  | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| macOS 10 or later    | [:white_check_mark:][conda_page] (Apple Silicon, Intel)  | :no_entry_sign:  | [:white_check_mark:][notebooks_page] (Intel) [:warning:][notebooks_page] (slow on Apple Silicon)  | :no_entry_sign:  |

  [conda_page]: conda.md
  [pip_page]: pip.md
  [notebooks_page]: khiops-notebook.md
  [nocode]: nocode.md

<br>

## Install the Khiops Python library using Conda <small>  🚧 Beta 🚧 </small> {#with-conda data-toc-label="Install Khiops via conda"}

The Conda package contains all the necessary components. 

=== "Linux"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```
    
=== "Windows"
    ``` sh
    conda install -c khiops khiops
    ```

=== "macOS"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```

[:material-cursor-default-click-outline: See the Conda Installation Page](conda.md){ .md-button .md-button--primary }

<br>

## Install the Khiops Python library using Pip  <small> :tools: Advanced :tools: </small> {#with-pip data-toc-label="Install Khiops via pip"}

Installing the library using Pip requires installing the `khiops` binary first.

=== "Ubuntu"
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB="$(mktemp)" && \
    wget -O "$TEMP_DEB" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core_10.2.0-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB && \
    pip install --no-cache-dir 'git+https://github.com/khiopsml/khiops-python@v10.2.0b2'
    ```

=== "Windows"
    First, you need to download and install the Khiops desktop application:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

    Then, you can run the following Pip command:
    ```sh
    pip install "git+https://github.com/khiopsml/khiops-python@v10.2.0b2"
    ```

=== "CentOS"
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" -y && \
    rm -f $TEMP_RPM && \
    pip install --no-cache-dir 'git+https://github.com/khiopsml/khiops-python@v10.2.0b2'
    ```

!!! info "Currently, our packages are released on GitHub. In the coming weeks, we'll transition to official repositories."

[:material-cursor-default-click-outline: See the Pip Installation Page](pip.md){ .md-button .md-button--primary }

<br>

## Run Khiops with Jupyter Docker Stacks <small>  🚧 Beta 🚧 </small> { #with-jupyter  data-toc-label="Using Khiops on Jupyter notebooks"}

For a quick and easy way to get started with Khiops, you can use our Docker container. 

```bash
docker pull khiopsml/khiops-notebook
```

[:material-cursor-default-click-outline: See the Docker notebooks Installation Page](khiops-notebook.md){ .md-button .md-button--primary }

<br>
  
## Install the Khiops Desktop Application

This version contains a Graphical User Interface (GUI). 


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops desktop application, all its dependencies, plus the Khiops samples and the Khiops Visualization application:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>
    
=== "Ubuntu"
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core_10.2.0-1-${CODENAME}.amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops_10.2.0-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we'll transition to official repositories."


=== "CentOS"
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" "$TEMP_DEB_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_DEB_KHIOPS    ```
    ```

    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we'll transition to official repositories."

    
[:material-cursor-default-click-outline: See the Khiops Desktop Installation Page](nocode.md){ .md-button .md-button--primary }
