---
hide:
  - toc
---
<!-- Transform the pre-release version for the Rocky package
{% set ROCKY_KHIOPS_VERSION = KHIOPS_VERSION.replace("-", "_") %}
-->

# Installation Options {label="Overview"}

Khiops supports a diversified set of installation options, to meet different needs:

  - **Khiops Python Library**:
    - Packaged via [`pip`][pip_page] (recommended)
    - Packaged via [`conda`][conda_page] 
    - Packaged in our [khiops-notebook][notebooks_page] container
  - **Applications**:
    - [**Khiops Application**][nocode] for advanced data analytics with just a few clicks using a graphical user interface. This application is also the basis for easy integration into different systems (all programming languages, docker, servers, etc.).
    - [**Khiops Visualization**][vis]: for intuitive visualization of all analysis results (**interactive demo available [here][demo-vis]**)
    - [**Khiops Native Interface (KNI)**][kni]: to deploy Khiops models with a lightweight shared library.
  - **Cloud storage drivers** 
    - [**Cloud-ready Khiops Python library**](drivers-and-sdk-for-library.md)
    - [**Khiops application**](drivers-and-sdk-for-application.md)

!!! success "Supported Platforms"

    The following platforms are fully tested:

    - Windows 10 or later
    - Ubuntu 20.04, 22.04, 24.04, and 26.04 LTS (on both x86-64 & ARM architectures)
    - Debian 11, 12, and 13
    - Rocky Linux 8, 9, and 10
    - macOS 13 or later on ARM (only via the Khiops Python library).

    For other platforms, please :material-send: **[Contact Us][contact]**.

      [conda_page]: conda.md
      [pip_page]: pip.md
      [notebooks_page]: khiops-notebook.md
      [nocode]: nocode.md
      [vis]: visualization.md
      [demo-vis]: demovisualization.md
      [contact]: ../contact.md
      [kni]: kni.md

