# Install the Khiops Library Using Conda <small>  🚧 Beta 🚧 </small>

The Conda package installation guarantees optimal performance since it handles installing or upgrading all Khiops dependencies, including the MPI library, in your Conda environment. 

## Instructions

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

<br>

??? tip "Important Note for Users Upgrading from the previous pyKhiops package (up to 10.1)"
    
    If you are upgrading from a version prior to Khiops 10.2, it is essential to first uninstall the `pykhiops` package. This step ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

    To uninstall pykhiops, please execute the following command in your terminal or command prompt:

    ```sh
    pip uninstall pykhiops -y
    ```

## User Guide

- For those who aren't familiar with Conda, you can start by reading [**Getting started with Conda**][conda-user-guide].

[conda-user-guide]: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

- If you use Conda behind **a company proxy**, you may encounter an HTTP and SSL error. In this case, you can read [**Using Anaconda behind a company proxy**][proxy-conda] 

[proxy-conda]: https://docs.anaconda.com/free/anaconda/configurations/proxy/


## What You Should Know

You can consult the limitations or known problems corresponding to your operating system:

=== "Users on :material-apple: Apple Silicon"
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets. To avoid these popups and ensure optimal performance, please run the following commands:

        ``` sh
        FW=/usr/libexec/ApplicationFirewall/socketfilterfw 
        sudo $FW --remove $(which MODL)
        sudo $FW --add $(which MODL)
        sudo $FW --block $(which MODL)
        ```
    
    !!! warning 

        The installation of Khiops will utilize MPICH version 3.4.3 due to compatibility issues. 
        This is why you need to use a dedicated command:
        ``` sh
        conda install -c conda-forge -c khiops khiops
        ```
            
        Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.

=== "Users on :material-microsoft-windows: Windows"
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.

    !!! warning 
        Windows users already having MSMPI installed may see an Anaconda warning suggesting to uninstall it; please ignore this message.


=== "Users on Linux"
    !!! warning 

        The installation of Khiops will utilize MPICH version 3.4.3 due to compatibility issues. 
        This is why you need to use a dedicated command:
        ``` sh
        conda install -c conda-forge -c khiops khiops
        ```
            
        Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.


    


<br>
