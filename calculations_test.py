
from pytest import approx, raises
import calculations as calc

b = 172  # flange width
t = 13.1 # flange thickness
w = 7.9 # web thickness
fy = 350
phi =  0.9 #material resistance factor
sx = 896e3 #Elastic section modulus about major axis
sy = 129e3 #Elastic section modulus about minor axis
zx = 1010e3 #Plastic section modulus about major axis
zy = 199e3 #Plastic section modulus about minor axis
E = 200e3 #Steel Elastic Modulus
G = 77e3  #Shear Modulus
i_y = 11.1e6 #Second moment of area about minor axis
J = 333e3 # St. Venant Torsional Constant
Cw =  331e9 #Warping constant
L_min = 200
L_max = 5000
interval = 100
omega=1.0

def test_class_of_section():
    flange_class = calc.class_of_section(b, t, fy)  
    assert flange_class == 1
    
def test_flexural_capacity_LTB():
    Mr = calc.flexural_capacity_LTB(b, t, fy, phi, sx, sy, zx, zy, E, G, i_y, J, Cw, L_min, L_max, interval, omega)
    Mr_LTB = min(Mr[1])/1e6
    assert Mr_LTB == approx(159.76464)