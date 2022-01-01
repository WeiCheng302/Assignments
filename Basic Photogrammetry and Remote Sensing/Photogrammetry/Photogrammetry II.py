#HW3-1

#Question01

PixelSize = 0.000006
F_mm = 0.1005

def parallex(XA1, XA2):
    UA1 = (XA1 - 11310/2)*PixelSize
    UA2 = (XA2 - 11310/2)*PixelSize
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

H_Top = parallex_H(parallex_Top, Baseline, H, F_mm)
H_Buttom = parallex_H(parallex_Buttom, Baseline, H, F_mm)

print("    ")
print("Homework 3")
print("#Question01")
print("    ")
print("Baseline = ")
print(Baseline)
print("    ")
print("Baseline/ Height = ")
print(Baseline/H)
print("    ")
print("Parallex Top / Parallex Buttom = ")
print(parallex_Top, parallex_Buttom)
print("    ")
print("Building Height = ")
print((H_Top - H_Buttom))
#==================================================================================#

#Question02

Omega28 = 354.035 * math.pi / 180
Phi28 = 353.098 * math.pi / 180
Kappa28 = 322.358 *  math.pi / 180 
EOP28 = np.array([169316.359, 2544469.908, 1727.712]).T

Omega30 = 353.447  * math.pi / 180
Phi30 = 354.961 * math.pi / 180
Kappa30 = 322.252 * math.pi / 180
EOP30 = np.array([169571.460, 2544279.421, 1722.203 ]).T

Rot28 = Rotation_Mat(Omega28, Phi28, Kappa28)
Rot30 = Rotation_Mat(Omega30, Phi30, Kappa30)
Rot30to28 = Rot28.dot(Rot30.T)

Baseline = ((EOP28[0]-EOP30[0])**2 + (EOP28[1]-EOP30[1])**2 + (EOP28[2]-EOP30[2])**2)**0.5
Vec_Baseline = np.array([EOP30[0]-EOP28[0], EOP30[1]-EOP28[1], EOP30[2]-EOP28[2] ])

Eul_omega_3028 = math.atan2(-Rot30to28[2,1],Rot30to28[2,2])
Eul_phi_3028 = math.atan2(Rot30to28[2,0],(Rot30to28[2,2]**2 + Rot30to28[2,1]**2)**0.5)
Eul_kappa_3028 = math.atan2(-Rot30to28[1,0],Rot30to28[0,0])

PixTop28 = Pix2Cam(Top28[0], Top28[1], 0.00006)
PixTop30 = Pix2Cam(Top30[0], Top30[1], 0.00006)
PixButtom28 = Pix2Cam(Buttom28[0], Buttom28[1], 0.00006)
PixButtom30 = Pix2Cam(Buttom30[0], Buttom30[1], 0.00006)

def DET(a,b,c,d,e,f,g,h,i):
    return a*e*i + d*h*c + b*f*g - c*e*g - a*h*f - b*d*i

def CoPlane(a, b, c):
    return a.dot(np.cross(b,c))

plane_Top = CoPlane(PixTop28, Vec_Baseline, PixTop30)		
plane_Buttom = CoPlane(PixButtom28, Vec_Baseline, PixButtom30)

print("    ")
print("#Question02")
print("    ")
print("Omega = ")
print(Eul_omega_3028 * math.pi / 180)
print("    ")
print("Phi = ")
print(Eul_phi_3028 * math.pi / 180)
print("    ")
print("Kappa = ")
print(Eul_kappa_3028 * math.pi / 180)
print("    ")
print("Baseline = ")
print(Baseline)
print(Vec_Baseline)
print("    ")
print("Plane Top = WTF")
print(plane_Top)
print("    ")
print("Plane Buttom = WTF")
print(plane_Buttom)
#==================================================================================#

#Question03

DLT28 = DLT(EOP28, Rot28, -0.000183, 0.000003, 0.1005, 0.000006)
DLT30 = DLT(EOP30, Rot30, -0.000183, 0.000003, 0.1005, 0.000006)

