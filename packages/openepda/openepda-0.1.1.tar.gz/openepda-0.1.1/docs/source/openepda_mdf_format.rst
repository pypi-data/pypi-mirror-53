.. _opendpda_mdf_format:

openEPDA MDF format (Draft)
===========================

Summary
~~~~~~~
This document contains draft description of the Measurement Description File
(MDF), which is used for hardware- and setup-independent configuring of the
measurements to be performed on Photonic Integrated Circuits (PIC).

Introduction
~~~~~~~~~~~~
MDF is configuration file that contains data
regarding the measurement sequences that are to be performed on a specific
die. Therefore it is linked to a specific design (cell), meaning that for
every new die design, also the applicable MDF needs to be composed. A new
MDF needs also to be composed if a different measurement sequence has to
be performed on the same die.

Being a YAML file, its content is human readable and intuitive in its structure.
It provides all necessary information starting from cell identification data, which is to be
crosschecked with other configuration files, up to the very essence of
the file which is the definition of the measurements themselves. More
details regarding YAML syntax can be found here:
https://yaml.org/spec/1.2/spec.html.

Specification
~~~~~~~~~~~~~
The data format defines how to write the information into a file. Besides
this, YAML section contains reserved keys which start with the underscore
symbol. The list of particular keys is given for a particular format version.

Version 0.2
-----------
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA MDF FORMAT``. After
this, the data section follows, which adheres to the YAML format [1],
and contains all settings (numeric and textual) data in the form of an
associative array.



An example of am openEPDA MDF is shown below.

Reserved keys
^^^^^^^^^^^^^
The following keys are required to be present in the MDF:

* ``_openEPDA``: an object defining the format and its version.
* ``mdf``: a string with a unique identifier of the MDF
* ``cell``: a string with an identifier of the PIC design to be measured
* ``die_rotation``: an angle for die position on the setup. It
  determines the orientation of the die, e.g. west-to-left or west-to-right.
* ``measurements``: Definition of the measurements used in the file. A
  measurement includes the measurement module and its settings.
  Key is the name of the measurement, value is a dictionary with
  measurement module name and settings (see Note 4).
* ``reference``: A list of reference circuits. Each list element is a
  dictionary: key is a reference port label, value is a dictionary
  `{side: port}`.
* ``measurement_sequence``: Each list element is a measurement group.
  A measurement group is a list of dictionaries, each describing a set of
  individual observation on a single circuit.

Example MDF file
^^^^^^^^^^^^^^^^

.. include:: mdf_v0.2_example.rst


Notes
^^^^^
1. All the above keys are obligatory to be present in an MDF in order
   to be used. Otherwise MDF reader should return an error of incorrect MDF
   format.
2. There must be two reference circuits defined, each containing one east
   and west port.
3. For each circuit to be measured, two ports maximum can be used at the
   same time, and they must be on the opposite sides of the chip (this comes
   from a hardware restrictions of the current setup). The ports for a circuit
   are grouped by the side, and their combinations are generated based on
   settings in measurements key.
4. The measurements key contains a dictionary of the measurements that are
   intended to be used in the MDF. The names for these can be arbitrary
   (``mmi_perm`` in the example) and they are referenced later on in the
   `measurement_sequence` part. The value contains a dictionary with required
   keys `measurement_module` and `measurement_module_settings`.
5. Measurement module name is a valid class which describes the algorithm
   performing the measurements. A measurement module can be standard or a
   user-defined. See the list of standard modules with their parameters in the
   next section.
6. The measurement_sequence tag contains a list of measurement groups. Each
   measurement group is identified by its label (top_mmi in the example) and
   contains a list of observations sets. In the example, the group top_mmi
   contains two measurement sets, each set determined by the mmi_perm
   measurement name.
7. Each dictionary describing an observation set must contain the following keys:

   * measurement
   * west_ports
   * east_ports

   The in_ports and out_ports keys can be either single port or lists of ports.
   The combinations of these to be actually used in the measurement are
   determined by in the measurements section.
8. Comments are standard YAML comments, they start with a hashtag
   symbol and can be placed at the end of any line. E.g., # This is a comment.

License
~~~~~~~
openEPDA MDF format is available under CC BY-ND 4.0 license.

This is Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). See full license text here:
`CC BY-ND 4.0 <https://creativecommons.org/licenses/by-nd/4.0/legalcode>`_.

References
~~~~~~~~~~
1. "YAML Ain't Markup Language (YAML™) Version 1.2."
`<http://yaml.org/spec/1.2/spec.html>`_.
