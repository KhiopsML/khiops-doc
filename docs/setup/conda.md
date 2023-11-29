# Install the Khiops Library Using Conda <small>  🚧 Beta 🚧 </small>

The Conda package installation guarantees optimal performance since it handles installing or upgrading all Khiops dependencies, including the MPI library, in your Conda environment. 

## Instructions

=== "x86-64"
    ``` sh
    conda install -c khiops khiops
    ```

=== ":material-apple: Apple Silicon (ARM64)"
    ``` sh
    conda install -c conda-forge -c khiops khiops
    ```


## User Guide

- For those who aren't familiar with Conda, you can start by reading [**Getting started with Conda**][conda-user-guide].

[conda-user-guide]: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

- If you use Conda behind **a company proxy**, you may encounter an HTTP and SSL error. In this case, you can read [**Using Anaconda behind a company proxy**][proxy-conda] 

[proxy-conda]: https://docs.anaconda.com/free/anaconda/configurations/proxy/


## What You Should Know

You can consult the limitations or known problems corresponding to your operating system:

=== "Users on :material-microsoft-windows: Windows"
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.

    !!! warning 
        Windows users already having MSMPI installed may see an Anaconda warning suggesting to uninstall it; please ignore this message.


=== "Users on :material-apple: Apple Silicon"
    !!! warning 

        The installation of Khiops will utilize MPICH version 3.4.3 due to compatibility issues. 
        This is why you need to use a dedicated command:
        ``` sh
        conda install -c conda-forge -c khiops khiops
        ```
            
        Be aware that this may result in **slower execution times** compared to other platforms. This limitation is expected to be addressed in a future MPICH release.
    !!! warning 
        On the first run of Khiops, **an MPI-related popup may appear** due to parallel execution sockets; please allow access for optimal functionality.


<br>
