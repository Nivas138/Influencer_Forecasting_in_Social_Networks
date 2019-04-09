setwd('C:\\Users\\Nivas\\')
getwd()
#install.packages('RWeka')
#install.packages('party')
#install.packages('partykit')
#install.packages('mvtnorm')

#setRepositories('mvtnorm')
library(RWeka)
#library(ggplot2)
#library(party)
#library(partykit)
library(MASS)
library(rpart)
termCrosssell<-read.csv(file="m5_rtmax_class_final.csv",header = T)
str(termCrosssell)
m1 <- J48(termCrosssell$sent.class ~., data = termCrosssell)
if(require("party", quietly = TRUE))plot(m1)
s<-summary(m1)
s$details  #Retrieves all the fields of summary 
Accuracy<-s$details[1] #Retrieves the pctCorrect(Correctly classified Instances %)
Accuracy
gsub(".* ","",Accuracy) #To remove the text "pctCorrect"
Accuracypercent = as.double(Accuracy) #To convert the value to numeric
Accuracypercent

