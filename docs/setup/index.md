# Installation Options {label="Overview"}

Khiops supports a diversified set of installation options, to meet different needs:

  - **Khiops Python Library**:
    - Packaged via [`conda`][conda] (recommended)
    - Packaged via [`pip`][pip]
    - Packaged in our [khiops-notebook][notebooks] container
  - **Khiops Application**: for advanced data analytics with just a few clicks using a graphical user interface. This application is also the basis for easy integration into different systems (all programming languages, docker, servers, etc.).
  - **Khiops Visualization Application**: for intuitive visualization of all analysis results
  - **Khiops Native Interface (KNI)**: to deploy Khiops models with a lightweight shared library.

  [conda]: #with-conda
  [pip]: #with-pip
  [notebooks]: #with-jupyter
  [nocode]: nocode.md
  [kni]: kni.md

<br>

We support :simple-python: **Python from 3.8 to 3.12** and the following operating systems:

- Windows 10 or later
- Ubuntu 20, 22 and 24 (LTS)
- Debian 10, 11 and 12
- Rocky Linux 8 and 9
- macOS 12 or later, only via :simple-anaconda: **Conda**. Full support for ARM architectures, limited support for x86-64 architectures.

The :simple-kaggle: **Kaggle Notebooks** and :simple-googlecolab: **Google Colaboratory** environments are supported. To benefit from Khiops on these environments, users are encouraged to install the Khiops :simple-anaconda: **Conda** package, which has been tested in these environments.

For other platforms, please :material-send: **[Contact Us][contact]**.

  [conda_page]: conda.md
  [pip_page]: pip.md
  [notebooks_page]: khiops-notebook.md
  [nocode]: nocode.md
  [contact]: ../contact.md

<br>


## Install the Khiops Python Library Using Conda <small> Recommended </small> { #with-conda data-toc-label="Install Khiops via conda" }

The Conda package contains all the necessary components.

=== "Linux"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```

=== "Windows"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```

=== "macOS"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```
**We support :simple-python: Python from 3.8 to 3.12**. If you are using a different version of Python in your current environment, we recommend visiting our Conda Installation Page for instructions on creating a new environment tailored for Khiops:

[:material-cursor-default-click-outline: See the Conda Installation Page](conda.md){ .md-button .md-button--primary }

<br>



## Run Khiops with Jupyter Docker Stacks { #with-jupyter  data-toc-label="Using Khiops on Jupyter notebooks"}

For a quick and easy way to get started with Khiops, you can use our Docker container.

```bash
docker pull khiopsml/khiops-notebook
```

[:material-cursor-default-click-outline: See the Docker notebooks Installation Page](khiops-notebook.md){ .md-button .md-button--primary }

<br>

## Install the Khiops Application

This version contains a standalone Graphical User Interface (GUI).


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops application, all its dependencies, plus the Khiops samples and the Khiops Visualization application:

    <a href="https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-{{ KHIOPS_VERSION }}-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

=== "Ubuntu/Debian"

    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-core-openmpi_{{ KHIOPS_VERSION }}-1-${CODENAME}.amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops_{{ KHIOPS_VERSION }}-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we will transition to official repositories."

=== "Rocky Linux"

    ``` sh
    sudo yum update -y && sudo yum install wget -y && \
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp).rpm" && \
    TEMP_RPM_KHIOPS="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-core-openmpi-{{ KHIOPS_VERSION }}-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_RPM_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-{{ KHIOPS_VERSION }}-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM" "$TEMP_RPM_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_RPM_KHIOPS    ```
    ```


[:material-cursor-default-click-outline: See the Khiops Desktop Installation Page](nocode.md){ .md-button .md-button--primary }

<br>

## Install the Khiops Visualization Applications

[:material-cursor-default-click-outline: See the Khiops Visualization Page](visualization.md){ .md-button .md-button--primary } [:octicons-graph-16: Try our Interactive Demo](demovisualization.md){ .md-button .md-button--secondary }

<br>

## Install the Khiops Python library using Pip  <small> :tools: For Advanced users :tools: </small> { #with-pip data-toc-label="Install Khiops via pip" }

Using `pip` for installation is best suited for experienced users, especially those integrating Khiops into specific environments or requiring advanced configuration. **This method offers flexibility, but requires familiarity with operating systems specifics, Python-based environments and dependency management.**

[:material-cursor-default-click-outline: See the Pip Installation Page](pip.md){ .md-button .md-button--primary }

