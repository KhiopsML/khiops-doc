# Khiops Desktop (No Code)

## Simplifying Data Science for Everyone

Welcome to the Khiops Desktop Application download page. Our intuitive, user-friendly desktop interface is designed for those who may not be familiar with Python or scikit-learn, as well as for users who prefer the convenience of a Graphical User Interface (GUI) for data manipulation. With Khiops Desktop, advanced data analytics is now just a few clicks away.



## Download & Installation

To get started with the Khiops Desktop Application, follow the procedure appropriate for your operating system. Please click on the relevant operating system after reading [README.txt][readme], [install.txt][install] and [whatsnew.txt][whatsnew]:

[releases]: https://github.com/KhiopsML/khiops/releases
[readme]: README.txt
[install]: install.txt
[whatsnew]: whatsnewV10.1.txt


=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs all your needs, including the Khiops samples et the Khiops Visualization application.

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

=== "Ubuntu"
    The installation of Khiops Desktop requires two packages: `khiops-core` and `khiops` (containing the GUI). 
    
    You can run the following command:
    
    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+${CODENAME}_amd64.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops_10.1.1-0+${CODENAME}_amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    If you need the Khiops samples, you can add the following package:
    ```sh
    https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples_10.1.1-0+${CODENAME}_all.deb
    ```

=== "CentOS"
    The installation of Khiops Desktop requires two packages: `khiops-core` and `khiops` (containing the GUI). 
    
    You can run the following command:
    
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" "$TEMP_DEB_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_DEB_KHIOPS    
    ```

    If you need the Khiops samples, you can add the following package:
    ```sh
    https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm
    ```

You can find the all versions on the [releases page][releases].

## Documentation
For a comprehensive guide on how to use the Khiops Desktop Application, please download our [**PDF Documentation**][Documentation]. 

The users already familiar with the CoClustering approach will find the dedicated documentation [**here**][coclustering].

[Documentation]: KhiopsGuide.pdf
[coclustering]: KhiopsCoclusteringGuide.pdf

A tutorial is also [**available**][tutorial] to help you understand and grasp the tool.

[tutorial]: KhiopsTutorial.pdf

!!! info "For users on Khiops versions prior to 10.1, the license support is available via [khiops.tech.orange][khiopslegacy]"

[khiopslegacy]: https://khiops.tech.orange

## Screenshots 

<div class="text-center">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/feature_eng_pane.png">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/database_pane.png">
</div>