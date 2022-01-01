import csv
import os
import statistics
import pandas as pd              
import matplotlib.pyplot as plt

#Extracting the value we need and save to another folder
dirpath = 'E:\\Test Data\\Original_Data'
filenames = os.listdir(dirpath)

foldername = 'Reflect_Result_No_Roll'
homedir = os.getcwd()
savedir = dirpath[0:13] + '\\' + foldername

try:
    os.mkdir(foldername)
    os.chdir(foldername)
except OSError:
    os.chdir(foldername)

for fname in filenames:
	if fname[-4] != '.':
		filenames.remove(fname)
		
os.chdir(dirpath)

for fname in filenames:

	if os.path.isdir(fname):
		continue
		
	with open(fname, 'r', newline='') as infile:
		with open(savedir + '/' + fname[0:-4] + '_data.csv', 'w', newline='') as outfile:
		
			rows = csv.reader(infile, delimiter=',')	
			writer = csv.writer(outfile)
			count = 0
	
			for row in rows:
			
				if count < 21:
					if count == 20:
						writer.writerow(['Wavelength(nm)','Intensity(Counts)'])
					pass
					
				else: 	
															#Using '.' to determine the extraction of wavelength/Intensity value
					if (row[0][3]) == '.':
						wavelen = row[0][0:6]
					elif (row[0][4]) == '.':
						wavelen = row[0][0:7]
		
					dot_search = 0
		
					while(count != -1):
					
						if row[0][dot_search] != ' ' :
							if row[0][dot_search-1] == ' ' :
								#print(row[0][dot_search:-1]+row[0][-1])
								intensity = row[0][dot_search:-1]+row[0][-1]
								break
				
						if dot_search < -10:
							break
							
						dot_search -= 1
						
					if float(wavelen)>900.91:				#Give up the value whose wavelength>900.91(maximum of reflection panel)
						break
						
					writer.writerow([float(wavelen),float(intensity)])

				count+=1
				
os.chdir(savedir)

#Caculate Reflecting rate
for fname in filenames:
	
	if os.path.isdir(fname):
		continue
		
	with open('E:/Test Data/standard.csv','r', newline = '')as stdfile:	
		stdcsv = pd.read_csv(stdfile)
		df_std = pd.DataFrame(stdcsv)
		
		with open('Calibration_data.csv','r', newline='') as panelfile:		
			panelcsv = pd.read_csv(panelfile)
			df_panel = pd.DataFrame(panelcsv)
			
			with open(fname[0:-4] + '_data.csv', 'r', newline='') as becalifile:			
				calicsv = pd.read_csv(becalifile)
				df_cali = pd.DataFrame(calicsv)
				
				#Merge panel, clibration, observation data to caculate the reflection rate, then save.
				df_cali.columns = ["wavelength(nm)", 'STD_Int' + fname[0:-4]]
				df_cali = pd.concat([df_std, df_cali, df_panel],axis = 1)
				print(df_cali)
				df_cali['Cali_Reflect'] = df_cali.apply(lambda df_cali: df_cali['Standrad_Reflect']* (df_cali['STD_Int' + fname[0:-4]]/df_cali['Intensity(Counts)']), axis=1)
				
				df_out = df_cali[['wavelength(nm)','Cali_Reflect']]
				df_out.to_csv(fname[0:-4]+'_Reflect.csv', index=0, float_format='%.5f')

#Plot figures (with rolling smoothing)
count = 0
color = ['dimgray', 'indianred', 'limegreen', 'olivedrab', 'sandybrown', 'darkturquoise', 'cyan', 'black', 'magenta', 'coral']

