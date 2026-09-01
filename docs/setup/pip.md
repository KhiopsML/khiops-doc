<!-- Transform the pre-release versions for the rocky and python packages
{% set PIP_KHIOPS_PYTHON_VERSION = KHIOPS_PYTHON_VERSION.replace("-rc.", "rc").replace("-b.", "b").replace("-a.", "a") %}
{% set ROCKY_KHIOPS_VERSION = KHIOPS_VERSION.replace("-", "_") %}
-->

# Install the Khiops Library Using Pip

The `pip` package supports the installation and upgrade of all Khiops dependencies, including the MPI library, in your virtual environment.

We support :simple-python: **Python from 3.10 to 3.14**. Usage of previous
versions of Python can be attempted, but there is no support for it.

===  "Linux and macOS"

    In a dedicated virtual environment (recommended)

    ``` sh
    python -m venv myvenv
    source myenv/bin/activate
    pip install khiops=={{ PIP_KHIOPS_PYTHON_VERSION }}
    ```

=== "Windows"

    In a dedicated virtual environment (recommended)

    ```sh
    python -m venv myvenv
    myenv\Scripts\activate.bat
    pip install khiops=={{ PIP_KHIOPS_PYTHON_VERSION }}
    ```

If you intend to use remote resources while working with the Khiops Library you will have to install additional dependencies ([**vendors-specific SDK and Khiops drivers**](drivers-and-sdk-for-library.md)). 

This can be performed, still in a dedicated virtual environment as recommended, by specifying the type of remote storage (`s3`, `gcs` or `azure`) in square brackets.



```sh 
pip install khiops[s3]=={{ PIP_KHIOPS_PYTHON_VERSION }} # for a specific storage type only
pip install khiops[s3,gcs,azure]=={{ PIP_KHIOPS_PYTHON_VERSION }} # for all the supported storage types
```

## User Guide

- Users who want to understand how to manage their Python packages can read the  [**Pip user guide**][pip-tuto]. It will also help those who work behind **a company proxy**.

[pip-tuto]: https://pip.pypa.io/en/stable/user_guide/

- We also encourage our users to use virtual environments. If you are not familiar with them, you can read this [**Python documentation page**][venv].

[venv]: https://docs.python.org/3/library/venv.html


## What You Should Know

??? danger "Pip and Conda Khiops installations **should not be mixed.**"

    If the users wish to switch from a Pip-based installation to a Conda-based installation, they need to deactivate the Python virtual environment Khiops had been installed into, via Pip. Or, if no virtual environment has been used, the users need to uninstall the Khiops Library package:

    ``` sh
    pip uninstall khiops
    ```

=== "Users on :material-microsoft-windows: Windows"
    !!! warning
        In some companies, Windows AppLocker may block running installed Python packages via an IDE or terminal. If you encounter issues, try installing the Khiops Python library in a recommended directory or run your IDE or terminal as an administrator.

<br>

