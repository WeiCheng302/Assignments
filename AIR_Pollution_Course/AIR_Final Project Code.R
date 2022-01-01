#########################
# Set Working Directory #
#########################

setwd("D:\\GsuiteDirve\\1082_?Ŷ????T?޳N???Ů??ìV???S??????��?? APPLICATION OF GEOSPATIAL INFORMATION TECHNOLOGY ON AIR POLLUTION EXPOSURE ASSESSMENT_?d?v?F\\W13_20200526")

#################
# Load Packages #
#################

install.packages("descriptr")		# advancd way to do stepwise regression
install.packages("olsrr")		# advancd way to do stepwise regression
install.packages("tidyverse")

library("olsrr")
library("car")
library("tidyverse")

##################
# Import Dataset #
##################

dataset <- read.csv("Datebase_with_air_pollution.csv")
# dataset2 <- as.tibble(dataset)
#View(dataset)
summary(dataset)
summary(dataset[,c("PM25","NOx","PM10","O3")]) # The outcome variables are not nuerice format


###################
# Data Management #
###################

# Convert air pollution data (PM2.5) into numeric format #
str(dataset)
dataset$PM25 <- as.numeric(as.character(dataset$PM25))
dataset$NOx <- as.numeric(as.character(dataset$NOx))
dataset$PM10 <- as.numeric(as.character(dataset$PM10))
dataset$O3 <- as.numeric(as.character(dataset$O3))

dataset$restaurant_250 <- as.numeric(as.character(dataset$restaurant_250))
dataset$restaurant_500 <- as.numeric(as.character(dataset$restaurant_500))
dataset$restaurant_750 <- as.numeric(as.character(dataset$restaurant_750))
dataset$restaurant_1000 <- as.numeric(as.character(dataset$restaurant_1000))
dataset$restaurant_1250 <- as.numeric(as.character(dataset$restaurant_1250))
dataset$restaurant_1500 <- as.numeric(as.character(dataset$restaurant_1500))
dataset$restaurant_1750 <- as.numeric(as.character(dataset$restaurant_1750))
dataset$restaurant_2000 <- as.numeric(as.character(dataset$restaurant_2000))

dataset$nightmarket_250 <- as.numeric(as.character(dataset$nightmarket_250))
dataset$nightmarket_500 <- as.numeric(as.character(dataset$nightmarket_500))
dataset$nightmarket_750 <- as.numeric(as.character(dataset$nightmarket_750))
dataset$nightmarket_1000 <- as.numeric(as.character(dataset$nightmarket_1000))
dataset$nightmarket_1250 <- as.numeric(as.character(dataset$nightmarket_1250))
dataset$nightmarket_1500 <- as.numeric(as.character(dataset$nightmarket_1500))
dataset$nightmarket_1750 <- as.numeric(as.character(dataset$nightmarket_1750))
dataset$nightmarket_2000 <- as.numeric(as.character(dataset$nightmarket_2000))

dataset$temple_250 <- as.numeric(as.character(dataset$temple_250))
dataset$temple_500 <- as.numeric(as.character(dataset$temple_500))
dataset$temple_750 <- as.numeric(as.character(dataset$temple_750))
dataset$temple_1000 <- as.numeric(as.character(dataset$temple_1000))
dataset$temple_1250 <- as.numeric(as.character(dataset$temple_1250))
dataset$temple_1500 <- as.numeric(as.character(dataset$temple_1500))
dataset$temple_1750 <- as.numeric(as.character(dataset$temple_1750))
dataset$temple_2000 <- as.numeric(as.character(dataset$temple_2000))

