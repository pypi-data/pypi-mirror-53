.. _opendpda_cdf_format:

openEPDA CDF format (Draft)
===========================

Summary
~~~~~~~
This document contains draft description of the Chip Description File
(CDF), which is used as a reference for electrical pads and optical
ports positions for the measurements to be performed on Photonic
Integrated Circuits (PIC).

Introduction
~~~~~~~~~~~~
CDF is a configuration file that contains data with design coordinates
of the chip inputs and outputs (IO) (both electrical and optical). Therefore
it is linked to a specific design (cell), meaning that for
every new die design, also the applicable CDF needs to be composed.

Being a YAML file, its content is human readable and intuitive in its structure.
It provides all necessary information starting from cell design identification
data, which is to be crosschecked with other configuration files (e.g. MDF),
up to the IO coordinates themselves. More details regarding YAML syntax can be
found here: https://yaml.org/spec/1.2/spec.html.

Specification
~~~~~~~~~~~~~
The data format defines how to write the information into a file. Besides
this, YAML section contains reserved keys which start with the underscore
symbol. The list of particular keys is given for a particular format version.

Version 0.2
-----------
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA CDF``. After
this, the data section follows, which adheres to the YAML format [1],
and contains all settings (numeric and textual) data in the form of an
associative array.

An example of a file recorded in the openEPDA CDF format is shown below.

Reserved keys
^^^^^^^^^^^^^
The following keys are required to be present in the CDF:

* ``_openEPDA``: an object defining the format and its version.
* ``cdf``: a string with a unique identifier of the CDF
* ``cell``: a string with an identifier of the PIC design to be measured
* ``unit``: a string defining a unit for the coordinates in the file
* ``io``: An object with IOs located on the chip.

The following keys are optional to be present in the CDF:

* ``fiducial``: an object with fiducial markers on the chip.


Example CDF file
^^^^^^^^^^^^^^^^

.. include:: cdf_v0.2_example.rst

License
~~~~~~~
openEPDA CDF format is available under CC BY-ND 4.0 license.

This is Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). See full license text here:
`CC BY-ND 4.0 <https://creativecommons.org/licenses/by-nd/4.0/legalcode>`_.

References
~~~~~~~~~~
1. "YAML Ain't Markup Language (YAML™) Version 1.2."
`<http://yaml.org/spec/1.2/spec.html>`_.
