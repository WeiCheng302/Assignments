import csv
import random
import numpy as np
import pandas as pd
import scipy
from scipy import stats

def Correlation(a,b):
    sigma = 0
    count = 0
    std_a = a.std()
    std_b = b.std()
    for item in a :
        sig = (item-(sum(a)/len(a)))*(b[count]-(sum(b)/len(b)))
        sigma = sigma + sig
        count += 1

    r = sigma/((count-1)*(std_a*std_b))
    return r

def MinMaxNormalization(a, b, Upper_Value, Lower_Value):
    amax = a.max()
    amin = a.min()
    bmax = b.max()
    bmin = b.min()
    normalized1 = []
    normalized2 = []
    
    for item in a:
        normalized = (item-amin)*(Upper_Value-Lower_Value)/(amax-amin) + Lower_Value
        normalized1.append(normalized)  
        
    for item in b:
        normalized = (item-bmin)*(Upper_Value-Lower_Value)/(bmax-bmin) + Lower_Value
        normalized2.append(normalized)

    Random_df['Normalized1'] = normalized1
    Random_df['Normalized2'] = normalized2
    return 0
def EqualWidthBin(a, b, num_of_bins):
    amax = a.max()
    amin = a.min()
    bmax = b.max()
    bmin = b.min()
    alable = []
    blable = []
    awidth = (amax - amin)/num_of_bins
    bwidth = (bmax - bmin)/num_of_bins
    
    for item in a:
        if float((item -amin)/awidth) < 1:
            alable.append('Low')
        elif float((item-amin)/awidth) > 2:
            alable.append('High')            
        else:
            alable.append('Medium')
      
    for item in b:
        if float((item-bmin)/bwidth) < 1:
            blable.append('Low')
        elif float((item-bmin)/bwidth) > 2:
            blable.append('High')
        else:
            blable.append('Medium')
    
    Random_df['Equalwidtha'] = alable
    Random_df['Equalwidthb'] = blable
    Random_df[['Equalwidtha','Equalwidthb']]
    return alable, blable
def Entropy(labels):
    pass
    probs = pd.Series(labels).value_counts() / len(labels)
    entropy = stats.entropy(probs, base = 2)
    return entropy
def Gain(data,str1,str2):
    ent1 = data.groupby(str1).apply(lambda x:Entropy(x[str2]))
    prob1 = pd.value_counts(data[str1]) / len(data[str1])
    ent2 = sum(ent1 * prob1)
    
    return Entropy(data[str2]) - ent2
def ChiSquare(stra, strb):
    obs = Selected_Feature[[stra, strb]]   
    return scipy.stats.chi2_contingency(obs, correction = False)

# Data Aligning
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# Import Files
Import_Data = pd.read_csv('P66049133_Data_Mining_Data.csv')
Data_Size = len(Import_Data)-1

# Create Random Number and Append Therandom Base on the Random Number
Random_Choose_Number = random.choices(range(Data_Size),k=10)
Random_Data = []
Used_Column = Import_Data[Import_Data.columns[0:-1]].values
for number in Random_Choose_Number:
    Random_Data.append(Used_Column[Random_Choose_Number])

# Create DataFrame
Name = ['Time', 'Sexual', 'Age', 'LivingCity', 'MoneyMonthly','Education','Job','Distance Work','Rent','Way Prefer','TimeSpend Daily','CostDaily','Way Like','Way Want','Like Ur way?','TooMuch Time?','Cost TooMuch?','Move LowerCost?','Want Change Way?','Good CityPBTrans?','Wish better PB Offer?']
Count = ['0','1','2','3','4','5','6','7','8','9']
Random_df = pd.DataFrame(Random_Data[1], index = Count,  columns = Name)
Selected_Feature = Random_df[['Sexual','LivingCity','Way Prefer','Want Change Way?','Wish better PB Offer?']]
print(' ')
print('Table of Selected Feature and Numericted Nominal：')
print(' ')
print(Selected_Feature)
print(' ')

# Create DataFrame and Column Selection
Numeric_Column_1 = Random_df['Want Change Way?']
Numeric_Column_2 = Random_df['Wish better PB Offer?']

# Numeric Normalization
MinMaxNormalization(Numeric_Column_1, Numeric_Column_2, 1, 0)

# Equal Width Binning
EqualWidthBin(Numeric_Column_1, Numeric_Column_2, 3)

# Nominal Preporcessing
Sexual_Numeric = []
LivingCity_Numeric = []
WayPrefer_Numeric = []
Eqwida_Numric = []
Eqwidb_Numric = []

