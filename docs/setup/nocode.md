# The Khiops Desktop Application (No-Code Environment)

## Simplifying Data Science for Everyone

Welcome to the Khiops desktop application download page. Our intuitive, user-friendly desktop interface is designed for those who may not be familiar with Python or scikit-learn, as well as for users who prefer the convenience of a Graphical User Interface (GUI) for data manipulation. With the Khiops desktop application, advanced data analytics is now just a few clicks away.



## Download & Installation

To get started with the Khiops desktop application, follow the relevant procedure for your operating system. Please click on the relevant operating system after reading [README.txt][readme], [install.txt][install] and [whatsnew.txt][whatsnew]:

[releases]: https://github.com/KhiopsML/khiops/releases
[readme]: README.txt
[install]: install.txt
[whatsnew]: whatsnewV10.1.txt


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops desktop application, all its dependencies, plus the Khiops samples and the Khiops Visualization application.

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

=== "Ubuntu"
    The installation of the Khiops desktop application involves two packages: `khiops-core` and `khiops` (containing the GUI). 
    
    You can run the following command:
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core_10.2.0-1-${CODENAME}.amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops_10.2.0-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    If you need the Khiops samples, you can install the `khiops-samples` package:
    ```sh
    TEMP_DEB_SAMPLES="$(mktemp)" && \
    wget -O "$TEMP_DEB_SAMPLES" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples_10.1.1-0+${CODENAME}_all.deb" && \
    sudo dpkg -i "$TEMP_DEB_SAMPLES" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_SAMPLES
    ```

=== "CentOS"
    The installation of the Khiops desktop application requires two packages: `khiops-core` and `khiops` (containing the GUI). 
    
    You can run the following command:
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp).rpm" && \
    TEMP_RPM_KHIOPS="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-core-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_RPM_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.2.0/khiops-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM" "$TEMP_RPM_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_RPM_KHIOPS
    ```

    In order to finalize the installation, elect `mpich` as the module that provides MPI support for the current shell session, by running the following commands:

    ``` sh
    source /etc/profile.d/modules.sh
    module unload mpi
    MPICH_MODULE=$(module avail |& sed -E -e 's/[[:blank:]]/\n/g' | grep mpich
    | sort | tail -1)
    module load $MPICH_MODULE
    ```

    These commands need to be executed upon each launch of a shell process. Hence, it can be practical to put them into a file that is automatically sourced upon shell launch, such as `~/.bashrc`.

    If you need the Khiops samples, you can install the `khiops-samples` package:

    ```sh
    TEMP_RPM_SAMPLES="$(mktemp)" && \
    wget -O "$TEMP_RPM_SAMPLES" https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm && \
    sudo yum install "$TEMP_RPM_SAMPLES" -y && \
    rm -f $TEMP_RPM_SAMPLES
    ```

You can find the all versions on the [releases page][releases].

## Documentation
For a comprehensive guide on how to use the Khiops desktop application, please download our [**PDF Documentation**][Documentation]. 

The users already familiar with the CoClustering approach will find the dedicated documentation [**here**][coclustering].

[Documentation]: KhiopsGuide.pdf
[coclustering]: KhiopsCoclusteringGuide.pdf

A tutorial is also [**available**][tutorial] to help you understand and grasp the Khiops desktop application.

[tutorial]: KhiopsTutorial.pdf

!!! info "For users on Khiops versions prior to 10.1, the license support is available via [khiops.tech.orange][khiopslegacy]"

[khiopslegacy]: https://khiops.tech.orange

## Screenshots 

<div class="text-center">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/feature_eng_pane.png">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/database_pane.png">
</div>
