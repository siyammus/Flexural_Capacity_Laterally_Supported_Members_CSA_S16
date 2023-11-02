import sectionproperties.pre.library.steel_sections as steel_geom
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section
from handcalcs.decorator import handcalc
from typing import Optional
import math
import numpy as np
import W_section_sectionprop as Wsec

calc_renderer = handcalc()


def class_of_section(flange_width:float, 
                     flange_thickness:float, 
                     fy:float) -> int:
        """
        This function Returns a float representing the the classification of flange W section either
        Class 1, 2 or 3 according to Table 2 of CSA S16-19
        """
        flange_class = 0
        effective_width = flange_width/2

        if (effective_width /flange_thickness) <= (145 / math.sqrt(fy)):
            flange_class = 1
            return flange_class  
        elif (effective_width /flange_thickness) <= (170 / math.sqrt(fy)):
            flange_class = 2
            return flange_class
        elif (effective_width /flange_thickness) <= (200 / math.sqrt(fy)):
            flange_class = 3
            return flange_class 
        else:
            return "Classification of section is Class 4"  
        

# def createList(L_min:int, L_max:int, interval:int):
#     L = np.arange(L_min, L_max+1, interval)
#     return L
     
        
def flexural_capacity_LTB(flange_width:float, 
                          flange_thickness:float, 
                          fy:float,
                          phi:float, 
                          sx:float,
                          sy:float, 
                          zx:float, 
                          zy:float,
                          E:float, 
                          G:float, 
                          i_y:float, 
                          J:float, 
                          Cw:float,  
                          L_min:float,
                          L_max:float,
                          interval:float,
                          omega:float = 1.0) -> list:
    """
    This function calculates the flexural capacity of laterally unsupported
    W Class 1, 2 or 3 sections
    """

    # Classification of a section
    section_class = class_of_section(flange_width, flange_thickness, fy)
    
    # Elastic and Plastic moment capacities in major and minor axes
    My_x = phi * sx * fy
    Mp_x = phi * zx * fy

    My_y = phi * sy * fy
    Mp_y = phi * zy * fy

    #Critical Elastic moment of unbraced segment
    # L = createList(L_min, L_max, interval)
    #Critical Elastic moment of unbraced segment
    Mu = []
    Mr = []
    L = list(range(L_min, L_max+interval, interval))

    for i in L:
        Mui = ((omega * math.pi)/(1.2*i)) * math.sqrt(E*i_y*G*J + ((math.pi*E) / i)**2 * i_y * Cw)
        if (section_class == 1) and (Mui > 0.67*Mp_x):
            Mri = min(1.15*phi*Mp_x * (1 - ((0.28*Mp_x)/Mui)), phi*Mp_x)
            Mu.append(Mui)
            Mr.append(Mri)
        elif (section_class == 2) and (Mui > 0.67*Mp_x):
            Mri = min(1.15*phi*Mp_x * (1 - ((0.28*Mp_x)/Mui)), phi*Mp_x)
            Mu.append(Mui)
            Mr.append(Mri)
        elif (section_class == 1) and (Mui <= 0.67*Mp_x):
            Mri = phi*Mui
            Mu.append(Mui)
            Mr.append(Mri)
        elif (section_class == 2) and (Mui <= 0.67*Mp_x):
            Mri = phi*Mui
            Mu.append(Mui)
            Mr.append(Mri)
        elif (section_class == 3) and (Mui > 0.67*My_x):
            Mri = min(1.15*phi*My_x * (1 - ((0.28*My_x)/Mui)), phi*My_x)
            Mu.append(Mui)
            Mr.append(Mri)
        elif (section_class == 3) and (Mui <= 0.67*My_x):
            Mri = phi*Mui
            Mu.append(Mui)
            Mr.append(Mri)
        else:
            print("Mr is to be computed for Class 4 Section")
    return L, Mr

### Compare Values obtained from Steel Hanbook with Section properties values


