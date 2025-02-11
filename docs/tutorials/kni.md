# Real-Time Deployment with KNI

The **Khiops Native Interface (KNI)** is a lightweight dynamically-linked library (DLL) that provides an ANSI C interface which enables the seamless integration the seamless integration of Khiops models directly into your applications. Unlike the standalone Khiops executable, KNI facilitates direct in-memory model inference, eliminating the need for temporary files or external calls.

Its key features include:

- **Real-Time Scoring**: KNI allows you to apply trained Khiops models directly within your application, providing low-latency predictions ideal for real-time applications.
- **Batch Processing**: While optimized for real-time use, KNI also efficiently handles batch processing, offering versatility for various deployment scenarios.
- **Lightweight and Fast**: Written in optimized C++, KNI is designed to run with minimal computational overhead, ensuring speed and efficiency.
- **Multi-Language Support**: KNI can be integrated into applications written in C, C++, Java, Python, and even Matlab, making it adaptable to diverse development environments.

## Getting Started with KNI

The KNI is targeted primarily at system integrators which aim to deploy the scoring capabilities of Khiops in native Windows and Linux environments. KNI can also be used in Conda environments on Windows, Linux and MacOS.

### Installation

=== "Windows"
    There are two steps for installing KNI on Windows:

    1. **Download KNI**: Download the KNI package [`KNI-{{ KHIOPS_VERSION }}.zip`][kni-windows].
    
    2. **Set Environment Variable**: Set the environment variable `KNI_HOME` to the extracted directory. 

[kni-windows]: https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/KNI-{{ KHIOPS_VERSION }}.zip


=== "Ubuntu / Debian"
    You can install KNI as follows:

    ``` sh
    CODENAME=$(lsb_release -cs) && \
    TEMP_DEB_KNI="$(mktemp)" && \
    wget -O "$TEMP_DEB_KNI" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/kni_{{ KHIOPS_VERSION }}-1-${CODENAME}.amd64.deb" && \
    sudo dpkg -i "$TEMP_DEB_KNI" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_KNI 
    ```

=== "Rocky Linux"
    You can install KNI as follow::

    ``` sh
    sudo yum update -y && sudo yum install wget python3-pip -y && \
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM_KNI="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM_KNI" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/kni-{{ ROCKY_KHIOPS_VERSION }}-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM_KNI" -y && \
    rm -f $TEMP_RPM_KNI
    ```

=== "conda"

    ```sh
    conda install -c khiops kni
    ```

You can find the all versions on the [releases page][releases].

[releases]: https://github.com/KhiopsML/khiops/releases


## Example Application in C

This example demonstrates how to compile and run a C program (`KNIRecodeFile`) that applies Khiops native recoding process using the shared library. The `KNIRecodeFile` binary is a standalone executable that directly processes input data using a Khiops [dictionary][dico], transforming raw features into recoded (scored) outputs.

[dico]: kdic_intro.md

The following example shows how to use KNI in C, on Linux, for a **single-table case**. If you need to apply KNI in a multi-table scenario or on a different operating system, refer to the [KNI-tutorial][KNI-tutorial-repo] repository for additional implementations in Python, Java, and Matlab.

[KNI-tutorial-repo]: https://github.com/KhiopsML/KNI-tutorial?tab=readme-ov-file

### Building the Example

1. **Clone our tutorial repositoy**: Run the following `git clone` command:
    ```bash
    git clone https://github.com/KhiopsML/KNI-tutorial.git
    ```
2. **Navigate to the Example Directory**: Change to the directory containing the example files:
    ```bash
    cd KNI-tutorial/cpp/
    ```
3. **Compile the Example**: Run the following command to compile the `KNIRecodeFile` application:
   ```bash
   gcc -o KNIRecodeFile cpp/KNIRecodeFile.c -I /usr/include/ -lKhiopsNativeInterface -ldl
   ```

### Running the Example

Once compiled, you can run the `KNIRecodeFile` application to recode a dataset. Here's how:

1. **Prepare Your Files**: Ensure you have the following files:
  
    - A Khiops dictionary file (e.g., `ModelingIris.kdic`);
    - An input data file (e.g., `Iris.txt`).

2. **Run the Application**: Use the following command to recode the input file: 
   ```bash
   KNIRecodeFile data/ModelingIris.kdic SNB_Iris data/Iris.txt R_Iris.txt
   ```
    using the following inputs:

    - `data/ModelingIris.kdic`: The [dictionary][dico] file that describes both the data transformation process and the trained model;
    - `SNB_Iris`: The name of the dictionary within the [dictionary][dico] file;
    - `data/Iris.txt`: The input data file containing the data to be recoded;
    - `R_Iris.txt`: The output file where the recoded (scored) data will be saved.

### Understanding the Output

The output file (`R_Iris.txt`) will contain the recoded data, which includes the scores or predictions generated by the Khiops model as described in the [dictionary][dico] file. This process allows you to integrate Khiops' powerful data transformation capabilities directly into your applications, enabling real-time scoring and efficient batch processing.

## Conclusion

KNI provides a powerful and flexible solution for real-time deployment of Khiops models. Its efficiency, versatility, and ease of integration make it an ideal choice for developers and integrators looking to enhance their data science workflows with real-time scoring capabilities. By leveraging KNI, you can ensure that your applications are responsive, efficient, and capable of handling complex data processing tasks in real-time. Additionally, KNI can be used in conjunction with Khiops [drivers][drivers] to seamlessly access and process data stored in cloud storage solutions, further enhancing its utility in diverse deployment scenarios.

[drivers]: ./storage.md