dataset$rest_nimark_250 <- as.numeric(as.character(dataset$rest_nimark_250))
dataset$rest_nimark_500 <- as.numeric(as.character(dataset$rest_nimark_500))
dataset$rest_nimark_750 <- as.numeric(as.character(dataset$rest_nimark_750))
dataset$rest_nimark_1000 <- as.numeric(as.character(dataset$rest_nimark_1000))
dataset$rest_nimark_1250 <- as.numeric(as.character(dataset$rest_nimark_1250))
dataset$rest_nimark_1500 <- as.numeric(as.character(dataset$rest_nimark_1500))
dataset$rest_nimark_1750 <- as.numeric(as.character(dataset$rest_nimark_1750))
dataset$rest_nimark_2000 <- as.numeric(as.character(dataset$rest_nimark_2000))


#### check the x correlation 
allxcor <- cor(dataset[7:ncol(dataset)], method = "spearman")
write.csv(allxcor, file = "allxcor_delete0x-2_spearman.csv")


###############################
# Stepwise Regression Model 	#
# (olsrr Package)			#
###############################

#### Set the varaibles will be used for LUR ####
colnames(dataset)
Y <- colnames(dataset)[7]			# Outcome variable [PM2.5]
X <- colnames(dataset)[8:ncol(dataset)]	# predictors
allX <- paste(X, collapse = "+")		# put all predictors together
allX
as.formula(paste(Y, "~", allX))		# Check formula for linear model

temp <- lm(as.formula(paste(Y, "~", allX)), singular.ok=TRUE, data=dataset)
lmfit <- temp 
lmfit <- update(temp, .~. -season) # for model after adding in air pollution parameters
lmfit <- update(temp, .~. -Ind_house_1500 -nightmarket_1750 -Ind_house_1250 -nightmarket_1250 -temple_750 -temple_500 -NDVI_1000 -Ind_house_1750 -NDVI_750 -NDVI_500 -rest_nimark_250 -Ind_house_1000 -restaurant_250 -temple_1000 -Ind_house_500 -restaurant_500 -temple_1250 -Ind_house_750 -Ind_500 -NDVI_1250 -Ind_house_2000 -NDVI_2000 -temple_1500 -RH) # for final model 1
# lmfit <- update(temp, .~. - nightmarket_1750 - nightmarket_1250 - nightmarket_2000 - nightmarket_1500 - Rd_500 - Ind_house_1500 - restaurant_2000 - NDVI_1000 - restaurant_750 - restaurant_1750 - temple_500 - NDVI_750 - Res_1750 - Res_750 - NDVI_500 - Rd_1250 - Res_1000 - temple_2000 - temple_750 - Res_1000 - temple_2000 - temple_750  - Ind_house_1750) # remove some variables that make model can't converge in stepwise regression
summary(temp)
summary(lmfit)


#### Stepwise regression ####
stepResult <- ols_step_both_p(model=lmfit, pent=0.1, prem=0.3, details=TRUE)
stepResult
summary(stepResult$model)		# Get the final Model

# where
# pent (p-value for entry)
# prem (p-value for remove)
# details (show the stepwise preceure in details)

stepResult$steps 		# how many stpes it used (16 steps)
stepResult$predictors	# Variables in the final model
lmsummary(stepResult$model)$r.squared		#crude R-squared for final model
summary(stepResult$model)$adj.r.squared	#adjusted R-squared for final model


#### Check VIF and Details for final model####
vif(lmfit)
vif(stepResult$model)
as.matrix(sort(vif(stepResult$model)))	# NDVI_2000m and temple_2000 might be correleated
cor(dataset$PM25, dataset$NDVI_1000, method="spearman")	#R=0.97
cor(dataset$NDVI_1750, dataset$temple_1250, method="spearman")	#R=0.97


#### Removed Big VIF variable ###
vifCutoff = 3.0	# Set cutoff of VIF
varBigVif <- vif(stepResult$model)[vif(stepResult$model)>vifCutoff]
BigVifFormula <- as.formula(paste("~. -", paste(names(varBigVif), collapse="-")))
BigVifFormula

