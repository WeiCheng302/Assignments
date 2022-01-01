import math
import numpy as np

def cos(value):
    return math.cos(value)

def sin(value):
    return math.sin(value)

def Rotation_Mat(omega, phi, kappa):
    o = omega
    p = phi
    k = kappa
    
    R = np.array([[cos(p)*cos(k), cos(o)*sin(k)+sin(o)*sin(p)*cos(k), sin(o)*sin(k)-cos(o)*sin(p)*cos(k)], 
                  [-cos(p)*sin(k), cos(o)*cos(k)-sin(o)*sin(p)*sin(k), sin(o)*cos(k)+cos(o)*sin(p)*sin(k)], 
                  [sin(p), -sin(o)*cos(p), cos(o)*cos(p)]])
    return R
    
def Translation_Mat(Tx, Ty, Tz):
    T = np.array([Tx, Ty, Tz])
    return T

#Question01
point_pB = np.array([50, 100, 150]).T
Rab = Rotation_Mat(5 * math.pi / 180 , 10 * math.pi / 180 , 15 * math.pi / 180 )
Tab = Translation_Mat(10, 10, 10).T
point_pA = Rab.dot(point_pB) + Tab

print("    ")
print("#Question01")
print("    ")
print("Rab = ")
print(Rab)
print("    ")
print("Point P @ A frame = ")
print(point_pA)

#Question02
Rba = Rab.T
Tba = Rba.dot(point_pB) - point_pA 
Eul_omega = (math.atan(-Rba[2,1]/Rba[2,2]))**2
Eul_phi = (math.atan(Rba[2,0]/(Rba[2,2]**2 + Rba[2,1]**2)**0.5))**2
Eul_kappa = (math.atan(-Rba[1,0]/Rba[0,0]))**2

print("    ")
print("#Question02")
print("    ")
print("Omegaba = ")
print(Eul_omega * math.pi / 180 )
print("    ")
print("Phiba = ")
print(Eul_phi * math.pi / 180 )
print("    ")
print("Kappaba = ")
print(Eul_kappa * math.pi / 180 )
print("    ")
print("Rba = ")
print(Rba)
print("    ")
print("Tba = ")
print(Tba)

#Question03
#EOP
E28 = 169316.359
N28 = 2544469.908
H28 = 1727.712 
Omega28 = 354.035 * math.pi / 180 
Phi28 = 353.098 * math.pi / 180 
Kappa28 = 322.358 *  math.pi / 180 

#IOP
PixelSize = 0.000006 #m
ImgW = 11310 #pix
ImgH = 17310 #pix
ImgW_mm = 67.86 #mm
ImgH_mm = 103.86 #mm
F_mm = 100.5 #mm
ppu_mm = -0.183 #mm
ppv_mm = 0.003 #mm
ppu_pix = ImgW/2 - 30.5 #pix
ppv_pix = ImgH/2 - 0.5 #pix

#Cam_28
Scale = -F_mm/(H28*1000)
Rot_CM = Rotation_Mat(Omega28, Phi28, Kappa28)

T28 = np.array([E28, N28, H28]).T 

def ToCamCS28(Ep, Np, Hp):
    return Scale * Rot_CM.dot(np.array([Ep - E28, Np - N28, Hp - H28]).T)

def ToImgCS28(Imgx_mm, Imgy_mm):
    Imgx_mm = Imgx_mm + ppu_mm
    Imgy_mm = Imgy_mm + ppv_mm
    Imgx_pix = Imgx_mm/(PixelSize*1000) + ImgW/2
    Imgy_pix = -(Imgy_mm/(PixelSize*1000)) + ImgH/2
    return np.array([Imgx_pix, Imgy_pix])

G1_28 = ToCamCS28(169367.129, 2544958.454, 14.816)
G4_28 = ToCamCS28(168802.226, 2544089.245, 13.014)
G30_28 = ToCamCS28(169346.078, 2543964.132, 14.441)
print("    ")
print("#Question03")
print("    ")
print("G1 @ Camera C.S. = ")
print(G1_28)
print("    ")
print("G1 @ Image C.S. = ")
print(ToImgCS28(G1_28[0]/G1_28[2], G1_28[1]/G1_28[2]))
print("    ")
print("G4 @ Camera C.S. = ")
print(G4_28)
print("    ")
print("G4 @ Image C.S. = ")
print(ToImgCS28(G4_28[0]/G4_28[2], G4_28[1]/G4_28[2]))
print("    ")
print("G30 @ Camera C.S. = ")
print(G30_28)
print("    ")
print("G30 @ Image C.S. = ")
print(ToImgCS28(G30_28[0]/G30_28[2], G30_28[1]/G30_28[2]))
print("    ")
print("All next to the principle point ????")
print("    ")

