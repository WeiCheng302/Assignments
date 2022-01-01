import math
import numpy as np

X = np.array([0.07473996, -0.0865396857, 1.11085856])#np.array([1000,1000,1000])
Y = np.array([1.74411464, 0.0515281148, -0.5480666258])#np.array([1620,740,340])
Z = np.array([-0.5204898,-0.415525526,-2.48921418])

Centroid_XYZ = np.array([(X[0]+Y[0]+Z[0])/3, (X[1]+Y[1]+Z[1])/3, (X[2]+Y[2]+Z[2])/3])

X_ = X - Centroid_XYZ
Y_ = Y - Centroid_XYZ
Z_ = Z - Centroid_XYZ

VecA_ind = X_ - Y_
VecB_ind = X_ - Z_
VecA_ind_Unit = VecA_ind / np.linalg.norm(VecA_ind)
VecB_ind_Unit = VecB_ind / np.linalg.norm(VecB_ind)

AngleABint = math.acos(VecA_ind_Unit.dot(VecB_ind_Unit))
p_int = np.cross(VecB_ind_Unit, VecA_ind_Unit) / math.sin(AngleABint)
q_int = np.cross(VecA_ind_Unit, p_int)

R1 = np.array([[q_int[0],q_int[1],q_int[2]],[VecA_ind_Unit[0],VecA_ind_Unit[1],VecA_ind_Unit[2]],[p_int[0],p_int[1],p_int[2]]])

E = np.array([175424.125, 2537356.25, 37.415])#np.array([1911.9,1435.2,554.1])
N = np.array([175446.188,2537381.25,34.963])
U = np.array([175472.734,2537381.25,39.325])

Centroid_ENU = np.array([(E[0]+N[0]+U[0])/3, (E[1]+N[1]+U[1])/3, (E[2]+N[2]+U[2])/3])

E_ = E - Centroid_ENU
N_ = N - Centroid_ENU
U_ = U - Centroid_ENU

VecA_97 = E_ - N_
VecB_97 = E_ - U_
VecA_97_Unit = VecA_97 / np.linalg.norm(VecA_97)
VecB_97_Unit = VecB_97 / np.linalg.norm(VecB_97)

AngleAB97 = math.acos(VecA_97_Unit.dot(VecB_97_Unit))
p_97 = np.cross(VecB_97_Unit, VecA_97_Unit) / math.sin(AngleAB97)
q_97 = np.cross(VecA_97_Unit, p_97)

R2 = np.array([[q_97[0],q_97[1],q_97[2]],[VecA_97_Unit[0],VecA_97_Unit[1],VecA_97_Unit[2]],[p_97[0],p_97[1],p_97[2]]])

RA = R2.T.dot(R1)

Kappa = math.atan(-RA[1,0]/RA[0,0])
Phi = math.acos(RA[0,0]/math.cos(Kappa))
Omega = math.acos(RA[2,2]*math.cos(Kappa)/RA[0,0])
print(Kappa*180/math.pi)
print(Phi*180/math.pi)
print(Omega*180/math.pi)

X_Trans = RA.dot(X_)
Y_Trans = RA.dot(Y_)
Z_Trans = RA.dot(Z_)

print(E)
print(X_Trans + Centroid_ENU)
print(N)
print(Y_Trans + Centroid_ENU)
print(U)
print(Z_Trans + Centroid_ENU)













