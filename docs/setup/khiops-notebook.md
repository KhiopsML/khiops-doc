# Run Khiops with Jupyter Docker Stacks 

For a quick and easy way to get started with Khiops, you can use our pre-built Docker image.

To get the Khiops Docker image, run the following command:
```bash
docker pull khiopsml/khiops-notebook
```

## User guide

- This image is based on the official [**Jupyter Docker Stacks**][jupyterdockerstacks] and comes pre-configured on top of `scipy-notebooks`.

[jupyterdockerstacks]:https://jupyter-docker-stacks.readthedocs.io/en/latest/

- A more general introduction to containers can be found on the [**Docker user guide**][docker-guide].

[docker-guide]: https://docs.docker.com/get-started/


## What you should know

Some limitations regarding the target architecture:

=== "Users on ARM architecture"
    !!! warning 
        Our Jupyter Docker image is not yet built for the ARM microprocessor architecture. Running it will be extremely slow on :simple-raspberrypi: Raspberry or :material-apple: Apple Silicon.

