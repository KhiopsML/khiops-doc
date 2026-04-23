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
    Khiops with its graphical user interface is not natively available on macOS.
    You can still run it with Docker. However, Khiops Visualization must be installed directly on macOS. Follow this [link][vis] to download the DMG installers.

    Install the following prerequisites first:

    - [Homebrew](https://brew.sh): package manager for macOS
    - [Colima](https://github.com/abiosoft/colima): lightweight alternative to Docker Desktop
    - [XQuartz](https://www.xquartz.org): X Window System required to display the Khiops GUI

    Then create two scripts named `khiops` and `khiops_coclustering` with the following content:

    === "khiops"
        ``` bash
        #!/bin/bash
    
        set -e

        APPLICATION=khiops

        # Check if Colima is installed
        if ! command -v colima &> /dev/null; then
            echo "Error: Colima is not installed. Please install it with: brew install colima"
            exit 1
        fi

        # Check brew dependency
        if ! command -v brew &> /dev/null; then
            echo "Error: brew is not installed. Please install it, go to: https://brew.sh"
            exit 1
        fi

        # Check XQuartz dependency
        if ! command -v Xquartz &> /dev/null; then
            echo "Error: XQuartz is not installed. Please install it with: brew install xquartz"
            exit 1
        fi

        # Check and configure XQuartz network connections property
        CURRENT_VALUE=$(defaults read org.xquartz.X11.plist nolisten_tcp 2>/dev/null || echo "not-set")

        if [[ "$CURRENT_VALUE" == "1" ||  "$CURRENT_VALUE" == "not-set" ]]; then
            echo "XQuartz network connections are disabled. Reconfiguring..."
            
            # Stop XQuartz if running
            if pgrep -q Xquartz; then
                echo "Stopping XQuartz..."
                killall Xquartz 2>/dev/null || true
                sleep 2
            fi
            
            # Set the property to allow network connections
            defaults write org.xquartz.X11.plist nolisten_tcp -bool false
            echo "XQuartz configured to allow network connections."
        fi

        # Start XQuartz if not already running
        if ! pgrep -q Xquartz; then
            # Start XQuartz
            open -a XQuartz
            sleep 3
        fi

        # If not already started, start Colima using host CPU and memory,
        # and a 5 GB disk (Khiops does not use the container disk heavily).
        if ! colima status &> /dev/null; then
            CPU_NUMBER=$(sysctl -n hw.ncpu)
            echo "Allocating $CPU_NUMBER CPU cores to Khiops."
            MEMORY_SIZE=$(sysctl -n hw.memsize | awk '{printf "%.0f", $1 / 1024 / 1024 / 1024}')
            echo "Allocating $MEMORY_SIZE GB of memory to Khiops."
            echo "Starting Colima..."
            colima start --cpu $CPU_NUMBER --memory $MEMORY_SIZE --disk 5
        fi

        # Allow local X11 connections
        xhost +localhost &> /dev/null

        # Run Khiops in Docker with GUI forwarding. It starts in the macOS $HOME directory 
        # and uses the macOS temporary directory for temporary files
        docker run \
            -e DISPLAY=host.docker.internal:0 \
            -e KHIOPS_TMP_DIR=/macos-tmp \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v "$HOME":/macos-home \
            -v /tmp:/macos-tmp \
            khiopsml/khiops-desktop:11 bash -c "cd /macos-home && $APPLICATION" 

        # Revoke access to X11 after Khiops exits
        xhost - &> /dev/null
        ```

    === "Khiops Coclustering"
        ``` bash
        #!/bin/bash
    
        set -e

        APPLICATION=khiops_coclustering

        # Check if Colima is installed
        if ! command -v colima &> /dev/null; then
            echo "Error: Colima is not installed. Please install it with: brew install colima"
            exit 1
        fi

        # Check brew dependency
        if ! command -v brew &> /dev/null; then
            echo "Error: brew is not installed. Please install it, go to: https://brew.sh"
            exit 1
        fi

        # Check XQuartz dependency
        if ! command -v Xquartz &> /dev/null; then
            echo "Error: XQuartz is not installed. Please install it with: brew install xquartz"
            exit 1
        fi

        # Check and configure XQuartz network connections property
        CURRENT_VALUE=$(defaults read org.xquartz.X11.plist nolisten_tcp 2>/dev/null || echo "not-set")

        if [[ "$CURRENT_VALUE" == "1" ||  "$CURRENT_VALUE" == "not-set" ]]; then
            echo "XQuartz network connections are disabled. Reconfiguring..."
            
            # Stop XQuartz if running
            if pgrep -q Xquartz; then
                echo "Stopping XQuartz..."
                killall Xquartz 2>/dev/null || true
                sleep 2
            fi
            
            # Set the property to allow network connections
            defaults write org.xquartz.X11.plist nolisten_tcp -bool false
            echo "XQuartz configured to allow network connections."
        fi

        # Start XQuartz if not already running
        if ! pgrep -q Xquartz; then
            # Start XQuartz
            open -a XQuartz
            sleep 3
        fi

        # If not already started, start Colima using host CPU and memory,
        # and a 5 GB disk (Khiops does not use the container disk heavily).
        if ! colima status &> /dev/null; then
            CPU_NUMBER=$(sysctl -n hw.ncpu)
            echo "Allocating $CPU_NUMBER CPU cores to Khiops."
            MEMORY_SIZE=$(sysctl -n hw.memsize | awk '{printf "%.0f", $1 / 1024 / 1024 / 1024}')
            echo "Allocating $MEMORY_SIZE GB of memory to Khiops."
            echo "Starting Colima..."
            colima start --cpu $CPU_NUMBER --memory $MEMORY_SIZE --disk 5
        fi

        # Allow local X11 connections
        xhost +localhost &> /dev/null

        # Run Khiops in Docker with GUI forwarding. It starts in the macOS $HOME directory 
        # and uses the macOS temporary directory for temporary files
        docker run \
            -e DISPLAY=host.docker.internal:0 \
            -e KHIOPS_TMP_DIR=/macos-tmp \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v "$HOME":/macos-home \
            -v /tmp:/macos-tmp \
            khiopsml/khiops-desktop:11 bash -c "cd /macos-home && $APPLICATION" 

        # Revoke access to X11 after Khiops exits
        xhost - &> /dev/null
        ```

    Make the script executable:
    ```bash
    chmod +x khiops khiops_coclustering
    ```

    You can then launch Khiops by running:
    ```bash
    ./khiops
    ```
    and Khiops Coclustering by running:
    ```bash
    ./khiops_coclustering
    ```

    You can also launch Khiops (or Khiops Coclustering) by double-clicking the corresponding script in Finder.
 
    !!! note "Khiops and Khiops Coclustering start in the macOS $HOME directory and use the macOS temporary directory for temporary files."
    !!! warning "The log window may appear completely black. If this happens, resize the window to refresh its display."


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