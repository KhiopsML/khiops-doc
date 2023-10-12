# Installation

Khiops was originally released as a desktop application with a graphical user interface, the "No code" version, which is currently production-ready and available [here][nocode]. **But, as part of our recent transition to open-source, we are actively expanding the installation options to meet various user requirements**. Specifically, we offer a *beta* version of a [`conda`][conda] packaging (managing the MPI installation, what `pip` cannot) and a beta version of a notebook image based on the [`Jupyter`][jupyter] Docker Stacks. Details and installation steps are provided below.

  [conda]: #with-conda
  [jupyter]: #with-docker
  [docker]: #with-jupyter
  [nocode]: nocode.md

## Install Khiops using conda <small>  🚧 Beta 🚧 </small> {#with-conda data-toc-label="Install Khiops via conda"}

The `conda` installation guarantees optimal performance since it handles installing or upgrading the MPI library on your system. Windows users already having MSMPI installed may see an anaconda warning suggesting to uninstall it; please ignore this message.

``` sh
conda install -c khiops khiops
```

On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.

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


## Getting Khiops with docker { #with-docker  }

The official [Docker image] provides all the necessary to start using Khiops, including notebooks samples. Open up a terminal
and pull the image with:

  [Docker image]: https://hub.docker.com/r/squidfunk/mkdocs-material/

```
docker pull dockerfactory.tech.orange/khiops/docker/khiops-ubuntu:20.04-0.6.1
```


??? question "How to add plugins to the Docker image?"

    Khiops only bundles selected plugins in order to keep the size
    of the official image small. If the plugin you want to use is not included, 
    create a new `Dockerfile` and extend the official Docker image:

    ``` Dockerfile
    FROM dockerfactory.tech.orange/khiops/docker/khiops-ubuntu-slim:20.04-0.6.1
    ADD my_code_and_packages /where_I_want_them
    # Write my_own_entrypoint.sh, calling install_license.sh if needed
    ADD my_own_entrypoint.sh
    RUN chmod +x my_own_entrypoint.sh
    ENTRYPOINT ["/tini", "--", "/my_own_entrypoint.sh"]
    ```

    Next, you can build the image with the following command:

    ```
    docker build -t dockerfactory.tech.orange/khiops/docker/khiops-ubuntu:20.04-0.6.1 .
    ```

    The new image can be used exactly like the official image.

