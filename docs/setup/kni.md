# The Khiops Native Interface

The purpose of the Khiops Native Interface (or KNI) is to allow a deeper integration of Khiops in information systems, by mean of the C programming language, using a shared library (.dll in Windows, .so in Linux). This relates specially to the problem of model deployment, which otherwise requires the use of input and output data files when using directly the Khiops tool in batch mode. See [**Khiops Guide**][Documentation] for an introduction to dictionary files, dictionaries, database files and deployment.

[Documentation]: KhiopsGuide.pdf

The Khiops deployment API is thus made public through a shared library. Therefore, a Khiops model can be deployed directly from any programming language, such as C, C++, Java, Python, Matlab, etc. This enables real time model deployment without the overhead of temporary data files or launching executables. This is critical for certain applications, such as marketing or targeted advertising on the web.

All the basics to install and use the Khiops Native Interface is available at this [github project](https://github.com/KhiopsML/KNI-tutorial).