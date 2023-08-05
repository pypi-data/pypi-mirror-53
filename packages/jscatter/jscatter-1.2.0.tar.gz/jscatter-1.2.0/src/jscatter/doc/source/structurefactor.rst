structurefactor (sf)
====================

.. automodule:: jscatter.structurefactor
    :noindex:

Structure Factors
-----------------
.. autosummary::
   RMSA
   PercusYevick
   PercusYevick1D
   PercusYevick2D
   stickyHardSphere
   adhesiveHardSphere
   criticalSystem
   weakPolyelectrolyte
   latticeStructureFactor
   orientedLatticeStructureFactor
   radialorientedLSF

Hydrodynamics
-------------
.. autosummary::
   hydrodynamicFunct
   
Pair Correlation
----------------
.. autosummary::
   sq2gr

Lattice
-------
Lattices to describe atomic crystals or **mesoscopic materials** as ordered  structures  of spheres, ellipsoids,
cylinders or planes in 3D (fcc,  bcc,  hcp,  sc), 2D (hex, sq) and lamellar structures.
For the later it is assumed that particles share the same normalised formfactor
but allow particle specific scattering amplitude.

The small angle scattering of a nano particle build from a lattice may be calculated by
:py:func:`~.formfactor.cloudScattering` or :py:func:`~.formfactor.orientedCloudScattering`.

The crystal structure factor of a lattice  may be calculated by :py:func:`~.structurefactor.latticeStructureFactor`
and related functions (see above).

Methods

.. autosummary::
    latticeFromCIF
    ~jscatter.lattice.latticeVectorsFromLatticeConstants

**Lattices with specific structure** :

3D

.. autosummary::
    bravaisLattice
    scLattice
    bccLattice
    fccLattice
    hexLattice
    hcpLattice
    diamondLattice
    rhombicLattice
    pseudoRandomLattice


2D

.. autosummary::
    sqLattice
    hex2DLattice

1D

.. autosummary::
    lamLattice

**lattice methods** :

.. autosummary::
    lattice.X
    lattice.Y
    lattice.Z
    lattice.XYZ
    lattice.b
    lattice.array
    lattice.points
    lattice.set_b
    lattice.type
    lattice.move
    lattice.centerOfMass
    lattice.numberOfAtoms
    lattice.show
    lattice.filter
    lattice.planeSide
    lattice.inSphere
    lattice.inParallelepiped
    rhombicLattice.unitCellAtomPositions
    rhombicLattice.getReciprocalLattice
    rhombicLattice.getRadialReciprocalLattice
    rhombicLattice.getScatteringAngle
    rhombicLattice.rotatePlane2hkl
    rhombicLattice.rotatePlaneAroundhkl
    rhombicLattice.rotatehkl2Vector
    rhombicLattice.rotateAroundhkl
    rhombicLattice.vectorhkl

.. include:: ../../lattice.py
    :start-after: ---
    :end-before:  END

--------

.. automodule:: jscatter.structurefactor
    :members:
    :undoc-members:
    :show-inheritance:


.. autoclass:: lattice
    :members:

.. autoclass:: rhombicLattice
    :members:

.. autoclass:: bravaisLattice
.. autoclass:: scLattice
.. autoclass:: bccLattice
.. autoclass:: fccLattice
.. autoclass:: hexLattice
.. autoclass:: hcpLattice
.. autoclass:: diamondLattice
.. autoclass:: pseudoRandomLattice
.. autoclass:: sqLattice
.. autoclass:: hex2DLattice
.. autoclass:: lamLattice
.. autoclass:: latticeFromCIF

.. automodule:: jscatter.lattice
    :members:
     latticeVectorsFromLatticeConstants
