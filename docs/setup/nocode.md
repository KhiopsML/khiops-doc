<!-- Transform the pre-release version for the Rocky package
{% set ROCKY_KHIOPS_VERSION = KHIOPS_VERSION.replace("-", "_") %}
-->
# The Khiops Application (No-Code Environment)

## Simplifying Data Science for Everyone

Our intuitive, user-friendly desktop interface is designed for people who may not be familiar with Python or scikit-learn, as well as for users who prefer the convenience of a standalone graphical user interface (GUI) for data manipulation. With the Khiops application, advanced data analytics is just a few clicks away, along with easy system integration.


## Download & Installation

To get started with the Khiops application, follow the procedure for your operating system.
For further details, refer to [README][readme] and [WHATSNEW][whatsnew].

=== "Windows"
    The :material-microsoft-windows: Khiops installer automatically installs the Khiops application, all its dependencies, plus some data samples formatted as expected by Khiops, and the Khiops Visualization application.

    <a href="https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-{{ KHIOPS_VERSION }}-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

=== "Ubuntu / Debian (ARM and x86)"
    Installing the Khiops desktop application involves two packages:

    - `khiops-core`: This is a lightweight package without a GUI, documentation, or samples. It is intended for advanced settings, servers, and Docker images.
    - `khiops`: This package requires `khiops-core` and is the full version of Khiops, containing the GUI and documentation.

    Unlike the Windows installer, **the Khiops Visualization application is not included.**

    Install both packages as follows:

    ``` sh
    sudo apt-get update -y && sudo apt-get install wget -y && \
    source /etc/os-release && \
    ARCH=$(dpkg --print-architecture) && \
    TEMP_DEB_CORE="$(mktemp)" && \
    TEMP_DEB_KHIOPS="$(mktemp)" && \
    wget -O "$TEMP_DEB_CORE" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-core-openmpi_{{ KHIOPS_VERSION }}-1-${VERSION_CODENAME}.${ARCH}.deb" && \
    wget -O "$TEMP_DEB_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops_{{ KHIOPS_VERSION }}-1-${VERSION_CODENAME}.${ARCH}.deb" && \
    sudo dpkg -i "$TEMP_DEB_CORE" "$TEMP_DEB_KHIOPS" || sudo apt-get -f -y install && \
    rm -f $TEMP_DEB_CORE $TEMP_DEB_KHIOPS
    ```

    If you need the Khiops samples, you can download them from
    <a href="https://github.com/KhiopsML/khiops-samples/releases/download/{{ KHIOPS_SAMPLES_VERSION }}/khiops-samples-{{ KHIOPS_SAMPLES_VERSION }}.zip        ">
    here</a>, or run the following commands:
    ```sh
    TEMP_SAMPLES="$(mktemp)" && \
    wget -O "$TEMP_SAMPLES" "https://github.com/KhiopsML/khiops-samples/releases/download/{{ KHIOPS_SAMPLES_VERSION }}/khiops-samples-{{ KHIOPS_SAMPLES_VERSION }}.zip" && \
    mkdir -p ~/khiops_data/samples && \
    unzip "$TEMP_SAMPLES" -d ~/khiops_data/samples && \
    rm -f $TEMP_SAMPLES
    ```

=== "Rocky Linux"
    Installing the Khiops desktop application involves two packages:

    - `khiops-core`: This is a lightweight package without a GUI, documentation, or samples. It is intended for advanced settings, servers, and Docker images.
    - `khiops`: This package requires `khiops-core` and is the full version of Khiops, containing the GUI and documentation.

    Unlike the Windows installer, **the Khiops Visualization application is not included.**

    Install both packages as follows:

    ``` sh
    sudo yum update -y && sudo yum install wget python3-pip -y && \
    CENTOS_VERSION=$(rpm -E %{rhel}) && \
    TEMP_RPM="$(mktemp).rpm" && \
    TEMP_RPM_KHIOPS="$(mktemp).rpm" && \
    wget -O "$TEMP_RPM" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-core-openmpi-{{ ROCKY_KHIOPS_VERSION }}-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    wget -O "$TEMP_RPM_KHIOPS" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-{{ ROCKY_KHIOPS_VERSION }}-1.el${CENTOS_VERSION}.x86_64.rpm" && \
    sudo yum install "$TEMP_RPM" "$TEMP_RPM_KHIOPS" -y && \
    rm -f $TEMP_RPM $TEMP_RPM_KHIOPS
    ```

    If you need the Khiops samples, you can download them from
    <a href="https://github.com/KhiopsML/khiops-samples/releases/download/{{ KHIOPS_SAMPLES_VERSION }}/khiops-samples-{{ KHIOPS_SAMPLES_VERSION }}.zip        ">
    here</a>, or run the following commands:
    ```sh
    TEMP_SAMPLES="$(mktemp)" && \
    wget -O "$TEMP_SAMPLES" "https://github.com/KhiopsML/khiops-samples/releases/download/{{ KHIOPS_SAMPLES_VERSION }}/khiops-samples-{{ KHIOPS_SAMPLES_VERSION }}.zip" && \
    mkdir -p ~/khiops_data/samples && \
    unzip "$TEMP_SAMPLES" -d ~/khiops_data/samples && \
    rm -f $TEMP_SAMPLES
    ```