oldModel <- formula(stepResult$model) # 14 predictors
newModel <- update(oldModel, BigVifFormula) # 7 predictors remained after removing big VIG variables

finalModel <- lm(newModel, data=dataset)
finalModel2 <- lm(newModel, data=dataset)
summary(finalModel)
vif(finalModel$model)

as.matrix(sort(vif(finalModel)))	# low VIF for each variables
summary(finalModel)$r.squared		#adjusted R-squared for final model
summary(finalModel)$adj.r.squared	#adjusted R-squared for final model
install.packages("helplots")
library("heplots")
etasq(finalModel)				#Partial R-squared for each variable






#######################
#  Regression Model   #
# 		                #
#######################


lmfit <- lm(PM25~PM10+O3+localroad_1000m+allroad_1000m+restaurant_1000
            +rest_temple_1000+pureRA_1000m+industrialRA_1000m+commercialRA_1000m
            +mixRA_1000m+allRA_1000m+paddy_1000m+unlandrice_1000m+NDVI_250m,singular.ok = TRUE,dataset)
summary(lmfit)



############################
# Correlation and P-value  #
#   (Hmisc Package)        #
############################

install.packages("Hmisc") 
library("Hmisc")

str(dataset)                   
states <- dataset[,8:79]                                   #Database 8 to 79 behavior  
View(states)                     

data <- rcorr(as.matrix(states))                           #Correlation , sample, Pvalue
## ? why transform to matrix first then data frame??
data2 <- data.frame(c(data))        
View(data2)
write.table(data2,file="data_corr.csv",sep=",",row.names=F, na = "NA") # export the result as a CSV file


###############################
# Stepwise Regression Model   #
# (olsrr Package)	            #
###############################


#### Set the varaibles will be used for LUR ####
##    Create a full and null linear models    ##

lm.fullmodel = lm(PM25~PM10+O3+localroad_1000m+allroad_1000m+restaurant_1000
                  +rest_temple_1000+pureRA_1000m+industrialRA_1000m+commercialRA_1000m
                  +mixRA_1000m+allRA_1000m+paddy_1000m+unlandrice_1000m+NDVI_1000m,singular.ok = TRUE,dataset)



#### Stepwise regression ####
step1 <- ols_step_both_p(model=lm.fullmodel, pent=0.1, prem=0.3, details=TRUE)

# where
# pent (p-value for entry)
# prem (p-value for remove)
# details (show the stepwise preceure in details)


step2 <- update(lm.fullmodel, ~. -  localroad_1000m )
step2 <- ols_step_both_p(model=step2, pent=0.1, prem=0.3, details=TRUE)

step3 <- update(lm.fullmodel, ~. -  localroad_1000m -restaurant_1000) 
step3 <- ols_step_both_p(model=step3, pent=0.1, prem=0.3, details=TRUE)


step4 <- update(lm.fullmodel, ~. -localroad_1000m -restaurant_1000 -rest_temple_1000 )
step4 <- ols_step_both_p(model=step4, pent=0.1, prem=0.3, details=TRUE)

step5 <- update(lm.fullmodel, ~. -  localroad_1000m -restaurant_1000 -rest_temple_1000 -mixRA_1000m )
step5 <- ols_step_both_p(model=step5, pent=0.1, prem=0.3, details=TRUE)


step6 <- update(lm.fullmodel, ~. -  localroad_1000m -restaurant_1000 -rest_temple_1000 -mixRA_1000m -industrialRA_1000m )  
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

stepResult <- lm(PM25~PM10+allRA_1000m+O3+allroad_1000m ,singular.ok = TRUE,dataset)
stepResult <- ols_step_both_p(model=stepResult, pent=0.1, prem=0.3, details=TRUE)
stepResult 
vif(stepResult$model)



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

write.table(varResult,file="D:\\Air_pollution_class\\C9\\2020_C9\\varResult.csv",sep=",",row.names=F, na = "NA") # export the result as a CSV file



