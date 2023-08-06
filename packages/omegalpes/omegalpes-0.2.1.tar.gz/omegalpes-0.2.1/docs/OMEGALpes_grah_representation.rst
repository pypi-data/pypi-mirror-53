OMEGAlpes Graphical Representation
==================================

The energy systems developed in OMEGAlpes are describes following
a specified graph representation.

Energy Unit representation
--------------------------
The energy units are describes as rectangles as presented just below.
The graph is adapted considering if the unit is a
variable or a fixed energy unit.

.. figure::  images/units_fixed_variable.png
   :align:   center
   :scale:   40%

   *Figure: Energy unit representation*

A colour may be added to specify the carrier of the energy unit like
gas (yellow), thermal (red), electricity (blue).

.. figure::  images/units_carrier.png
   :align:   center
   :scale:   40%

   *Figure: Specified carrier energy unit representation*

Conversion units use the former representation inside a green box
as multi-carrier energy units. Have a look to the representation
for ElectricalToHeat and HeatPump energy units

.. figure::  images/conversion_units.png
   :align:   center
   :scale:   40%

   *Figure: Conversion units representation*


Representing all the energy unit
--------------------------------
In order to link the energy units, energy nodes and arrows should
be used. It is possible to highlight the variable which may
be optimised by the system or which is interesting for the user.

.. figure::  images/nodes_flows.png
   :align:   center
   :scale:   40%

   *Figure: Energy Nodes, Flows and Variable of interest representation*

Finally, constraints and objectives can be added on the model
with the following representation


.. figure::  images/obj_cst.png
   :align:   center
   :scale:   40%

   *Figure: Objectives and Constraints representation*

**Please, have a look to the examples to see if applications of this graphical representation**
`OMEGAlpes Examples Documentation`_

.. note:: This graph representation is not used yet as a graphical
    user interface but we hope that it will be in the near future.


.. _OMEGAlpes Examples Documentation: https://omegalpes_examples.readthedocs.io/
