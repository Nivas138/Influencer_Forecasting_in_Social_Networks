setwd('C:\\Users\\Nivas\\')
getwd()
# Load library
#install.packages('randomForest')
library(randomForest)
library(caret)
# Help on ramdonForest package and function
#library(help=randomForest)
#help(randomForest)
## Read data
set.seed(138)
termCrosssell<-read.csv(file="m5_fmax_class_final.csv",header = T)
names(termCrosssell)
table(termCrosssell$sent.class)
nrow(termCrosssell)
table(termCrosssell$sent.class)/nrow(termCrosssell)
sample.ind <- sample(3, 
                     nrow(termCrosssell),
                     replace = T,
                     prob = c(0.8,0.2,0.1))
sample.ind
cross.sell.dev <- termCrosssell[sample.ind==1,]
cross.sell.val <- termCrosssell[sample.ind==2,]
cross.sell.dev
cross.sell.val

table(cross.sell.dev$sent.class)/nrow(cross.sell.dev)
table(cross.sell.val$sent.class)/nrow(cross.sell.dev)
class(cross.sell.dev$sent.class)
varNames <- names(cross.sell.dev)
# Exclude ID or Response variable
varNames <- varNames[!varNames %in% c("sent_class")]
varNames
# add + sign between exploratory variables
varNames1 <- paste(varNames, collapse = "+")
varNames1
# Add response variable and convert to a formula object
rf.form <- as.formula(paste("sent.class", varNames1, sep = " ~ "))
rf.form
cross.sell.rf <- randomForest(rf.form,
                              cross.sell.dev,
                              ntree=500,
                              type='classification',
                              importance=T)
cross.sell.rf

#plot(cross.sell.rf,main="Random Forest",xlab="Trees",ylab="Accuracy")
# Variable Importance Plot
#varImpPlot(cross.sell.rf,
#          sort = T,
#          main="Variable Importance",
#         n.var=4)
# Variable Importance Table
var.imp <- data.frame(importance(cross.sell.rf,
                                 type=2))
# make row names as columns
var.imp$Variables <- row.names(var.imp)
var.imp[order(var.imp$MeanDecreaseGini,decreasing = T),]

# Predicting response variable
cross.sell.dev$predicted.response <- predict(cross.sell.rf)

library(e1071)
library(caret)
## Loading required package: lattice
## Loading required package: ggplot2
# Create Confusion Matrix
cf<-confusionMatrix(data=cross.sell.dev$predicted.response,
                    reference=cross.sell.dev$sent.class,
                    positive='yes')

cf

