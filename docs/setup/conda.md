# Install the Khiops Library Using Conda 

The Conda package installation guarantees optimal performance since it handles installing or upgrading all Khiops dependencies, including the MPI library, in your Conda environment. 

## Instructions

We support :simple-python: **Python from 3.8 to 3.12**. If your current environment is compatible with this requirement, you can proceed as follows:

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

<br>

If your default Conda environment uses a non-compatible Python version (e.g., Python 3.7) or if you need to use a specific python version for ensuring compatibility with other third-party packages, **you can create a new Conda environment for Khiops**, for example, with Python 3.8 (or any version from 3.8 to 3.12 that suits your needs). You can do so by using the command:

```sh
conda create --name khiops_env python=3.8
```

After creating the environment, activate it using:

```sh
conda activate khiops_env
```

Then, proceed with the installation of the Khiops library within this environment.

<br>




## User Guide

- For those who aren't familiar with Conda, you can start by reading [**Getting started with Conda**][conda-user-guide].

[conda-user-guide]: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

- For :simple-googlecolab: **Google Colaboratory** Colab users, please follow usual Conda installation procedure as documented [**here**][conda-colab]

[conda-colab]: https://github.com/conda-incubator/condacolab/tree/0.1.x

- If you use Conda behind **a company proxy**, you may encounter an HTTP and SSL error. In this case, you can read [**Using Anaconda behind a company proxy**][proxy-conda] 

[proxy-conda]: https://docs.anaconda.com/working-with-conda/reference/security/#using-anaconda-behind-a-company-proxy


## What You Should Know

You can consult the limitations or known problems corresponding to your operating system:

=== "Users on :material-apple: macOS"
    ??? tip "Important Note for users upgrading from the previous pyKhiops package (up to 10.1)"
        
        If you are upgrading from a version prior to Khiops 10.2, it is essential that the `pykhiops` package is not installed in your Python environment. This ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

        To uninstall pykhiops, please execute the following command in your terminal or command prompt (use **admin rights** if necessary):

        ```sh
        pip uninstall pykhiops -y
        ```

        Alternatively, you can just create a new, fresh Conda environment and install the Khiops Conda package therein.
    
    ??? danger "Pip and Conda Khiops installations **should not be mixed.**"

        If the users wish to switch from a Conda-based installation to a Pip-based installation, they need to, first, deactivate the Conda environment Khiops is installed into. Or, alternatively, they need to uninstall the Khiops Conda package:

        ``` sh
        conda remove khiops
        ```
        **Note**:  If the standard uninstallation process fails, it may be necessary to add `--force`. This option forces the removal, potentially bypassing dependency conflicts or other issues preventing the package from being uninstalled normally. However, users should be cautious as forcing the removal can impact the stability of their Conda environment and affect other packages.

    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets. To avoid these popups and ensure optimal performance, please configure Khiops to not accept incoming connections. To this end, enter the following commands in your shell:

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
    ??? tip "Important Note for users upgrading from the previous pyKhiops package (up to 10.1)"
        
        If you are upgrading from a version prior to Khiops 10.2, it is essential that the `pykhiops` package is not installed in your Python environment. This ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

        To uninstall pykhiops, please execute the following command in your terminal or command prompt (use **admin rights** if necessary):

        ```sh
        pip uninstall pykhiops -y
        ```

        Alternatively, you can just create a new, fresh Conda environment and install the Khiops Conda package therein.
        
    ??? danger "Pip and Conda Khiops installations **should not be mixed.**"

        If the users wish to switch from a Conda-based installation to a Pip-based installation, they need to, first, deactivate the Conda environment Khiops is installed into. Or, alternatively, they need to uninstall the Khiops Conda package:

        ``` sh
        conda remove khiops
        ```
        
        **Note**:  If the standard uninstallation process fails, it may be necessary to add `--force`. This option forces the removal, potentially bypassing dependency conflicts or other issues preventing the package from being uninstalled normally. However, users should be cautious as forcing the removal can impact the stability of their Conda environment and affect other packages.


    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.

    !!! warning 
        Windows users already having MSMPI installed may see an Anaconda warning suggesting to uninstall it; please ignore this message.


=== "Users on Linux"
    ??? tip "Important Note for users upgrading from the previous pyKhiops package (up to 10.1)"
        
        If you are upgrading from a version prior to Khiops 10.2, it is essential that the `pykhiops` package is not installed in your Python environment. This ensures that your upgrade process is smooth and that the new version of Khiops installs without conflicts.

        To uninstall pykhiops, please execute the following command in your terminal or command prompt (use **admin rights** if necessary):

        ```sh
        pip uninstall pykhiops -y
        ```

        Alternatively, you can just create a new, fresh Conda environment and install the Khiops Conda package therein.
    
    ??? danger "Pip and Conda Khiops installations **should not be mixed.**"

        If the users wish to switch from a Conda-based installation to a Pip-based installation, they need to, first, deactivate the Conda environment Khiops is installed into. Or, alternatively, they need to uninstall the Khiops Conda package:

        ``` sh
        conda remove khiops
        ```
        
        **Note**:  If the standard uninstallation process fails, it may be necessary to add `--force`. This option forces the removal, potentially bypassing dependency conflicts or other issues preventing the package from being uninstalled normally. However, users should be cautious as forcing the removal can impact the stability of their Conda environment and affect other packages.


    !!! warning 

        The installation of Khiops will utilize MPICH version 4.0.3 due to compatibility issues. 
        This is why you need to use a dedicated command:
        ``` sh
        conda install -c conda-forge -c khiops khiops
        ```
            
        Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.

<br>

