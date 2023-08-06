# OXASL_MP

Plugin for the OXASL pipeline to support multiphase ASL data.

The multiphase data is fitted to the multiphase model and the
output magnitude is used as the differenced output for 
conventional ASL modelling

## Issues

One issue is that for multi-PLD data the phase offset map
is not shared between PLDs. To solve this problem we need to
modify the multiphase model to accept multi-PLD data directly.

## Citation

*Quantitative blood flow measurement in rat brain with multiphase arterial spin labelling magnetic resonance imaging.*
Larkin, James R, Manon A Simard, Alexandre A Khrapitchev, James A Meakin, Thomas W Okell, Martin Craig, Kevin J Ray, Peter Jezzard, Michael A Chappell, Nicola R Sibson.
Journal of Cerebral Blood Flow & Metabolism. https://doi.org/10.1177/0271678X18756218