# def flexural_capacity_LTB_from_sectionprop(flange_width:float, 
#                           flange_thickness:float, 
#                           fy:float,
#                           phi:float, 
#                           zxx1:float,
#                           zyy2:float, 
#                           sxx:float, 
#                           syy:float,
#                           E:float, 
#                           G:float, 
#                           iyy_c:float, 
#                           j:float, 
#                           Iw:float,  
#                           L_min:float,
#                           L_max:float,
#                           interval:float,
#                           omega:float = 1.0) -> list:
#     """
#     This function calculates the flexural capacity of laterally unsupported
#     W Class 1, 2 or 3 sections
#     """



#     print(f"Area = {area:.1f} mm2")
#     print(f"Ixx = {ixx_c:.3e} mm4")
#     print(f"Iyy = {iyy_c:.3e} mm4")
#     print(f"Ixy = {ixy_c:.3e} mm4")
#     print(f"Principal axis angle = {phi:.1f} deg")
#     print(f"Torsion constant = {j:.3e} mm4")
#     print(f"Zxx = {sxx:.3e} mm3")
#     print(f"Zyy = {syy:.3e} mm3")
#     print(f"Sxx = {zxx1:.3e} mm3")
#     print(f"Syy = {zyy2:.3e} mm3")
#     print(f"Warping constant = {Iw:.3e} mm6")

#     # Classification of a section
#     section_class = class_of_section(flange_width, flange_thickness, fy)
    
#     # Elastic and Plastic moment capacities in major and minor axes
#     My_x_sp = phi * zxx1 * fy
#     Mp_x_sp = phi * sxx * fy

#     My_y = phi * zyy2 * fy
#     Mp_y = phi * syy * fy

#     #Critical Elastic moment of unbraced segment
#     # L = createList(L_min, L_max, interval)
#     #Critical Elastic moment of unbraced segment
#     Mu_sp = []
#     Mr_sp = []
#     L = list(range(L_min, L_max+interval, interval))

#     for i in L:
#         Mui_sp = ((omega * math.pi)/(1.2*i)) * math.sqrt(E*iyy_c*G*j + ((math.pi*E) / i)**2 * iyy_c * Iw)
#         if (section_class == 1) and (Mui_sp > 0.67*Mp_x_sp):
#             Mri_sp = min(1.15*phi*Mp_x_sp* (1 - ((0.28*Mp_x_sp)/Mui_sp)), phi*Mp_x_sp)
#             Mu_sp.append(Mui_sp)
#             Mr_sp.append(Mri_sp)
#         elif (section_class == 2) and (Mui_sp > 0.67*Mp_x_sp):
#             Mri_sp = min(1.15*phi*Mp_x_sp * (1 - ((0.28*Mp_x_sp)/Mui)), phi*Mp_x_sp)
#             Mu_sp.append(Mui_sp)
#             Mr_sp.append(Mri_sp)
#         elif (section_class == 1) and (Mui_sp <= 0.67*Mp_x_sp):
#             Mri_sp = phi*Mui_sp
#             Mu_sp.append(Mui_sp)
#             Mr_sp.append(Mri_sp)
#         elif (section_class == 2) and (Mui_sp <= 0.67*Mp_x_sp):
#             Mri_sp = phi*Mui_sp
#             Mu_sp.append(Mui)
#             Mr_sp.append(Mri_sp)
#         elif (section_class == 3) and (Mui > 0.67*My_x_sp):
#             Mri_sp = min(1.15*phi*My_x_sp * (1 - ((0.28*My_x_sp)/Mui)), phi*My_x_sp)
#             Mu_sp.append(Mui)
#             Mr_sp.append(Mri)
#         elif (section_class == 3) and (Mui <= 0.67*My_x_sp):
#             Mri_sp = phi*Mui_sp
#             Mu_sp.append(Mui_sp)
#             Mr_sp.append(Mri_sp)
#         else:
#             print("Mr is to be computed for Class 4 Section")
#     return L, Mr_sp