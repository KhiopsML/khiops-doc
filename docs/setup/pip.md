# Install the Khiops Library Using Pip <small> :tools: For Advanced users :tools: </small>

Opting for `pip` is ideal for those with a comprehensive grasp of Python's ecosystem and an understanding of operating system specifics. This approach, while offering adaptability for custom setups, necessitates knowledge of environment setup and dependency handling.

The Khiops binaries must be installed as a prerequisite. This also ensures the installation of the appropriate version of `MPICH` library.

We support :simple-python: **Python from 3.8 to 3.12**. 

=== "Ubuntu 20, 22 / Debian 10"
    
    You need to download and install the `khiops-core` package (via Apt) and then the Khiops library (via Pip). You can do this through the following shell commands:
    ``` sh
    sudo apt-get update -y && sudo apt-get install wget lsb-release -y && \
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB="$(mktemp)" && \
    wget -O "$TEMP_DEB" "https://github.com/KhiopsML/khiops/releases/download/10.2.0/khiops-core_10.2.0-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB && \
    pip install 'https://github.com/KhiopsML/khiops-python/releases/download/10.2.0.0/khiops-10.2.0.0.tar.gz'
    ```


=== "Windows"
    You need to download and install the Khiops desktop application first:

    <a href="https://github.com/KhiopsML/khiops/releases/download/10.2.0/khiops-10.2.0-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

    Then, you can run the following Pip command:
    ```sh
    pip install "https://github.com/KhiopsML/khiops-python/releases/download/10.2.0.0/khiops-10.2.0.0.tar.gz"
    ```

=== "Rocky Linux 9"
    
    You need to download and install the `khiops-core` package (via Yum) and then the Khiops library (via Pip). You can do this through the following command:
    ``` sh
    sudo yum update -y && sudo yum install wget python3-pip -y && \
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/10.2.0/khiops-core-10.2.0-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM" -y && \
    rm -f $TEMP_RPM && \
    pip install 'https://github.com/KhiopsML/khiops-python/releases/download/10.2.0.0/khiops-10.2.0.0.tar.gz'
    ```


## User Guide

- Users who want to understand how to manage their Python packages can read the  [**Pip user guide**][pip-tuto]. It will also help those who work behind **a company proxy**.

[pip-tuto]: https://pip.pypa.io/en/stable/user_guide/

- We also encourage our users to use virtual environments. If you are not familiar with them, you can read this [**Python documentation page**][venv].

[venv]: https://docs.python.org/3/library/venv.html


## What You Should Know

You can consult the limitations or known issues for your operating system:

=== "Users on :simple-linux: Linux"
    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we will transition to official repositories."

    ??? tip "Important Note for users upgrading from the pre-10.2.0 versions of the `pyKhiops` package"
    
        If you are upgrading from a version prior to Khiops 10.2.0, it is essential to first make sure the `pykhiops` package is not installed in your Python environment. This ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

        To uninstall pykhiops, please execute the following command in your terminal or command prompt, in your Python environment (use **admin rights** if necessary):

        ```sh
        pip uninstall pykhiops -y
        ```
    ??? danger "Pip and Conda Khiops installations **should not be mixed.**"

        If the users wish to switch from a Pip-based installation to a Conda-based installation, they need to deactivate the Python virtual environment Khiops had been installed into, via Pip. Or, if no virtual environment has been used, the users need to uninstall the Khiops Python package:

        ``` sh
        pip uninstall khiops
        ```

        Even though the Khiops binaries would remain installed on the operating system, the Conda-based installation would take precedence over them.
        
    !!! warning
        The `khiops-core` binary will install or upgrade the system-wide `MPICH` library on your system. If you depend on another version of `MPICH` for other programs, please prefer an installation using Conda.

    !!! warning 

        The installation of Khiops will utilize MPICH version 4.0.3 due to compatibility issues. 
        This is why you need to use a dedicated command:
        ``` sh
        conda install -c conda-forge -c khiops khiops
        ```
            
        Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.


=== "Users on :material-microsoft-windows: Windows"
    !!! info "Currently, our packages are released on GitHub. In the coming weeks, we will transition to official repositories."

    ??? tip "Important Note for users upgrading from the pre-10.2.0 versions of the `pyKhiops` package"
    
        If you are upgrading from a version prior to Khiops 10.2.0, it is essential to first make sure the `pykhiops` package is not installed in your Python environment. This ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

        To uninstall pykhiops, please execute the following command in your terminal or command prompt, in your Python environment (use **admin rights** if necessary):

        ```sh
        pip uninstall pykhiops -y
        ```
    ??? danger "Pip and Conda Khiops installations **should not be mixed.**"

        If the users wish to switch from a Pip-based installation to a Conda-based installation, they need to deactivate the Python virtual environment Khiops had been installed into, via Pip. Or, if no virtual environment has been used, the users need to uninstall the Khiops Python package:

        ``` sh
        pip uninstall khiops
        ```

        Even though the Khiops binaries would remain installed on the operating system, the Conda-based installation would take precedence over them.
        
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.
    !!! warning 
        The Khiops installer relies on embedded installers for Java and MPI. Antivirus software may remove executable files (.exe, .jar) during installation. In this case, **you should add exceptions to your antivirus software or disable it during installation.** 
    !!! warning 
        The java installer results in a system reboot on some systems (e.g. on Windows Server 2008)

=== "Users on :material-apple: macOS"
    !!! warning
        Native packages for the Khiops binaries are not yet available for macOS, which means that you cannot install Khiops on macOS using Pip for now. You can use Conda or run our Docker container (x86-64 only).

<br>

