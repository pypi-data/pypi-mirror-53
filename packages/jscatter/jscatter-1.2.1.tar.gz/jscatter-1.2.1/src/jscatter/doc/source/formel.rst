formel
======

.. automodule:: jscatter.formel
    :noindex:

Functions
---------
.. autosummary::
   loglist
   gauss
   lorentz
   voigt
   lognorm
   box
   Ea
   boseDistribution

Quadrature
----------
.. autosummary::
   parQuadratureSimpson
   parQuadratureFixedGauss
   parQuadratureAdaptiveGauss
   sphereAverage
   psphereAverage
   convolve

Distribution of parameters
--------------------------
Experimental data might be influenced by multimodal parameters (like multiple sizes)
or by one or several parameters distributed around a mean value.

.. autosummary::
    parDistributedAverage
    multiParDistributedAverage
    scatteringFromSizeDistribution

Centrifugation
--------------
.. autosummary::
   sedimentationCoefficient
   sedimentationProfile
   sedimentationProfileFaxen                                                                                                                                     

NMR
---
.. autosummary::
   DrotfromT12
   T1overT2
   
Material Data
-------------
.. autosummary::   
   scatteringLengthDensityCalc
   waterdensity
   bufferviscosity
   dielectricConstant
   watercompressibility
   cstar
   molarity
   viscosity
   Dtrans
   Drot

other Stuff
-----------
.. autosummary::
   memoize
   xyz2rphitheta
   rphitheta2xyz
   rotationMatrix
   fibonacciLatticePointsOnSphere
   randomPointsOnSphere
   randomPointsInCube
   smooth

Constants and Tables
--------------------
.. autosummary::
    felectron
    Elements

-----

.. automodule:: jscatter.formel
    :members:
    :undoc-members:
    :show-inheritance:


   
   