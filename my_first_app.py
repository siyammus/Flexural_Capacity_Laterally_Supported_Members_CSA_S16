import streamlit as st
import plotly.graph_objects as go
import sectionproperties.pre.library.steel_sections as steel_geom
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section
import calculations as calc

st.header("Flexural Capacity of Laterally Unsupported Class 1/2/3 W-Sections")

st.sidebar.subheader("Results Parameters")
L_min = st.sidebar.number_input("Minimum Unbraced Length ($mm$)", value=200)
L_max = st.sidebar.number_input("Maximum Unbraced Length ($mm$)", value=5000)
interval = st.sidebar.number_input("Unbraced length step interval ($mm$)", value=100)

# Section Properties
st.sidebar.subheader("Section Properties of W Section")
area = st.sidebar.number_input("**Area** ($mm^2$)", value=7230)
d = st.sidebar.number_input("d ($mm$)", value=358)
b = st.sidebar.number_input("b ($mm$)", value=172)
t = st.sidebar.number_input("t ($mm$)", value=13.1)
w = st.sidebar.number_input("w ($mm$)", value=7.9)
i_x = st.sidebar.number_input("Ix (10e6 $mm^4$)", value=160e6)
i_y = st.sidebar.number_input("Iy (10e6 $mm^4$)", value=11.1e6)
s_x = st.sidebar.number_input("Sx (10e3 $mm^3$)", value=896e3)
s_y = st.sidebar.number_input("Sy (10e3 $mm^3$)", value=129e3)
z_x = st.sidebar.number_input("Zx (10e3 $mm^3$)", value=1010e3)
z_y = st.sidebar.number_input("Zy (10e3 $mm^3$)", value=199e3)
J = st.sidebar.number_input("J (10e3 $mm^4$)", value=333e3)
Cw = st.sidebar.number_input("Cw (10e9 $mm^6$)", value=331e9)
E = st.sidebar.number_input("Elastic modulus section (MPa)", value=200e3)
G = st.sidebar.number_input("Shear modulus of section (MPa)", value=77e3)
fy = st.sidebar.number_input("Yield strength of section (MPa)", value=350)
phi = 0.9 #material reduction factor of steel
omega = 1.0


col1, col2, col3, col4 = st.columns(4)

with col1:

    # Classification of section from Cl.11.1 and Cl.11.2 of CSA S16-19
    flange_class = calc.class_of_section(b, t, fy)
    st.write(f"The class of section W360x57 is {flange_class}")

with col2:
    ## Analysis from CISC Handbook geometric properties of W360x57 section using Cl13.6 from CSA S16-19 code
    Mr_LTB = calc.flexural_capacity_LTB(b, t, fy, phi, s_x, s_y, z_x, z_y, E, G, i_y, J, Cw, L_min, L_max, interval, omega)
    rr = min(Mr_LTB[1])/1e6
    st.write(f"The flexural capacity of W360x57 section using CISC geometric properties is {rr:.5f} kN.m ")

with col3:
    
## Using Section Properties Program
# W360x57
    k1=21  # Distances given for I section in Canadian Steel Handbook CISC
    w= 7.9 # web thickness

    Wsection1 = steel_geom.i_section(
        d=358,
        b=172,
        t_f=13.1,
        t_w=7.9,
        r=k1 - w/2,
        n_r=15,
    )
    Wsection1

    Wsection1.plot_geometry()

    #Mesh the section and create analysis section

    Wsection1.create_mesh(mesh_sizes=10)
    sec = Section(Wsection1, time_info=True)
    sec.plot_mesh()

    #Perform analysis

    sec.calculate_geometric_properties()
    sec.calculate_plastic_properties()
    sec.calculate_warping_properties()

    #Review results
    sec.display_results()

    # Retrieve individual properties from results

    sec.calculate_frame_properties()
    area = sec.get_area()
    ixx_c, iyy_c, ixy_c = sec.get_ic()
    angle = sec.get_phi()
    j = sec.get_j()
    sxx, syy = sec.get_s()   # defines plastic properties of section in section properties
    zxx1, zyy1, zxx2, zyy2  = sec.get_z() # defines elastic properties of section in section properties
    Iw = sec.get_gamma()

    # st.write(f"Area = {area:.1f} mm2")
    # st.write(f"Ixx = {ixx_c:.3e} mm4")
    # st.write(f"Iyy = {iyy_c:.3e} mm4")
    # st.write(f"Ixy = {ixy_c:.3e} mm4")
    # st.write(f"Principal axis angle = {angle:.1f} deg")
    # st.write(f"Torsion constant = {j:.3e} mm4")
    # st.write(f"Zxx = {sxx:.3e} mm3")
    # st.write(f"Zyy = {syy:.3e} mm3")
    # st.write(f"Sxx = {zxx1:.3e} mm3")
    # st.write(f"Syy = {zyy2:.3e} mm3")
    # st.write(f"Warping constant = {Iw:.3e} mm6")

    Mr_LTB_secprop = calc.flexural_capacity_LTB(b, t, fy, phi, zxx1, zyy2, sxx, syy, E, G, iyy_c, j, Iw, L_min, L_max, interval, omega)
    tt = min(Mr_LTB_secprop[1])/1e6
    st.write(f"The flexural capacity of W360x57 section using section properties program is {tt:.5f} kN.m")


with col4:
    perc_diff = (tt-rr)/100 * 100
    st.write(f"The percentage difference between Moment Capacities is {perc_diff:.2f}%")

## Plotting figures for CSA geometric properties and Section Properties program
fig = go.Figure()

# Plot lines
fig.add_trace(
    go.Scatter(
    x=Mr_LTB[0], 
    y=Mr_LTB[1],
    line={"color": "red"},
    name="Mr capacity with LTB using CISC Hanbook properties"
    )
)

fig.add_trace(
    go.Scatter(
    x=Mr_LTB_secprop[0], 
    y=Mr_LTB_secprop[1],
    line={"color": "teal"},
    name="Mr capacity with LTB using Section Properties program"
    )
)

fig.layout.title.text = "Factored Moment Capacity of Class 1/2/3 W-Section"
fig.layout.xaxis.title = "Unbraced Length L, mm"
fig.layout.yaxis.title = "Factored Moment Capacity, N"


st.plotly_chart(fig)


