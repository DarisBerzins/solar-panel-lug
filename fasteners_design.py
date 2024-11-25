import numpy as np


# number of fasteners

def fasteners_amount (w, D2, x): # x is number between 2 and 3
    number_fastener= np.ceil((w/D2-3)/x+1)
    return number_fastener

# spacing center-to-center between fasteners

def fasteners_spacing (w, D2, number_fastener):
    fastener_space =  (w-3*D2)/(number_fastener-1)
    return fastener_space
# spacing check with the condition mentioned in reader

def spacing_check (w, D2):
    x = 2.5
    # calculate number of fasterners
    number_fastener = fasteners_amount(w, D2, x)
    # Calculate spacing
    fastener_space = fasteners_spacing(w, D2, number_fastener)
    x=fastener_space/D2
    while True:
        # calculate number of fasterners
        number_fastener = fasteners_amount(w, D2, x)
        # Calculate spacing
        fastener_space = fasteners_spacing(w, D2, number_fastener)
        # calculating x
        print(x)
        
        if 2<=x<=3:
            return number_fastener, fastener_space
        elif x<2:
            
            x+=0.01
        else:
            x-=0.01
    return
        

# distance between edge of the plate and nearest fastener 

def edge_distance (D2):
    e1=1.5*D2
    e2=1.5*D2
    return e1, e2

w = 100  # Width of the plate
D2 = 10  # Diameter or parameter value

# Calculate the number of fasteners and spacing
number_fastener, fastener_space = spacing_check(w, D2)

# Calculate the edge distances
e1, e2 = edge_distance(D2)

print(f"Number of fasteners: {number_fastener}")
print(f"Spacing between fasteners: {fastener_space}")
print(f"Edge distances: e1 = {e1}, e2 = {e2}")
