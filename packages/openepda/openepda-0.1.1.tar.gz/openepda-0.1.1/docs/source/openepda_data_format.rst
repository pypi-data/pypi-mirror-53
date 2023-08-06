.. _opendpda_data_format:

openEPDA data format
====================

About openEPDA data format
--------------------------

Summary
~~~~~~~
With the development of fab-less approach to integrated photonics, there is
an increasing demand on infrastructure for handling measurement, analysis
and simulation data. In order to facilitate data exchange between parties we
fill the gap in the data file formats and describe an open standard for
file format, which is human readable and at the same time allows convenient
storage and manipulation of heterogeneous measurement data.

Motivation
~~~~~~~~~~
In integrated electronics and photonics various data in different
formats is generated on multiple stages of the fabrication chain:
design, simulations, fabrication, testing, and device characterization.
For example, testing is performed on different stages of the fabrication:
from on-wafer testing during and after the fabrication to module-level
testing of the packaged devices. The data generated during these measurements is
heterogeneous, and is used for different purposes: pass-fail procedure,
process control, device models development and calibration. This involves
various parties, such as foundry, measurement labs, designers, and software
companies which use different tools to generate and process the test data.

Data types
~~~~~~~~~~
The generated data comes from different sources and is heterogeneous.
The main data is obtained from the measurement equipment directly when
the observation is performed. This data is usually numeric (scalar or arrays).
The identifiers of the wafer, die and circuit under test represent metadata
for the given observation. Metadata also may include the equipment used,
the equipment settings, date of calibration, ambient conditions, etc.
The metadata can be of various simple (numeric, textual) and structured
types (arrays, maps). The overview of the datatypes is presented in the
table below.

+-----------+-----------------------------+---------------------------------+------------------------------+
| Data type | Description                 | Examples                        | Remarks                      |
+===========+=============================+=================================+==============================+
| Number    | Any numeric value           | 1                               | Representation is same       |
|           |                             | 2.3                             | as in section 10.2.1.4       |
|           |                             | .inf                            | of [1]                       |
|           |                             | 1.9e-3                          |                              |
+-----------+-----------------------------+---------------------------------+------------------------------+
|           | A list of characters        | 'spectrum analyzer'             |                              |
| String    |                             | 'SPM18-3'                       |                              |
+-----------+-----------------------------+---------------------------------+------------------------------+
| Array     | A sorted list of numeric    | [1, 2, 3, 4]                    | Values may have mixed types, |
|           | or string values            | ['voltage', 'current', 'power'] | which is discouraged         |
+-----------+-----------------------------+---------------------------------+------------------------------+
| Map       | Mapping of a set of values  |  {'wafer': 'SPM18-3',           | Also called a named array,   |
|           | to another set of values    |  'die': '38X23',                | a look-up table, or a        |
|           | in the ``key: value`` form  |  'design': 'SP00-38'}           | dictionary                   |
+-----------+-----------------------------+---------------------------------+------------------------------+

To facilitate exchange of the data between these parties, we have developed
a standard file data format, which can store the measurement data and metadata
in a human-readable way. The format is sufficiently flexible to include any
arbitrary structured data, including arrays and maps. The generated files are
straightforward to be imported by any software or analysis tool, for example
MatLab, python, and Excel.

Specification
-------------
The data format defines how to write the information into a file. Besides
this, YAML section contains reserved keys which start with the underscore
symbol. The list of particular keys is given for a particular format version.

Version 0.1
~~~~~~~~~~~
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA DATA FORMAT v0.1``. After
this, the data part follows, which contains two sections. The first section
adheres to the YAML format [1], and contains all scalar (numeric and textual)
data in the name: value form. This format is applicable for storing all
previously mentioned types of the data. The second section is a CSV-formatted
[2] part to store the tabular measurement data.

An example of a file recorded in the openEPDA data format is shown below.
Line 1 specifies the file format and its version. Lines 2 to 16 contain
metadata in YAML-format. Here, only string and float data types are used,
however arrays and maps can also be included. Line 17 contains a standard
document-end marker. Lines 18 to the end of the document contain the
CSV-formatted tabular data with a single header line.

Reserved keys
^^^^^^^^^^^^^
The following keys have a special meaning:

* ``_timestamp``: time the data was created in ISO format.

