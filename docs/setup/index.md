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
    - Packaged via [`conda`][conda_page] (recommended)
    - Packaged via [`pip`][pip_page]
    - Packaged in our [khiops-notebook][notebooks_page] container
  - [**Khiops Application**][nocode]: for advanced data analytics with just a few clicks using a graphical user interface. This application is also the basis for easy integration into different systems (all programming languages, docker, servers, etc.).
  - [**Khiops Visualization Application**][vis]: for intuitive visualization of all analysis results (**interactive demo available [here][demo-vis]**)
  - [**Khiops Native Interface (KNI)**][kni]: to deploy Khiops models with a lightweight shared library.

!!! warning "Supported Platforms"
    We support :simple-python: **Python from 3.8 to 3.13** and the following operating systems:

    - Windows 10 or later
    - Ubuntu 20, 22 and 24 (LTS)
    - Debian 10, 11 and 12
    - Rocky Linux 8 and 9
    - macOS 12 or later, only via :simple-anaconda: **Conda**. Full support for macOS 13 or later on ARM architectures, limited support for macOS 12 or for x86-64 architectures.

    The :simple-googlecolab: **Google Colaboratory** environments are supported. To benefit from Khiops on these environments, users are encouraged to install the Khiops :simple-anaconda:**Conda** package, which has been tested in these environments.

    For other platforms, please :material-send: **[Contact Us][contact]**.

      [conda_page]: conda.md
      [pip_page]: pip.md
      [notebooks_page]: khiops-notebook.md
      [nocode]: nocode.md
      [vis]: visualization.md
      [demo-vis]: demovisualization.md
      [contact]: ../contact.md
      [kni]: kni.md