#Question04
#K = np.array([[1/(PixelSize), 0, -ImgW/(2 * F_mm/1000)],
#              [0, -1/(PixelSize), -ImgH/(2 * F_mm/1000)],
#              [0, 0, -1/(F_mm/1000)]])
R = Rotation_Mat(Omega28, Phi28, Kappa28)
#KppRX0 = K.dot(np.array([ppu_mm/1000, ppv_mm/1000, 0]).T - R.dot(np.array([E28, N28, H28]).T))
#KR = K.dot(R)
#print(K)
#print(KR)
#print(KppRX0)
#DLT = np.array([[KR[0,0],KR[0,1],KR[0,2],KppRX0[0]],
#              [KR[1,0],KR[1,1],KR[1,2],KppRX0[1]],
#              [KR[2,0],KR[2,1],KR[2,2],KppRX0[2]]])
#DLT = DLT/KppRX0[2]

L1 = R[0,0] + R[2,0] * ppu_pix + R[2,0] * PixelSize * ImgW / (2 * F_mm)
L2 = R[0,1] + R[2,1] * ppu_pix + R[2,1] * PixelSize * ImgW / (2 * F_mm)
L3 = R[0,2] + R[2,2] * ppu_pix + R[2,2] * PixelSize * ImgW / (2 * F_mm)
L4 = -(R[0,0] * E28 + R[0,1] * N28 + R[0,2] * H28) - ppu_pix * (R[2,0] * E28 + R[2,1] * N28 + R[2,2] * H28) - ImgW * PixelSize * (R[2,0] * E28 + R[2,1] * N28 + R[2,2] * H28)/ (2 * F_mm)
L5 = R[1,0] + R[2,0] * ppv_pix + R[2,0] * PixelSize * ImgH / (2 * F_mm)
L6 = R[1,1] + R[2,1] * ppv_pix + R[2,1] * PixelSize * ImgH / (2 * F_mm)
L7 = R[1,2] + R[2,2] * ppv_pix + R[2,2] * PixelSize * ImgH / (2 * F_mm)
L8 = -(R[1,0] * E28 + R[1,1] * N28 + R[1,2] * H28) - ppv_pix * (R[2,0] * E28 + R[2,1] * N28 + R[2,2] * H28) - ImgH * PixelSize * (R[2,0] * E28 + R[2,1] * N28 + R[2,2] * H28)/ (2 * F_mm)
L9 = R[2,0]
L10 = R[2,1]
L11 = R[2,2]
L12 = -(R[2,0] * E28 + R[2,1] * N28 + R[2,2] * H28)

DLT = np.array([[L1/L12,L2/L12,L3/L12,L4/L12],
                [L5/L12,L6/L12,L7/L12,L8/L12],
                [L9/L12,L10/L12,L11/L12,L12/L12]])
				
BP_G1 = DLT.dot(np.array([169367.129, 2544958.454, 14.816, 1]).T)
BP_G4 = DLT.dot(np.array([168802.226, 2544089.245, 13.014, 1]).T)
BP_G30 = DLT.dot(np.array([169346.078, 2543964.132, 14.441, 1]).T)

print("#Question04")
print("    ")
print("DLT Matrix = ")
print(DLT)
print("    ")
print("Back Project G1 : ")
print(BP_G1[0]/BP_G1[2], BP_G1[1]/BP_G1[2])
print("    ")
print("Back Project G4 : ")
print(BP_G4[0]/BP_G4[2], BP_G4[1]/BP_G4[2])
print("    ")
print("Back Project G30 : ")
print(BP_G30[0]/BP_G30[2], BP_G30[1]/BP_G30[2])

#HW3-1

#Question01

#def Collinearity_toCR(EOP, R, Obj):
#    q1 = -0.001*F_mm*(R[0,0]*(Obj[0]-EOP[0])+R[0,1]*(Obj[1]-EOP[1])+R[0,2]*(Obj[2]-EOP[2]))
#    q2 = -0.001*F_mm*(R[1,0]*(Obj[0]-EOP[0])+R[1,1]*(Obj[1]-EOP[1])+R[1,2]*(Obj[2]-EOP[2]))
#    q3 = R[2,0]*(Obj[0]-EOP[0])+R[2,1]*(Obj[1]-EOP[1])+R[2,2]*(Obj[2]-EOP[2])
	
#    return[(q1/q3 + ppu_mm)/PixelSize + ImgW/2, ImgH/2 -(q2/q3+ppv_mm)/PixelSize]

