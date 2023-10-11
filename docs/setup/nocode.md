# Khiops Desktop (No Code)

## Simplifying Data Science for Everyone

Welcome to the Khiops Desktop Application download page. Our intuitive, user-friendly desktop interface is designed for those who may not be familiar with Python or scikit-learn, as well as for users who prefer the convenience of a Graphical User Interface (GUI) for data manipulation. With Khiops Desktop, advanced data analytics is now just a few clicks away.

<img style="max-width:400px;width: -webkit-fill-available;" src="/assets/images/feature_eng_pane.png" ;></img>


<img style="max-width:400px;width: -webkit-fill-available;" src="/assets/images/database_pane.png" ;></img>

## Documentation
For a comprehensive guide on how to use the Khiops Desktop Application, please download our [**PDF Documentation**][Documentation]. 

The users already familiar with the CoClustering approach will find the dedicated documentation [**here**][coclustering].

[Documentation]: KhiopsGuide.pdf
[coclustering]: KhiopsCoclusteringGuide.pdf

A tutorial is also [**available**][tutorial] to help you understand and grasp the tool.

[tutorial]: KhiopsTutorial.pdf

!!! info "For users on Khiops versions prior to 10.1, the license support is available via [khiops.tech.orange][khiopslegacy]"

[khiopslegacy]: https://khiops.tech.orange

## Download & Installation

To get started with the Khiops Desktop Application, follow the procedure appropriate for your operating system. The links to the latest binaries are provided below, but you can find the all versions on the [releases page][releases].

[releases]: https://github.com/KhiopsML/khiops/releases

Please click on the relevant operating system:
=== "Windows"
    On Windows, the Khiops installer automatically installs the visualization application, but you may also install it without the main application, to only analyze Khiops reports.

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-setup.exe">
        <button class="btn btn-light btn-sm">
          Download for Windows
        </button>
    </a>

    The Khiops Native Interface, a dynamic library for online deployment of models, is available here:

    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/KNI.10.1.1-windows.zip">
        <button class="btn btn-light btn-sm">
        Download KNI for Windows
        </button>
    </a>

=== "Ubuntu"
    On Linux, Khiops is available in three packages:

    - `khiops-core`: This is a lightweight package without GUI, documentation or samples. It is intended to be used on servers and dockers images.
    - `khiops`: This package requires khiops-core and is the full version of Khiops containing the GUI, the documentation.
    - `khiops-samples`: This package contains examples data for Khiops.

    If you download and install the packages manually you first need to remove the old khiops and install packages in the right order: first khiops-core and then khiops.
    ``` sh
    sudo apt remove -y khiops-core khiops # Only if Khiops is already installed
    sudo dpkg -i khiops-core_10.1.1-0+jammy_amd64.deb
    sudo dpkg -i khiops-samples_10.1.1-0+jammy_all.deb
    sudo dpkg -i khiops_10.1.1-0+jammy_amd64.deb
    sudo apt-get -f install # Don't forget this line !!!
    ```

    **Downloads for Ubuntu 22.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+jammy_amd64.deb">
        <button class="btn btn-light btn-sm">
        Khiops-core
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops_10.1.1-0+jammy_amd64.deb">
        <button class="btn btn-light btn-sm">
          Khiops
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples_10.1.1-0+jammy_all.deb">
        <button class="btn btn-light btn-sm">
          Khiops-samples
        </button>
    </a>

    **Downloads for Ubuntu 20.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+focal_amd64.deb">
        <button class="btn btn-light btn-sm">
        Khiops-core
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops_10.1.1-0+focal_amd64.deb">
        <button class="btn btn-light btn-sm">
          Khiops
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples_10.1.1-0+focal_all.deb">
        <button class="btn btn-light btn-sm">
          Khiops-samples
        </button>
    </a>

    **Downloads for Ubuntu 18.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core_10.1.1-0+bionic_amd64.deb">
        <button class="btn btn-light btn-sm">
        Khiops-core
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops_10.1.1-0+bionic_amd64.deb">
        <button class="btn btn-light btn-sm">
          Khiops
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples_10.1.1-0+bionic_all.deb">
        <button class="btn btn-light btn-sm">
          Khiops-samples
        </button>
    </a>

    The Khiops Native Interface, a dynamic library for online deployment of models, is available in two packages:

    - kni: This packages contains only the header and the shared library of the Khiops Native Interface.
    - kni-doc: This package contains the documentation and samples.

    **Downloads for Ubuntu 22.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni_10.1.1-0+jammy_amd64.deb">
        <button class="btn btn-light btn-sm">
        kni
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-doc_10.1.1-0+jammy_all.deb">
        <button class="btn btn-light btn-sm">
          kni-doc
        </button>
    </a>

    **Downloads for Ubuntu 20.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni_10.1.1-0+focal_amd64.deb">
        <button class="btn btn-light btn-sm">
        kni
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-doc_10.1.1-0+focal_all.deb">
        <button class="btn btn-light btn-sm">
          kni-doc
        </button>
    </a>

    **Downloads for Ubuntu 18.04:**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni_10.1.1-0+bionic_amd64.deb">
        <button class="btn btn-light btn-sm">
        kni
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-doc_10.1.1-0+bionic_all.deb">
        <button class="btn btn-light btn-sm">
          kni-doc
        </button>
    </a>




=== "CentOS"
    On Linux, Khiops is available in three packages:

    - `khiops-core`: This is a lightweight package without GUI, documentation or samples. It is intended to be used on servers and dockers images.
    - `khiops`: This package requires khiops-core and is the full version of Khiops containing the GUI, the documentation.
    - `khiops-samples`: This package contains examples data for Khiops.

    If you download and install the packages manually you first need to remove the old khiops and install packages in the right order: first khiops-core and then khiops.
    ``` sh
    sudo yum remove -y khiops-core khiops # Only if Khiops is already installed
    sudo yum localinstall khiops-core-10.1.1-1.el7.x86_64.rpm
    sudo yum localinstall khiops-samples-10.1.1-1.el7.x86_64.rpm
    sudo yum localinstall khiops-10.1.1-1.el7.x86_64.rpm
    ```

    **Downloads for CentOS el8**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el8.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops-core
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-1.el8.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples-10.1.1-1.el8.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops-samples
        </button>
    </a>

    **Downloads for CentOS el7**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-core-10.1.1-1.el7.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops-core
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-10.1.1-1.el7.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/khiops-samples-10.1.1-1.el7.x86_64.rpm">
        <button class="btn btn-light btn-sm">
          khiops-samples
        </button>
    </a>

    The Khiops Native Interface, a dynamic library for online deployment of models, is available in two packages:

    - kni: This packages contains only the header and the shared library of the Khiops Native Interface.
    - kni-doc: This package contains the documentation and samples.

    **Downloads for CentOS el8**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-10.1.1-1.el8.x86_64.rpm">
        <button class="btn btn-light btn-sm">
        kni
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-doc-10.1.1-1.el8.noarch.rpm">
        <button class="btn btn-light btn-sm">
          kni-doc
        </button>
    </a>

    **Downloads for CentOS el7**
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-10.1.1-1.el7.x86_64.rpm">
        <button class="btn btn-light btn-sm">
        kni
        </button>
    </a>
    <a href="https://github.com/KhiopsML/khiops/releases/download/v10.1.1/kni-doc-10.1.1-1.el7.noarch.rpm">
        <button class="btn btn-light btn-sm">
          kni-doc
        </button>
    </a>


