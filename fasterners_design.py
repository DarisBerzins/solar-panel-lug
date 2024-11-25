import numpy as np


# number of fasteners

def fasteners_amount (w, D2, x): # x is number between 2 and 3
    number_fastener= np.ceil((w/D2-3)/x+1)
    return number_fastener

# spacing center-to-center between fasteners

def fasteners_spacing (w, D2, number_fastener):
    fastener_spacing=  (w-3*D2)/number_fastener
    return fastener_spacing

# distance between edge of the plate and nearest fastener 

def edge_distance (D2):
    e1=1.5*D2
    e2=1.5*D2
    return e1, e2