for item in Random_df['Sexual']:
    if item == '男':
        Sexual_Numeric.append(1)
    elif item == '女':
        Sexual_Numeric.append(-1)
    else :
        Sexual_Numeric.append(0)
for item in Random_df['LivingCity']:
    if item == '台北市' : #有捷運 最發達大眾運輸
        LivingCity_Numeric.append(100)
    elif item == '新北市':
        LivingCity_Numeric.append(90)
    elif item == '桃園市':
        LivingCity_Numeric.append(80)
    elif item == '基隆市':
        LivingCity_Numeric.append(70)
    elif item == '宜蘭縣':
        LivingCity_Numeric.append(70)
    elif item == '新竹市':
        LivingCity_Numeric.append(50)
    elif item == '苗栗市':
        LivingCity_Numeric.append(50)
    elif item == '台南市':
        LivingCity_Numeric.append(60)
    elif item == '屏東線':
        LivingCity_Numeric.append(60)
    elif item == '高雄市': #有捷運 
        LivingCity_Numeric.append(80)
    elif item == '台中市':
        LivingCity_Numeric.append(80)
    elif item == '彰化縣':
        LivingCity_Numeric.append(60)
    elif item == '雲林縣':
        LivingCity_Numeric.append(50)
    elif item == '嘉義縣':
        LivingCity_Numeric.append(50)
    else:
        LivingCity_Numeric.append(1)
for item in Random_df['Way Prefer']   :
    list = [1,1,1,1,1,1,1,1,1,1]
    result = 1
    count = 0
    count2 = 0

    for smallitem in item:
        if smallitem == '走':
            list[0] = 2
        elif smallitem == '公':
            list[1] = 3
        elif smallitem == '捷':
            list[2] = 5
        elif smallitem == '機':
            count = 1
        elif count == 1:
            if smallitem == '車':
                list[3] = 7
        elif smallitem == '汽':
            list[4] = 11
        elif smallitem == '火':
            list[5] = 13
        elif smallitem == '高':
            list[6] = 17
        elif smallitem == '飛':
            list[7] = 19
        elif smallitem == '直':
            list[8] = 23
        elif smallitem == '其':
            list[9] = 29    

    for item in list:
        result = result*item        
        count2 += 1

        if count2 == len(list):
            WayPrefer_Numeric.append(result)
            break   
for item in Random_df['Equalwidtha']:
    if item == 'High':
        Eqwida_Numric.append(1)
    elif item == 'Low':
        Eqwida_Numric.append(-1)
    else :
        Eqwida_Numric.append(0)
for item in Random_df['Equalwidthb']:
    if item == 'High':
        Eqwidb_Numric.append(1)
    elif item == 'Low':
        Eqwidb_Numric.append(-1)
    else :
        Eqwidb_Numric.append(0)

Random_df['Sexual_Numeric'] = Sexual_Numeric
Random_df['LivingCity_Numeric'] = LivingCity_Numeric
Random_df['WayPrefer_Numeric'] = WayPrefer_Numeric
Random_df['Eqwida_Numric'] = Eqwida_Numric
Random_df['Eqwidb_Numric'] = Eqwidb_Numric
Selected_Feature = Random_df[['Sexual','Sexual_Numeric','LivingCity','LivingCity_Numeric','Way Prefer','WayPrefer_Numeric','Want Change Way?','Normalized1','Equalwidtha','Eqwida_Numric','Wish better PB Offer?','Normalized2','Equalwidthb','Eqwidb_Numric']]

# Table Showing
print('Table of Selected Feature and Numericted Nominal：')
print(' ')
print(Selected_Feature)
print(' ')

# Correlation Coefficient
print('Correlation Coefficient between Want Change Way? and Wish better PB Offer? = ',Correlation(Numeric_Column_1,Numeric_Column_2))
print(' ')

# Chi Square
print('Chi-Sauare Value of Living City = ',ChiSquare('LivingCity_Numeric','WayPrefer_Numeric'))
print(' ')

# Information Gain
print('Information Gain of Sexual_Numeric and Want Change Way? = ',Gain(Selected_Feature,'Sexual_Numeric','Eqwida_Numric'))
print('Information Gain of LivingCity and Want Change Way? = ',Gain(Selected_Feature,'LivingCity_Numeric','Eqwida_Numric'))
print('Information Gain of WayPrefer and Want Change Way? = ',Gain(Selected_Feature,'WayPrefer_Numeric','Eqwida_Numric'))
print('Information Gain of Wish better PB Offer? and Want Change Way? = ',Gain(Selected_Feature,'Eqwidb_Numric','Eqwida_Numric'))
print(' ')