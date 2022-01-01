#########################
# Set Working Directory #
#########################

setwd("C:\\Users\\theo\\Desktop\\C9\\All")

#################
# Load Packages #
#################

library("olsrr")
library("car")

##################
# Import Dataset #
##################

dataset <- read.csv("Finaldata_PR_delete.csv")
View(dataset)
summary(dataset)
summary(dataset[,c("SO2")]) # The outcome variables are not nuerice format


###################
# Data Management #
###################

# Convert air pollution data (PM2.5) into numeric format #
str(dataset)
dataset$SO2 <- as.numeric(as.character(dataset$SO2))

#######################
#  Regression Model   #
#######################


#lmfit <- lm(PM25~PM10+O3+localroad_1000m+allroad_1000m+restaurant_1000
 #           +rest_temple_1000+pureRA_1000m+industrialRA_1000m+commercialRA_1000m
  #          +mixRA_1000m+allRA_1000m+paddy_1000m+unlandrice_1000m+NDVI_250m,singular.ok = TRUE,dataset)
#summary(lmfit)

############################
# Correlation and P-value  #
#(Hmisc Package)           #
############################

library("Hmisc")

str(dataset)                   
states <- dataset[,4:44]                                   #Database 8 to 79 behavior  
View(states)                     

data <- rcorr(as.matrix(states))                           #Correlation , sample, Pvalue  
data2 <- data.frame(c(data))        
View(data2)
write.table(data2,file="C:\\Users\\theo\\Desktop\\C9\\All\\data_corr.csv",sep=",",row.names=F, na = "NA") # export the result as a CSV file


###############################
# Stepwise Regression Model   #
# (olsrr Package)	            #
###############################


#### Set the varaibles will be used for LUR ####
##    Create a full and null linear models    ##

lm.fullmodel = lm(SO2~City_Lvl+Industrial_1500
                  +Industrial_1750+Industrial_2000+River_750+River_1000+River_1250+River_1500
                  +River_1750+River_2000+Resident_250+Resident_500+Resident_750+Resident_1000
                  +X2013_017+X2013_097+X2013_193+X2013_289+scenic_500+scenic_750+scenic_1000+scenic_1250
                  +scenic_1500+scenic_1750+scenic_2000+temple_500+temple_750+temple_2000,singular.ok = TRUE,dataset)
summary(lm.fullmodel)


#### Stepwise regression ####
step1 <- ols_step_both_p(model=lm.fullmodel, pent=0.1, prem=0.3, details=TRUE)

# where
# pent (p-value for entry)
# prem (p-value for remove)
# details (show the stepwise preceure in details)

step2 <- update(lm.fullmodel, ~. -  Industrial_1500 -Industrial_1750 -River_1000 -River_1250
                -River_1500 -River_1750 -River_2000 -Resident_500 -Resident_750 -Resident_1000
                -X2013_097 -X2013_289 -scenic_500 -scenic_1500 -scenic_1750 -scenic_2000 -temple_750
                -scenic_750)
step2 <- ols_step_both_p(model=step2, pent=0.1, prem=0.3, details=TRUE)

step3 <- update(lm.fullmodel, ~. -  Industrial_1500 -Industrial_1750 -River_1000 -River_1250
                -River_1500 -River_1750 -River_2000 -Resident_500 -Resident_750 -Resident_1000
                -X2013_097 -X2013_289 -scenic_500 -scenic_1500 -scenic_1750 -scenic_2000 -temple_750
                -scenic_750 -temple_500 ) 
step3 <- ols_step_both_p(model=step3, pent=0.1, prem=0.3, details=TRUE)


step4 <- update(lm.fullmodel, ~. -  Industrial_1500 -Industrial_1750 -River_1000 -River_1250
                -River_1500 -River_1750 -River_2000 -Resident_500 -Resident_750 -Resident_1000
                -X2013_097 -X2013_289 -scenic_500 -scenic_1500 -scenic_1750 -scenic_2000 -temple_750
                -temple_2000 -temple_500 -scenic_1000)
step4 <- ols_step_both_p(model=step4, pent=0.1, prem=0.3, details=TRUE)

step5 <- update(lm.fullmodel, ~. -  Industrial_1500 -Industrial_1750 -River_1000 -River_1250
                -River_1500 -River_1750 -River_2000 -Resident_500 -Resident_750 -Resident_1000
                -X2013_097 -X2013_289 -scenic_500 -scenic_1500 -scenic_1750 -scenic_2000 -temple_750
                -temple_2000 -temple_500 -scenic_1000 -scenic_750)
step5 <- ols_step_both_p(model=step5, pent=0.1, prem=0.3, details=TRUE)


step6 <- update(lm.fullmodel, ~. -  Industrial_1500 -Industrial_1750 -River_1000 -River_1250
                -River_1500 -River_1750 -River_2000 -Resident_500 -Resident_750 -Resident_1000
                -X2013_097 -X2013_289 -scenic_500 -scenic_1500 -scenic_1750 -scenic_2000 -temple_750
                -temple_2000 -temple_500 -scenic_1000 -scenic_750 -X2013_193)  
step6 <- ols_step_both_p(model=step6, pent=0.1, prem=0.3, details=TRUE)

plot(step6)

#################################
# Variance Inflation Factorin   #
# (car Package)	              #
#################################


vif(step6$model)



###################
### final model ###
###################

stepResult <- lm(SO2~Industrial_2000+scenic_1250+City_Lvl+Resident_250+X2013_017+River_750 ,singular.ok = TRUE,dataset)
stepResult <- ols_step_both_p(model=stepResult, pent=0.1, prem=0.3, details=TRUE)
stepResult 
vif(stepResult$model)

lm.fullmodel2 = lm(SO2~Industrial_2000+scenic_1250+City_Lvl+Resident_250+X2013_017+River_750,singular.ok = TRUE,dataset)
summary(lm.fullmodel2)


####

stepResult$steps 		# how many stpes it used
stepResult$predictors	# Variables in the final model

stepResult$rsquare	# R-squared for each step
stepResult$adjr		# adjusted R-squared for each step
stepResult$aic		# AIC for each step
stepResult$rmse		# RMSE for each step

plot(stepResult)		# See how model performance changed in each step


#### Extract and Output Variable/Coefficient/P-value ####


varCoef <- stepResult$model$coefficient 				# Extract Variable/Coeeficients for each variables
varPvalue <- coef(summary(stepResult$model))[,"Pr(>|t|)"]	# Extract P-value for each variables

varResult <- cbind(varCoef, varPvalue)
colnames(varResult) <- c("Coefficient", "Pvalue")
varResult

write.table(varResult,file="C:\\Users\\theo\\Desktop\\C9\\All\\varResult.csv",sep=",",row.names=F, na = "NA") # export the result as a CSV file





