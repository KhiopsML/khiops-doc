# Distibuted execution with k8s

Kubernetes is a powerful platform for managing containerized applications, and it's an excellent choice for deploying Khiops in a **scalable and distributed manner**. One of the most remarkable features of Khiops is its ability to run seamlessly across multiple machines, thanks to its usage of MPI (Message Passing Interface). This means you can effortlessly scale your Khiops deployments using the same [docker image][dockerhub] across a Kubernetes cluster, making it incredibly straightforward to leverage distributed computing resources.

[dockerhub]: https://hub.docker.com/u/khiopsml

This guide will walk you through the process of setting up Khiops on a Kubernetes cluster using the MPI Operator to handle distributed execution. The setup leverages the official Khiops Docker image, ensuring consistency and simplicity across environments. For more details on using Khiops with Docker, refer to the [dedicated page][docker].

[docker]: ./docker.md

## Prerequisites

To run Khiops on Kubernetes, you need to have a Kubernetes cluster up and running. Additionally, you'll need to install the **MPI Operator**, which simplifies the deployment of MPI (Message Passing Interface) jobs on Kubernetes and manages the provisioning of worker nodes for distributed computing tasks. Follow the official [MPI Operator documentation][mpi-op]  to install it on your cluster.

[mpi-op]: https://github.com/kubeflow/mpi-operator

## Job Definition

Once the MPI Operator is installed, you can define an MPI Job to run Khiops with the desired configuration and resources. Below is an example of a Kubernetes manifest for an MPI Job that runs the `khiops -s` command which displays the allocated resources as seen by the Khiops program:

```yaml
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: khiops
spec:
  slotsPerWorker: 4
  runPolicy:
    cleanPodPolicy: Running
    ttlSecondsAfterFinished: 3600
  sshAuthMountPath: /home/ubuntu/.ssh
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
          - image: khiopsml/khiops-ubuntu
            name: mpi-launcher
            securityContext:
              runAsUser: 1000
            args:
            - khiops
            - -s
            resources:
              limits:
                cpu: 1
                memory: 512Mi
    Worker:
      replicas: 2
      template:
        spec:
          containers:
          - image: khiopsml/khiops-ubuntu
            name: mpi-worker
            securityContext:
              runAsUser: 1000
            args:
            - /usr/sbin/sshd
            - -De
            - -f
            - /home/ubuntu/.sshd_config
            env:
            - name: KHIOPS_MEMORY_LIMIT
              valueFrom:
                resourceFieldRef:
                  divisor: "1Mi"
                  resource: requests.memory
            readinessProbe:
              tcpSocket:
                port: 2222
              initialDelaySeconds: 4
            resources:
              requests
                cpu: 4
                memory: 4Gi
```

### Explanation

- **slotsPerWorker**: Defines the number of processes per worker pod (must be set to **at least 2** for Khiops to function correctly). It's recommended t**o set this equal to the number of CPU cores** requested for optimal performance. In the example, each of the 2 worker pods runs 4 virtual cpus, totaling 8 processes.
- **runPolicy**: Specifies policies for cleaning up pods and setting a time-to-live for finished jobs.
- **mpiReplicaSpecs**: Defines the specifications for the launcher and worker pods. The launcher initiates the job, while workers perform the computations.

### Customizing the Job

To tailor the Khiops job to your specific needs, you can customize the MPI Job definition.

If you have built a **custom** Docker image that includes a Python script or other custom logic, replace the container image of the launcher with your custom image. **The workers will continue to use the standard Khiops image** (`khiopsml/khiops-ubuntu`), as they function as pure Khiops slaves.

Example:

```yaml
mpiReplicaSpecs:
  Launcher:
    template:
      spec:
        containers:
        - image: my-custom-khiops-python-image
          name: mpi-launcher
          args:
          - python
          - my_script.py
```

If your job needs to access data stored in cloud storage solutions like Amazon S3, you can provide the necessary credentials in two ways: 

- Environment Variables: Pass the credentials as environment variables in the job definition.
- Mounted Volume: Mount a volume containing the standard AWS configuration files (config and credentials) to the pods.


### Launching the Job

Save the manifest to a file (e.g., `khiops_job.yaml`) and apply it to your Kubernetes cluster:

```bash
kubectl apply -f khiops_job.yaml
```

The MPI Operator will handle launching the pods and interconnecting them. Once ready, the launcher will start the execution, and you can monitor the job's progress using Kubernetes tools like `kubectl get pods` or `kubectl logs`.

## Conclusion

Running Khiops on Kubernetes with the MPI Operator allows you to leverage the power of distributed computing for large-scale data processing tasks. This setup ensures that your Khiops jobs are scalable, efficient, and integrated seamlessly into your Kubernetes workflows.