for fname in filenames:	

	if os.path.isdir(fname):
		continue
		
	with open(fname[0:-4]+'_Reflect.csv', 'r', newline='') as infile2:
	
		rows = pd.read_csv(infile2)
		
		#Caculate mean and std
		rows.insert(2, column="mean", value=rows["Cali_Reflect"].mean())
		rows.insert(3, column="plus_std", value=rows["Cali_Reflect"]+rows["Cali_Reflect"].std())
		rows.insert(4, column="minus_std", value=rows["Cali_Reflect"]-rows["Cali_Reflect"].std())
		
		#Draw lines
		plt.style.use("seaborn")
		plt.figure(figsize=(9,6))
		plt.axis('auto')
		
		#Upper/ Lower width setting
		if rows["plus_std"].max()>1: 
			plt.ylim(ymax = 1)	
		else:
			plt.ylim(ymax = rows["plus_std"].max()+0.1*rows["plus_std"].max())
			if rows["plus_std"].max()+0.1*rows["plus_std"].max()>1:
				plt.ylim(ymax = rows["plus_std"].max())
			
		if rows["minus_std"].min()<-0.1: 
			plt.ylim(ymin = -0.1)
		else:
			plt.ylim(ymin = rows["minus_std"].min()-0.1*rows["minus_std"].min())
			if rows["minus_std"].min()-0.1*rows["minus_std"].min()< -0.1:
				plt.ylim(ymin = rows["minus_std"].min())
				
		plt.style.use("seaborn")		
		plt.plot(rows["wavelength(nm)"], rows["Cali_Reflect"],c = "r", linewidth=1.5)
		plt.plot(rows["wavelength(nm)"], rows["mean"],c = "blue", linewidth=1.0)
		plt.plot(rows["wavelength(nm)"], rows["plus_std"],c = "silver", linewidth=1.0,linestyle="--")
		plt.plot(rows["wavelength(nm)"], rows["minus_std"],c = "silver", linewidth=1.0,linestyle="--")
		plt.plot(rows["wavelength(nm)"][rows["Cali_Reflect"].idxmax()],rows["Cali_Reflect"].max(),'^')
		
		#Draw chart
		show_max = ' ('+str(rows["wavelength(nm)"][rows["Cali_Reflect"].idxmax()])+', '+str('%.3f'%(rows["Cali_Reflect"].max()))+')'
		plt.annotate(show_max,xytext=(rows["wavelength(nm)"][rows["Cali_Reflect"].idxmax()],rows["Cali_Reflect"].max()),xy=(rows["wavelength(nm)"][rows["Cali_Reflect"].idxmax()],rows["Cali_Reflect"].max()))
		plt.legend(labels=[fname[0:-4],'mean','plus_std','minus_std'], loc = 'best')
		plt.xlabel("wavelength(nm)", fontweight = "bold")
		plt.ylabel("Reflection_Rate", fontweight = "bold")
		plt.title(fname[0:-4], fontsize = 15, fontweight = "bold", y = 1.1)
		
		#Save chart
		plt.savefig(fname[0:-4] + '.jpg' , bbox_inches='tight', pad_inches=0.0)
		plt.close()
		
df = pd.DataFrame()
count = 0
plt.style.use("seaborn")
plt.figure(figsize=(9,6))
leg = []

#Plot figures (without rolling smoothing)
for fname in filenames:	

	if os.path.isdir(fname):
		continue
	
	if fname[0:2] == 'Ca':
		continue
	
	with open(fname[0:-4]+'_Reflect.csv', 'r', newline='') as infile3:
	
		rows = pd.read_csv(infile3)
		rows.columns = ['wav' + fname[0:-4], 'Reflect' + fname[0:-4]]
		df = pd.concat([df,rows],axis = 1)
		
		#Plot lines
		plt.plot(df['wav' + fname[0:-4]], df['Reflect' + fname[0:-4]],c = color[count], linewidth=1.5)
		plt.plot(df['wav' + fname[0:-4]][df['Reflect' + fname[0:-4]].idxmax()], df['Reflect' + fname[0:-4]].max(),'^')
		
		show_max = ' ('+str(df['Reflect' + fname[0:-4]].idxmax())+', '+str('%.3f'%( df['Reflect' + fname[0:-4]].max()))+')'
		plt.annotate(show_max,xytext=(df['wav' + fname[0:-4]][df['Reflect' + fname[0:-4]].idxmax()], df['Reflect' + fname[0:-4]].max()),xy=(df['wav' + fname[0:-4]][df['Reflect' + fname[0:-4]].idxmax()], df['Reflect' + fname[0:-4]].max()))
		plt.xlabel("Wavelength(nm)", fontweight = "bold")
		plt.ylabel("Reflection_Rate", fontweight = "bold")
		plt.title('Compare', fontsize = 15, fontweight = "bold", y = 1.1)
		plt.xticks(rotation=45)
		leg.append(fname[0:-4])
		leg.append(fname[0:-4]+'_max')
		
		count += 1
		
