<!-- Transform the pre-release versions for the rocky and python packages
{% set PIP_KHIOPS_PYTHON_VERSION = KHIOPS_PYTHON_VERSION.replace("-rc.", "rc").replace("-b.", "b").replace("-a.", "a") %}
-->

# Install the Khiops Library Using Uv

The `pip` package supports the installation and upgrade of all Khiops dependencies, including the MPI library, in your virtual environment, via Uv.

We support :simple-python: **Python from 3.11 to 3.15**.

``` sh
uv venv
uv pip install khiops=={{ PIP_KHIOPS_PYTHON_VERSION }}
```

If you intend to use remote resources while working with the Khiops Library you will have to install additional dependencies ([**vendors-specific SDK and Khiops drivers**](drivers-and-sdk-for-library.md)). 

This can be performed by specifying the type of remote storage (`s3`, `gcs` or `azure`) in square brackets.



```sh 
uv pip install khiops[s3]=={{ PIP_KHIOPS_PYTHON_VERSION }} # for a specific storage type only
uv pip install khiops[s3,gcs,azure]=={{ PIP_KHIOPS_PYTHON_VERSION }} # for all the supported storage types
```

## User Guide

- Users who want to understand how to manage their Python packages can read the  [**Uv user guide**][uv-tuto].

[uv-tuto]: https://docs.astral.sh/uv/

## What You Should Know

??? danger "Uv and Conda Khiops installations **should not be mixed.**"

    If the users wish to switch from a Uv-based installation to a Conda-based installation, they need to uninstall the Khiops Library package:

    ``` sh
    uv pip uninstall khiops
    ```

=== "Users on :material-microsoft-windows: Windows"
    !!! warning
        In some companies, Windows AppLocker may block running installed Python packages via an IDE or terminal. If you encounter issues, try installing the Khiops Python library in a recommended directory or run your IDE or terminal as an administrator.

<br>