def DLT_Space_Intersect(DLT1, DLT2, co1x, co1y, co2x, co2y):
    A = np.array([[DLT1[0,0]-co1x*DLT1[2,0], DLT1[0,1]-co1x*DLT1[2,1], DLT1[0,2]-co1x*DLT1[2,2], DLT1[0,3]],
                  [DLT1[1,0]-co1y*DLT1[2,0], DLT1[1,1]-co1y*DLT1[2,1], DLT1[1,2]-co1y*DLT1[2,2], DLT1[1,3]],
                  [DLT2[0,0]-co2x*DLT2[2,0], DLT2[0,1]-co2x*DLT2[2,1], DLT2[0,2]-co2x*DLT2[2,2], DLT2[0,3]],
                  [DLT2[1,0]-co2y*DLT2[2,0], DLT2[1,1]-co2y*DLT2[2,1], DLT2[1,2]-co2y*DLT2[2,2], DLT2[1,3]]])
    L = np.array([co1x, co1y, co2x, co2y]).T
	
    return np.linalg.inv(A.T.dot(A)).dot(A.T).dot(L)
	
DLT_Space_Buttom = DLT_Space_Intersect(DLT28, DLT30, Buttom28[0], Buttom28[1], Buttom30[0], Buttom30[1])
DLT_Space_Top = DLT_Space_Intersect(DLT28, DLT30, Top28[0], Top28[1], Top30[0], Top30[1])

print("    ")
print("#Question03")
print("    ")
print(DLT_Space_Top[2] - DLT_Space_Buttom[2])

def Collinearity_Space_Intersect(E01, E02, RotM1, RotM2, f, x1, y1, x2, y2):
    
    h = 15	
    X0 = np.array([0, 0, 0]).T

    Scale1 = f/(E01[2] - h)
    Scale2 = f/(E02[2] - h)
    SR1 = Scale1*RotM1
    SR2 = Scale2*RotM2
    A = np.array([[SR1[0,0], SR1[0,1], SR1[0,2]],
                  [SR1[1,0], SR1[1,1], SR1[1,2]],
                  [SR1[2,0], SR1[2,1], SR1[2,2]],
                  [SR2[0,0], SR2[0,1], SR2[0,2]],
                  [SR2[1,0], SR2[1,1], SR2[1,2]],
                  [SR2[2,0], SR2[2,1], SR2[2,2]]])
    SRE0xyf1 = SR1.dot(E01) + np.array([x1,y1, -f]).T
    SRE0xyf2 = SR2.dot(E02) + np.array([x2,y2, -f]).T
    L = np.array([SRE0xyf1[0], SRE0xyf1[1], SRE0xyf1[2], SRE0xyf2[0], SRE0xyf2[1], SRE0xyf2[2]]).T
    Xp = np.linalg.inv((A.T).dot(A)).dot(A.T).dot(L)
	V = A.dot(Xp) - L

    while(np.linalg.norm(V ord = 2) > 1):
        h = Xp[2]
        Scale1 = f/(E01[2] - h)
        Scale2 = f/(E02[2] - h)
        SR1 = Scale1*RotM1
        SR2 = Scale2*RotM2
        A = np.array([[SR1[0,0], SR1[0,1], SR1[0,2]],
                      [SR1[1,0], SR1[1,1], SR1[1,2]],
                      [SR1[2,0], SR1[2,1], SR1[2,2]],
                      [SR2[0,0], SR2[0,1], SR2[0,2]],
                      [SR2[1,0], SR2[1,1], SR2[1,2]],
                      [SR2[2,0], SR2[2,1], SR2[2,2]]])
					  
        SRE0xyf1 = SR1.dot(E01) + np.array([x1,y1, -f]).T
        SRE0xyf2 = SR2.dot(E02) + np.array([x2,y2, -f]).T
        L = np.array([SRE0xyf1[0],
                      SRE0xyf1[1],
                      SRE0xyf1[2],
                      SRE0xyf2[0],
                      SRE0xyf2[1],
                      SRE0xyf2[2]])
					  
        Xp = np.linalg.inv((A.T).dot(A)).dot(A.T).dot(L).T
        h = Xp[2]

        print(Xp)
		
    return Xp

#間接觀測平差，需求ENH修正數，對共線方程式偏微分，放棄
#Col_Space_Top = Collinearity_Space_Intersect(EOP28, EOP30, Rot28, Rot30, 0.1005, Top28[0], Top28[1], Top30[0], Top30[1])
#Col_Space_Buttom = Collinearity_Space_Intersect(EOP28, EOP30, Rot28, Rot30, 0.1005, Buttom28[0], Buttom28[1], Buttom30[0], Buttom30[1])

#print(Col_Space_Top)
#print(Col_Space_Buttom)
#==================================================================================#