+-------------+----------------------------------------------------+
| Line number | File contents                                      |
+=============+====================================================+
|           1 | # openEPDA DATA FORMAT v.0.1                       |
+-------------+----------------------------------------------------+
|           2 | _timestamp: '2018-09-12T09:59:19.310182'           |
+-------------+----------------------------------------------------+
|           3 | project: OpenPICs                                  |
+-------------+----------------------------------------------------+
|           4 | setup: RF setup                                    |
+-------------+----------------------------------------------------+
|           5 | operator: Xaveer                                   |
+-------------+----------------------------------------------------+
|           6 | wafer: 36386X                                      |
+-------------+----------------------------------------------------+
|           7 | sample: 13L8                                       |
+-------------+----------------------------------------------------+
|           8 | cell: SP35-1-3                                     |
+-------------+----------------------------------------------------+
|           9 | circuit: MSSOA1-6                                  |
+-------------+----------------------------------------------------+
|          10 | "current_density, kA/cm**2": 1                     |
+-------------+----------------------------------------------------+
|          11 | "reverse_bias, V": -2                              |
+-------------+----------------------------------------------------+
|          12 | configuration: 1                                   |
+-------------+----------------------------------------------------+
|          13 | polarization: TE                                   |
+-------------+----------------------------------------------------+
|          14 | port: "ioE132"                                     |
+-------------+----------------------------------------------------+
|          15 | "chip_temperature, degC": 18                       |
+-------------+----------------------------------------------------+
|          16 | "water_temperature, degC": 14                      |
+-------------+----------------------------------------------------+
|          17 | ...                                                |
+-------------+----------------------------------------------------+
|          18 | "wavelength, nm","transmitted power, dBm"          |
+-------------+----------------------------------------------------+
|          19 | 1550.00000000000000e+00,-21.000000000000000000e+00 |
+-------------+----------------------------------------------------+
|          20 | 1551.00000000000000e+00,-22.000000000000000000e+00 |
+-------------+----------------------------------------------------+

Version 0.2
~~~~~~~~~~~
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA DATA FORMAT``. After
this, the data part follows, which contains two sections. The first section
adheres to the YAML format [1], and contains all scalar (numeric and textual)
data in the name: value form. This format is applicable for storing all
previously mentioned types of the data. The second section is a CSV-formatted
[2] part to store the tabular measurement data.

An example of a file recorded in the openEPDA data format is shown below.
Line 1 specifies the file format. Lines 2 to 16 contain
metadata in YAML-format, including the values for two reserved keys.
Here, only string and float data types are used, however arrays and maps can
also be included. Line 18 contains a standard document-end marker.
Lines 19 to the end of the document contain the CSV-formatted tabular data
with a single header line.

Reserved keys
^^^^^^^^^^^^^
The following keys have a special meaning:

* ``_timestamp``: time the data was created in ISO format.
* ``_openEPDA_version``: string defining the format version, e.g. ``'0.2'``

+-------------+----------------------------------------------------+
| Line number | File contents                                      |
+=============+====================================================+
|           1 | ``# openEPDA DATA FORMAT``                         |
+-------------+----------------------------------------------------+
|           2 | ``_timestamp: '2018-09-12T09:59:19.310182'``       |
+-------------+----------------------------------------------------+
|           3 | ``_openEPDA_version: '0.2'``                       |
+-------------+----------------------------------------------------+
|           4 | ``project: OpenPICs``                              |
+-------------+----------------------------------------------------+
|           5 | ``setup: RF setup``                                |
+-------------+----------------------------------------------------+
|           6 | ``operator: Xaveer``                               |
+-------------+----------------------------------------------------+
|           7 | ``wafer: 36386X``                                  |
+-------------+----------------------------------------------------+
|           8 | ``sample: 13L8``                                   |
+-------------+----------------------------------------------------+
|           9 | ``cell: SP35-1-3``                                 |
+-------------+----------------------------------------------------+
|          10 | ``circuit: MSSOA1-6``                              |
+-------------+----------------------------------------------------+
|          11 | ``'current_density, kA/cm**2': 1``                 |
+-------------+----------------------------------------------------+
|          12 | ``'reverse_bias, V': -2``                          |
+-------------+----------------------------------------------------+
|          13 | ``configuration: 1``                               |
+-------------+----------------------------------------------------+
|          14 | ``polarization: TE``                               |
+-------------+----------------------------------------------------+
|          15 | ``port: 'ioE132'``                                 |
+-------------+----------------------------------------------------+
|          16 | ``'chip_temperature, degC': 18``                   |
+-------------+----------------------------------------------------+
|          17 | ``'water_temperature, degC': 14``                  |
+-------------+----------------------------------------------------+
|          18 | ``...``                                            |
+-------------+----------------------------------------------------+
|          19 | ``"wavelength, nm","transmitted power, dBm"``      |
+-------------+----------------------------------------------------+
|          20 | ``1550.0000000000000e+00,-21.000000000000000e+00`` |
+-------------+----------------------------------------------------+
|          21 | ``1551.0000000000000e+00,-22.000000000000000e+00`` |
+-------------+----------------------------------------------------+

License
-------
openEPDA data formats are available under CC BY-ND 4.0 license.

This is Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). See full license text here:
`CC BY-ND 4.0 <https://creativecommons.org/licenses/by-nd/4.0/legalcode>`_.

References
----------
1. "YAML Ain't Markup Language (YAML™) Version 1.2."
`<http://yaml.org/spec/1.2/spec.html>`_.

2. RFC 4180, "Common Format and MIME Type for Comma-Separated Values
(CSV) Files." `<https://tools.ietf.org/html/rfc4180>`_.