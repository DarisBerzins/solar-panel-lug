import numpy as np


# number of fasteners

def fasteners_amount (w, D2, x): # x is number between 2 and 3
    number_fastener= np.ceil((w/D2-3)/x+1)
    return number_fastener

# spacing center-to-center between fasteners

def fasteners_spacing (w, D2, number_fastener):
    fastener_space =  (w-3*D2)/(number_fastener-1)
    return fastener_space


# spacing check with the condition mentioned in reader 2-3xD2.

def optimum_configuration (w, D2, x):

    while True:
        # calculate number of fasterners
        number_fastener = fasteners_amount(w, D2, x)
        #print(number_fastener)
        # Calculate spacing
        fastener_space = fasteners_spacing(w, D2, number_fastener)
        # calculating x
        spacing_factor=fastener_space/D2
        #print(x)
        #print(spacing_factor)
        if 2<=spacing_factor<=3 or x==3:
            return number_fastener, fastener_space
        x+=0.1

# distance between edge of the plate and nearest fastener 

def edge_distance (D2):
    e1=1.5*D2
    e2=1.5*D2
    return e1, e2



w=300
D2=25
x_initial=2
print(optimum_configuration(w, D2, x_initial))