plt.legend(leg, loc = 'best', ncol = int(count/3))
plt.savefig('Compare' + '.jpg' , bbox_inches='tight', pad_inches=0.0)
plt.close()

df2 = pd.DataFrame()
count = 0	
plt.style.use("seaborn")
plt.figure(figsize=(9,6))
leg2 = []

#Plot simplified figures (with rolling smoothing)
for fname in filenames:	

	if os.path.isdir(fname):
		continue
	
	if fname[0:2] == 'Ca':
		continue
	
	idx = 0
	sum_396_458 = []
	sum_506_586 = []
	sum_624_694 = []
	sum_699_749 = []
	sum_765_901 = []
	sum_442_515 = []
	sum_584_632 = []
	sum_856_1043 = []
	
	Bandlen = [427, 478, 546, 608, 659, 724, 833, 949]
	
	with open(fname[0:-4]+'_Reflect.csv', 'r', newline='') as infile4:
	
		rows = pd.read_csv(infile4)
		rows.columns = ['wav' + fname[0:-4], 'Reflect' + fname[0:-4]]
		df2 = pd.concat([df2,rows],axis = 1)
		
		#Data Simplification
		for item in df2['wav' + fname[0:-4]]:
			
			if 458>float(item)>396 :				
				sum_396_458.append(df2['Reflect' + fname[0:-4]][idx])
			elif 586>float(item)>506:
				sum_506_586.append(df2['Reflect' + fname[0:-4]][idx])
			elif 694>float(item)>624:
				sum_624_694.append(df2['Reflect' + fname[0:-4]][idx])
			elif 749>float(item)>699:
				sum_699_749.append(df2['Reflect' + fname[0:-4]][idx])
			elif 901>float(item)>765:
				sum_765_901.append(df2['Reflect' + fname[0:-4]][idx])
			
			if 515>float(item)>442:
				sum_442_515.append(df2['Reflect' + fname[0:-4]][idx])
			elif 632>float(item)>584:
				sum_584_632.append(df2['Reflect' + fname[0:-4]][idx])
			elif 1043>float(item)>856:
				sum_856_1043.append(df2['Reflect' + fname[0:-4]][idx])
				
			idx += 1
		
		avg_reflect = [statistics.mean(sum_396_458), statistics.mean(sum_442_515), statistics.mean(sum_506_586), statistics.mean(sum_584_632), statistics.mean(sum_624_694), statistics.mean(sum_699_749), statistics.mean(sum_765_901), statistics.mean(sum_856_1043)]
		
		#Plot lines
		plt.plot(Bandlen, avg_reflect, c = color[count], linewidth=1.5)
		plt.xlabel("Wavelength(nm)", fontweight = "bold")
		plt.ylabel("Reflection_Rate", fontweight = "bold")
		plt.title('Compare_Simplified', fontsize = 15, fontweight = "bold", y = 1.1)
		plt.xticks(rotation=45)
		plt.xticks(Bandlen)
		leg2.append(fname[0:-4])
		
		count += 1
		
plt.legend(leg2, loc = 'best', ncol = int(count/3))
plt.savefig('Compare_Simplified' + '.jpg' , bbox_inches='tight', pad_inches=0.0)
plt.close()	

os.chdir(homedir)