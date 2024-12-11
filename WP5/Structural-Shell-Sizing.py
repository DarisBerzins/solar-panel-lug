# Sizes the structural shells depending on loads, computes its mass and updates
# Diferent from report --> Normal stress distributions can be calculated and plotted
import numpy as np
import matplotlib.pyplot as plt

class Shell():
    def __init__(self, length, diameter, E_modulus):