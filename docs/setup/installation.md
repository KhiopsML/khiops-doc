# Installation

Khiops was originally released as a desktop application with a graphical user interface, the "No code" version, which is currently production-ready and available [here][nocode]. **But, as part of our recent transition to open-source, we are actively expanding the installation options to meet various user requirements**. Specifically, we offer a *beta* version of a [`conda`][conda] packaging (managing the MPI installation, what `pip` cannot) and a beta version of a notebook image based on the [`Jupyter`][jupyter] Docker Stacks. Details and installation steps are provided below.

  [conda]: #with-conda
  [jupyter]: #with-docker
  [docker]: #with-jupyter
  [nocode]: nocode.md

## Install Khiops using conda <small>  🚧 Beta 🚧 </small> {#with-conda data-toc-label="Install Khiops via conda"}

The `conda` installation guarantees optimal performance since it handles installing or upgrading the MPI library on your system. For those who aren't familiar with `conda`, you can start by reading [**Getting started with conda**][conda-user-guide].

[conda-user-guide]: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

``` sh
conda install -c khiops khiops
```

On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality. Plus, Windows users already having MSMPI installed may see an anaconda warning suggesting to uninstall it; please ignore this message.

!!! warning "Temporary limitation on :material-apple: Apple Silicon"
    
    For users on Apple Silicon: The installation of Khiops will utilize MPICH version 3.4.3 due to compatibility concerns. 
    
    You would need to execute the following command for installation:
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```
    Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.

## Using Khiops with Jupyter Docker Stacks <small>  🚧 Beta 🚧 </small> { #with-jupyter  data-toc-label="Using Khiops on Jupyter notebooks"}

For a quick and easy way to get started with Khiops, you can use our pre-built Jupyter Docker image. This image is based on the official [Jupyter Docker Stacks][jupyterdockerstacks] and comes pre-configured on top of `scipy-notebooks`.

[jupyterdockerstacks]:https://jupyter-docker-stacks.readthedocs.io/en/latest/

To get the Khiops Docker image, run the following command:
```bash
docker pull khiopsml/khiops-notebook
```

**Try it without effort using Binder**: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KhiopsML/khiops-notebook/main/)

!!! warning "Our Jupyter Docker image is not yet build for ARM architecture"
    Running it will be extremly slow on :simple-raspberrypi: Raspberry or :material-apple: Apple Silicon.


## Install Khiops using pip <small>  Advanced </small> {#with-pip data-toc-label="Install Khiops via pip"}

Before proceeding with the `pip` installation, there are essential prerequisites:

- **Windows Users**: Install Khiops on your machine using the desktop application.
- **Linux Users**: Ensure you've installed the `khiops-core` package. This will set up an appropriate version of `MPI` on your system.

Instructions for installation are available [here][nocode]. This method is not yet available for :material-apple: Mac users. 

Once the prerequisites are met, you can install Khiops using the following command:

```sh
pip install 'khiops @ git+https://github.com/khiopsml/khiops-python@v10.2.0b1'
```

