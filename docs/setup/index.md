# Installation Options {label="Overview"}

Khiops supports a diversified set of installation options, to meet different needs:

  - **Khiops Python Library**:
    - Packaged via [`conda`][conda]
    - Packaged via [`pip`][pip]
    - Packaged in our [khiops-notebook][notebooks] container
  - **Khiops Desktop Application**: for advanced data analytics with just a few clicks using a GUI (includes Khiops Visualization)
  - **Khiops Visualization Application**: for intuitive visualization of all analysis results

  [conda]: #with-conda
  [pip]: #with-pip
  [notebooks]: #with-jupyter
  [nocode]: nocode.md

<br>

Refer to the following table to select the appropriate installation method for your operating system. <br>We support :simple-python: **Python from 3.8 to 3.11.**

| OS | :simple-anaconda: Conda | Binary + :simple-python: pip | :simple-docker: Khiops-notebook |  :material-remote-desktop: Desktop app    |
| ----------- | --------------------- | --------------------- | ----------------------- | -------------------------- |
| :material-microsoft-windows: Windows 10 and later | [:white_check_mark:][conda_page]  | [:white_check_mark:][pip_page]  | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| :material-apple: macOS 10 and later    | [:white_check_mark:][conda_page]   |   | [:white_check_mark:][notebooks_page] |   |
| :simple-linux: Ubuntu 20 and 22 (LTS)        | [:white_check_mark:][conda_page]  | [:white_check_mark:][pip_page]  | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| :simple-linux: Debian 10  | [:white_check_mark:][conda_page]  | [:white_check_mark:][pip_page] | [:white_check_mark:][notebooks_page]  | [:white_check_mark:][nocode]  |
| :simple-linux: Debian 11 and 12   | [:white_check_mark:][conda_page]  |   | [:white_check_mark:][notebooks_page]  |  |
| :simple-linux: Rocky Linux 7 and 8    | [:white_check_mark:][conda_page]  |   | [:white_check_mark:][notebooks_page]  |   |

The :simple-kaggle: **Kaggle Notebooks** and :simple-googlecolab: **Google Colaboratory** environments are supported. To benefit from Khiops on these environments, users are encouraged to install the Khiops the :simple-anaconda: **Conda** package, which has been tested in these environments.

  [conda_page]: conda.md
  [pip_page]: pip.md
  [notebooks_page]: khiops-notebook.md
  [nocode]: nocode.md

<br>

## Install the Khiops Python Library Using Conda {#with-conda data-toc-label="Install Khiops via conda"}

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
**We support :simple-python: Python from 3.8 to 3.11**. If you are using a different version of Python in your current environment, we recommend visiting our Conda Installation Page for instructions on creating a new environment tailored for Khiops:

[:material-cursor-default-click-outline: See the Conda Installation Page](conda.md){ .md-button .md-button--primary }

<br>



## Run Khiops with Jupyter Docker Stacks { #with-jupyter  data-toc-label="Using Khiops on Jupyter notebooks"}

For a quick and easy way to get started with Khiops, you can use our Docker container.

```bash
docker pull khiopsml/khiops-notebook
```

[:material-cursor-default-click-outline: See the Docker notebooks Installation Page](khiops-notebook.md){ .md-button .md-button--primary }

<br>
  
## Install the Khiops Desktop Application

This version contains a standalone Graphical User Interface (GUI). 


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops desktop application, all its dependencies, plus the Khiops samples and the Khiops Visualization application:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>
    
=== "Ubuntu/Debian"
    
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

<!--- 
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
--->
    
[:material-cursor-default-click-outline: See the Khiops Desktop Installation Page](nocode.md){ .md-button .md-button--primary }

<br>

## Install the Khiops Visualization Applications

Please refer to the dedicated page to install the visualization or co-visualization tool according to your needs and host operating system. 

[:material-cursor-default-click-outline: See the Khiops Visualization Page](visualization.md){ .md-button .md-button--primary } [:octicons-graph-16: Try our Interactive Demo](demovisualization.md){ .md-button .md-button--secondary }

<br>

## Install the Khiops Python library using Pip  <small> :tools: For Advanced users :tools: </small> {#with-pip data-toc-label="Install Khiops via pip"}

Using `pip` for installation is best suited for experienced users, especially those integrating Khiops into specific environments or requiring advanced configuration. **This method offers flexibility, but requires familiarity with operating systems specifics, Python-based environments and dependency management.**

[:material-cursor-default-click-outline: See the Pip Installation Page](pip.md){ .md-button .md-button--primary }

