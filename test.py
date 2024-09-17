import pynbody as pyn
import matplotlib.pyplot as plt

sim = pyn.load('simFiles/run708main.01000')
pyn.analysis.angmom.faceon(sim)
sim.physical_units()

print(sim.g['rho'].units)