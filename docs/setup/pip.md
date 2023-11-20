# Install Khiops using pip <small>  Advanced </small> 

Installing the `khiops-core` binary is a prerequisite. 

=== "Ubuntu"
    
    You need to download and install the `khiops-core` package and then the python library. You can do it using the single following command:
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
    pip install "khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1"
    ```

=== "CentOS"
    
    You need to download and install the `khiops-core` package and then the python library. You can do it using the single following command:
    ``` sh
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp)" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum localinstall "$TEMP_RPM" -y && \
    rm -f $TEMP_RPM && \
    pip install --no-cache-dir 'khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1'
    ```


## User guide

- Users who want to understand how to manage their python packages can read the  [**pip user guide**][pip-tuto]. It will also help the ones behind **a company proxy**.

[pip-tuto]: https://pip.pypa.io/en/stable/user_guide/

- We encourage also our users to use virtual environnements. If you are not familiar with it, you can read this [**python documentation page**][venv].

[venv]: https://docs.python.org/3/library/venv.html


## What you should know

You can consult the limitations or known problems corresponding to your operating system:

=== "Users on :simple-linux: Linux"
    !!! warning
        The `khiops-core` binary will install or upgrade the system-wide `MPICH` library in your system. If you depend on another version of `MPICH`, please favor an installation using `conda`.


=== "Users on :material-microsoft-windows: Windows"
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.

=== "Users on :material-apple: Mac"
    !!! warning
        The `khiops-core` binary is not yet available for Mac OS, meaning you cannot install Khiops using `pip` for now. You can use `conda` or run our container (Intel x86-64).