=== "macOS" 
    Khiops with its graphical user interface is not natively available on macOS. However, you can run it using Docker containers with X11 forwarding to display the GUI on your Mac.

    **Note:** Khiops Visualization must be installed separately and directly on macOS. Follow this [link][vis] to download the DMG installers.

    ### Prerequisites

    The following software is required to run Khiops on macOS:

    - **[Homebrew](https://brew.sh)**: Package manager for macOS. Used to install other dependencies.
    - **[Docker Client](https://docs.docker.com/desktop/setup/install/mac-install/)**: Docker client tools for container management.
    - **[Colima](https://github.com/abiosoft/colima)**: Lightweight container runtime that provides a Docker-compatible environment without requiring Docker Desktop.
    - **[XQuartz](https://www.xquartz.org)**: X Window System for macOS. Required to display the Khiops GUI from the Docker container.

    ### Step 1: Install Prerequisites

    First, install Homebrew if you don't have it already. Open Terminal and run:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    Then use Homebrew to install Docker, Colima, and XQuartz:

    ```bash
    brew install docker colima xquartz
    ```

    ### Step 2: Download Launch Scripts

    Download the launch scripts that automate the setup and execution of Khiops:

    - [khiops](./khiops) - Launch script for Khiops
    - [khiops_coclustering](./khiops-coclustering) - Launch script for Khiops Coclustering

    Save these scripts to a convenient location (e.g., your home directory or a dedicated folder).

    ### Step 3: Make Scripts Executable

    Open Terminal, navigate to the directory where you saved the scripts, and make them executable:

    ```bash
    chmod +x khiops khiops_coclustering
    ```

    ### Step 4: Launch Khiops

    **From Terminal:**

    Navigate to the directory containing the scripts and run:

    ```bash
    ./khiops
    ```

    For Khiops Coclustering:

    ```bash
    ./khiops_coclustering
    ```

    **From Finder:**

    You can also double-click on the `khiops` or `khiops_coclustering` scripts in Finder to launch them.

    ### What Happens When You Launch

    The launch scripts automatically handle the following:

    1. Verify that all prerequisites are installed
    2. Configure XQuartz to allow network connections
    3. Start XQuartz if not already running
    4. Start Colima (allocating all available CPU cores and memory)
    5. Pull the Khiops Docker image (first run only)
    6. Launch Khiops with the GUI displayed through XQuartz

    ### Important Notes

    !!! note "Working Directory and Temporary Files"
        Khiops starts in your macOS `$HOME` directory and has full access to your home folder. Temporary files are stored in the macOS temporary directory (`/tmp`).

    !!! note "First Launch"
        The first time you run Khiops, Colima will download the Docker image, which may take a few minutes depending on your internet connection.

    !!! warning "Display Issue"
        The log window may appear completely black on first launch. If this happens, simply resize the window to refresh its display.

    !!! warning "X11 Network Access"
        During Khiops execution, bidirectional X11 connections are enabled between your host machine and the Khiops container (`xhost +localhost`). This allows the container to display the GUI on your host. These connections are automatically revoked when Khiops exits. For security-sensitive environments, be aware of this temporary network access during execution.

    !!! tip "Resource Allocation"
        The scripts automatically allocate all available CPU cores and memory to Khiops for optimal performance. If you need to limit resources, you can modify the `colima start` command in the scripts.


You can find all versions on the [releases page][releases].

## Documentation

For comprehensive guides on using the Khiops application and its GUI:

- [**Khiops Guide**][khiops-guide], for supervised analysis
- [**Khiops Coclustering Guide**][coclustering-guide], for unsupervised analysis



## What You Should Know

You can consult the limitations and known issues for your operating system:

=== "Users on :material-microsoft-windows: Windows"
    !!! warning
        The Khiops installer relies on embedded installers for Java and MPI. Antivirus software may remove executable files (.exe, .jar) during installation. In this case, **you should add exceptions to your antivirus software or disable it during installation.**
    !!! warning
        On some machines, reinstalling Khiops may unexpectedly discard the existing Khiops installation directory. In that case, uninstall Khiops before reinstalling it.
    !!! warning
        In some companies, programs are blocked by the Windows AppLocker group policy. In this case, install Khiops in a recommended directory or run it as administrator.

## Screenshots

<div class="text-center">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/feature_eng_pane.png">
    <img style="max-width:400px; width: -webkit-fill-available; display: inline-block;" src="/assets/images/database_pane.png">
</div>


[vis]: visualization.md
[khiops-guide]: ../ui-docs/khiops.md
[coclustering-guide]: ../ui-docs/coclustering.md
[releases]: https://github.com/KhiopsML/khiops/releases
[readme]: https://raw.githubusercontent.com/KhiopsML/khiops/refs/tags/{{ KHIOPS_VERSION }}/packaging/common/khiops/README.txt
[whatsnew]: https://raw.githubusercontent.com/KhiopsML/khiops/refs/tags/{{ KHIOPS_VERSION }}/packaging/common/khiops/WHATSNEW.txt