Omega30 = 353.447  * 180 / math.pi
Phi30 = 354.961 * 180 / math.pi
Kappa30 = 322.252 * 180 / math.pi
#Obj28 = np.array([169316.359, 2544469.908, 0, 1]).T
#Obj30 = np.array([169571.460, 2544279.421, 0, 1]).T
#DLT_PC28 = DLT.dot(EOP28)
#DLT_PC30 = DLT.dot(EOP30)
#Coli_PC28 = Collinearity_toCR(EOP28, Rotation_Mat(Omega28, Phi28, Kappa28), Obj28)
#Coli_PC30 = Collinearity_toCR(EOP30, Rotation_Mat(Omega30, Phi30, Kappa30), Obj30)

def parallex(XA1, XA2):
    UA1 = (XA1 + ImgW/2)*PixelSize
    UA2 = (XA2 + ImgW/2)*PixelSize
    return UA1-UA2
	
def parallex_H(PL, BL, H, F):
    return H - (BL*F/PL)

H = 1700

EOP28 = np.array([169316.359, 2544469.908, H, 1]).T
EOP30 = np.array([169571.460, 2544279.421, H, 1]).T
Top28 = np.array([6384, 10582]).T
Top30 = np.array([3363, 10214]).T
Buttom28 = np.array([6159, 10443]).T
Buttom30 = np.array([3558, 10061]).T

Baseline = ((EOP28[0]-EOP30[0])**2+(EOP28[1]-EOP30[1])**2)**0.5
	
parallex_Top = parallex(Top28[0], Top30[0])
parallex_Buttom = parallex(Buttom28[0], Buttom30[0])
	
H_Top = parallex_H(parallex_Top, Baseline, H, F_mm/1000)
H_Buttom = parallex_H(parallex_Buttom, Baseline, H, F_mm/1000)

print("    ")
print("Homework 3")
print("#Question01")
print("    ")
print("Baseline = ")
print(Baseline)
print("    ")
print("Parallex Top / Parallex Buttom = ")
print(parallex_Top, parallex_Buttom)
print("    ")
print("Building Height = ")
print((H_Top - H_Buttom))

#Question02

Rot28 = Rotation_Mat(Omega28, Phi28, Kappa28)
Rot30 = Rotation_Mat(Omega30, Phi30, Kappa30)

Rot30to28 = Rot28.dot(Rot30.T)
Eul_omega_3028 = (math.atan(-Rot30to28[2,1]/Rot30to28[2,2]))**2
Eul_phi_3028 = (math.atan(Rot30to28[2,0]/(Rot30to28[2,2]**2 + Rot30to28[2,1]**2)**0.5))**2
Eul_kappa_3028 = (math.atan(-Rot30to28[1,0]/Rot30to28[0,0]))**2

xyf_Top_28 = np.array([(Top28[0] + ImgW/2)*PixelSize,(Top28[1] + ImgH/2)*PixelSize, -F_mm]).T
xyf_Top_30 = np.array([(Top30[0] + ImgW/2)*PixelSize,(Top30[1] + ImgH/2)*PixelSize, -F_mm]).T
xyf_Buttom_28 = np.array([(Buttom28[0] + ImgW/2)*PixelSize,(Buttom28[1] + ImgH/2)*PixelSize, -F_mm]).T
xyf_Buttom_30 = np.array([(Buttom30[0] + ImgW/2)*PixelSize,(Buttom30[1] + ImgH/2)*PixelSize, -F_mm]).T

Baseline = np.array([EOP28[0]-EOP30[0],EOP28[1]-EOP30[1], EOP28[2]-EOP30[2]]).T  

def DET(a,b,c,d,e,f,g,h,i):
    return a*e*i + d*h*c + b*f*g - c*e*g - a*h*f - b*d*i
	
plane_Top = DET(xyf_Top_28[0], xyf_Top_28[1], xyf_Top_28[2], Baseline[0], Baseline[1], Baseline[2], xyf_Top_30[0], xyf_Top_30[1], xyf_Top_30[2])
plane_Buttom = DET(xyf_Buttom_28[0], xyf_Buttom_28[1], xyf_Buttom_28[2], Baseline[0], Baseline[1], Baseline[2], xyf_Buttom_30[0], xyf_Buttom_30[1], xyf_Buttom_30[2])

print("#Question02")
print("    ")
print("Baseline = ")
print(Baseline)
print("    ")
print("Omega = ")
print(Eul_omega_3028 * 180 / math.pi)
print("    ")
print("Phi = WTF")
print(Eul_phi_3028 * 180 / math.pi)
print("    ")
print("Kappa = WTF")
print(Eul_kappa_3028 * 180 / math.pi)
print("    ")
print("Plane Top = WTF")
print(plane_Top)
print("    ")
print("Plane Buttom = WTF")
print(plane_Buttom)






