# The Khiops Application (No-Code Environment)

## Simplifying Data Science for Everyone

Welcome to the Khiops application download page. Our intuitive, user-friendly desktop interface is designed for those who may not be familiar with Python or scikit-learn, as well as for users who prefer the convenience of a standalone Graphical User Interface (GUI) for data manipulation. With the Khiops application, advanced data analytics is now just a few clicks away, together with easy system integration.


## Download & Installation

To get started with the Khiops application, follow the relevant procedure for your operating system. Please click on the relevant operating system. Note that our Application **is not yet available on :material-apple: macOS**.

For further details, you may refer to [README.txt][readme], and [whatsnew.txt][whatsnew]:

[releases]: https://github.com/KhiopsML/khiops/releases
[readme]: README.txt
[whatsnew]: WHATSNEW.txt


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops application, all its dependencies, plus some data samples formatted as expected by Khiops, and the Khiops Visualization application.

    <a href="https://github.com/KhiopsML/khiops/releases/download/10.2.2/khiops-10.2.2-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

=== "Ubuntu / Debian"
    The installation of the Khiops desktop application involves two packages:
    
     - `khiops-core`: This is a lightweight package without GUI, documentation or samples. It is intended to be used in advanced settings, on servers and Docker images.
     - `khiops`: This package requires `khiops-core` and is the full version of Khiops containing the GUI and the documentation.

    You can install both packages as follows:
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/10.2.2/khiops-core-openmpi_10.2.2-1-${CODENAME}.amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/10.2.2/khiops_10.2.2-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    If you need the Khiops samples, you can run the following commands:
    ```sh
    TEMP_SAMPLES="$(mktemp)" && \
    wget -O "$TEMP_SAMPLES" "https://github.com/KhiopsML/khiops-samples/releases/download/10.2.0/khiops-samples-10.2.0.zip" && \
    mkdir -p ~/khiops_data/samples && \
    unzip "$TEMP_SAMPLES" -d ~/khiops_data/samples && \
    rm -f $TEMP_SAMPLES
    ```

    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we will transition to official repositories."

=== "Rocky Linux"
    The installation of the Khiops desktop application involves two packages:
    
     - `khiops-core`: This is a lightweight package without GUI, documentation or samples. It is intended to be used in advanced settings, on servers and Docker images.
     - `khiops`: This package requires `khiops-core` and is the full version of Khiops containing the GUI and the documentation.

    You can install both packages as follows:

    ``` sh
    sudo yum update -y && sudo yum install wget python3-pip -y && \
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp).rpm" && \
    TEMP_RPM_KHIOPS="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/10.2.2/khiops-core-openmpi-10.2.2-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_RPM_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/10.2.2/khiops-10.2.2-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM" "$TEMP_RPM_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_RPM_KHIOPS
    ```

You can find the all versions on the [releases page][releases].

## Documentation

For a comprehensive guide on how to use the Khiops application and its GUI:

- [**Khiops Guide**][Documentation], for supervised analysis
- [**Khiops Coclustering Guide**][coclustering], for unsupervised analysis
- [**Tutorial**][tutorial]

For easy system integration: 

- [**Khiops Scenarios**][scenario], based on recording and replaying Khiops scenarios in batch mode from any programming language."


[tutorial]: KhiopsTutorial.pdf
[Documentation]: KhiopsGuide.pdf
[coclustering]: KhiopsCoclusteringGuide.pdf
[scenario]: KhiopsScenarios-v10.2.0.pdf    

!!! info "Users of pre-10.2.0 Khiops versions should refer to the **legacy** Khiops [web site][khiopslegacy]"

[khiopslegacy]: https://khiops.tech.orange

## What You Should Know

You can consult the limitations or known problems for your operating system:

=== "Users on :material-microsoft-windows: Windows"
    !!! warning 
        The Khiops installer relies on embedded installers for Java and MPI. Antivirus software may remove executable files (.exe, .jar) during installation. In this case, **you should add exceptions to your antivirus software or disable it during installation.** 
    !!! warning 
        The java installer results in a system reboot on some systems (e.g. on Windows Server 2008)
    !!! warning
        On some machines, re-installing Khiops may unexpectedly result in just discarding the existing Khiops installation directory. In that case, uninstall Khiops before reinstalling it.
    

## Screenshots 

<div class="text-center">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/feature_eng_pane.png">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/database_pane.png">
</div>
