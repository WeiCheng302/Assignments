import numpy as np
from numpy.linalg import inv, eig, det
import math

#def sin(angle):
#    return math.sin(angle)
	
#def cos(angle):
#    return math.cos(angle)
	
#def tan(angle):
#    return math.tan(angle)

def AngleCase(i, Angle):
    if i == 0:
        return Angle
    elif i == 1:
        return math.pi - Angle
    #elif i == 2:
    #    return Angle
    #elif i == 3:
    #    return Angle - math.pi

def AngleCase2(i, Angle):
    if i == 0:
        return Angle
    elif i == 1:
        return Angle + math.pi

def AngleCorr(Angle):
    if Angle > math.pi :
        return Angle - 2 * math.pi
    elif Angle < -math.pi:
        return Angle + 2 * math.pi
    else:
        return Angle

def RotationMatrix(omega, phi, kappa):
    MOmega = np.array([[1, 0, 0],[0, math.cos(omega), math.sin(omega)],[0, -math.sin(omega), math.cos(omega)]])
    MPhi = np.array([[math.cos(phi), 0, -math.sin(phi)],[0, 1, 0 ],[math.sin(phi), 0, math.cos(phi)]])
    MKappa = np.array([[math.cos(kappa), math.sin(kappa), 0],[-math.sin(kappa), math.cos(kappa), 0 ],[0, 0, 1]])
    return MKappa.dot(MPhi.dot(MOmega))

RA = np.array([[-0.068675, -0.0640878, -0.764565],[0.012267, 0.765774, -0.642993],[0.997564, -0.053536, -0.044728]])

Phi = math.asin(RA[2, 0])
Omega = math.asin(-RA[2, 1] / math.cos(Phi))
Kappa = math.asin(-RA[1, 0] / math.cos(Phi))

Kappa2 = math.atan(RA[1, 0] / RA[0, 0])
Omega2 = math.atan(-RA[2, 1] / RA[2, 2])
Phi2 = math.atan(RA[2, 0] * math.cos(Kappa2) / RA[0, 0])

#Kappa = math.atan(-RA[1,0]/RA[0,0])
#Phi = math.acos(RA[0,0]/math.cos(Kappa))
#Omega = math.acos(RA[2,2]*math.cos(Kappa)/RA[0,0])

print("Omega = " + str(Omega*180/math.pi) + "////" + "129.52.40")
print("Phi = " + str(Phi*180/math.pi) + "////" + "85.59.59")
print("Kappa = " + str(Kappa*180/math.pi) + "////" + "190.07.39")

print("  ")
print("Omega = " + str(Omega2*180/math.pi) + "////" + "129.52.40")
print("Phi = " + str(Phi2*180/math.pi) + "////" + "85.59.59")
print("Kappa = " + str(Kappa2*180/math.pi) + "////" + "190.07.39")

AccurateAngle = [0, 0, 0, 0, 0, 0]
AccurateAngle2 = [0, 0, 0, 0, 0, 0]

min = 99999999

for i in range(2):
    om = AngleCase(i, Omega)
    for j in range(2):
        ph = AngleCase(j, Phi)
        for k in range(2):
            ka = AngleCase(k, Kappa)
            R = RotationMatrix(om, ph, ka)
            if abs(det(R.T.dot(RA))) < min:
                min = abs(det(R.T.dot(RA)))
                AccurateAngle[0] = AngleCorr(om)*180/math.pi
                AccurateAngle[1] = AngleCorr(ph)*180/math.pi
                AccurateAngle[2] = AngleCorr(ka)*180/math.pi
                AccurateAngle[3] = i
                AccurateAngle[4] = j
                AccurateAngle[5] = k

for i in range(2):
    om = AngleCase2(i, Omega2)
    for j in range(2):
        ph = AngleCase2(j, Phi2)
        for k in range(2):
            ka = AngleCase2(k, Kappa2)
            R = RotationMatrix(om, ph, ka)
            if abs(det(R.T.dot(RA))) < min:
                min = abs(det(R.T.dot(RA)))
                AccurateAngle2[0] = AngleCorr(om)*180/math.pi
                AccurateAngle2[1] = AngleCorr(ph)*180/math.pi
                AccurateAngle2[2] = AngleCorr(ka)*180/math.pi
                AccurateAngle2[3] = i
                AccurateAngle2[4] = j
                AccurateAngle2[5] = k
				
print("    ")
print(AccurateAngle)
print(AccurateAngle2)
print("[129.52.40 85.59.59 190.07.39]")


















                
			
