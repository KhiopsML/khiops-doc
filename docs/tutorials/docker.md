# Running Khiops with Docker

Docker provides a convenient way to run Khiops in a consistent and documented environment, making it easier to manage dependencies and ensure clarity across different systems. This is particularly useful for running Khiops on different operating systems, ensuring consistency across development and production setups.

With Khiops official Docker images, you can execute Khiops commands in isolated environments while benefiting from containerization's flexibility and portability. 

## Why Use Docker for Khiops?

Using Docker to run Khiops offers several advantages:

- **No installation required**: No need to install dependencies manually—simply pull the Khiops Docker image and start using it;
- **Cross-platform compatibility**: Run Khiops consistently on Windows, macOS, and Linux without worrying about system dependencies;
- **Reproducibility**: Ensure the same execution environment across different machines and teams;
- **Easy integration into workflows**: Docker allows seamless integration into CI/CD pipelines and automation scripts.

## Getting Started

### Base Images

You will find two images on dockerhub:

- **khiopsml/khiops-ubuntu**: A minimal installation of Khiops on Ubuntu.
- **khiopsml/khiops-python**: The same base image with Khiops-Python preinstalled.
 
### Basic Usage

By default, the Docker image is configured to launch a Khiops service. You can also run specific commands or use interactive mode. Here’s how to get started:

**Running a Scenario File**

To run a specific scenario file located in your local directory, use the following command:

```bash
docker run -v $PWD:/my_data \
  -it khiopsml/khiops-ubuntu
  khiops -b -i /my_data/my_scenario.kh
```

This command mounts your current directory (`$PWD`) to `/my_data` in the container and runs the specified scenario file using Khiops.


**Running a Python Script**

Similarly, you can use the Python image to run a Khiops-Python script:

```bash
docker run -v $PWD:/my_volume \
  -it khiopsml/khiops-python
  python /my_volume/script.py
```

This command mounts your current directory to `/my_volume` in the container and executes the specified Python script.

### Service Usage

You can run the container as a Khiops service, allowing it to process multiple scenarios without restarting the container. Here's how to set it up:

```bash
docker run -v $PWD:/my_data -p 11000:11000 \
  -it khiopsml/khiops-ubuntu
```

This command maps port 11000 on your host to the container, enabling you to submit requests to the Khiops service.

**Submitting a Request**

To process a scenario, send a POST request to the REST endpoint using standard HTTP tools (cURL, wget, postman...):

```bash
curl -k -X POST -d "{\"scenario\": \"/my_data/my_scenario.kh\"}" "https://localhost:11000/v1/batch" \
 -H "accept: application/json"
```

This command submits a job to the Khiops service to process the specified scenario file. The API definition is available at https://localhost:11000.

## Conclusion
Using Docker with Khiops simplifies deployment and ensures a consistent environment across different systems. Whether you're running specific commands or using it as a service, Docker provides the flexibility to integrate Khiops seamlessly into your workflow. 