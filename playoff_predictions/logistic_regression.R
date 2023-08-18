# Author: Isabella Carlos
# Date: Apr 9, 2023
# Purpose: Fit a robust logistic regression on round 1 NBA playoffs 2022-23
# 

# Libraries
library(vtreat)
library(MLmetrics)
library(pROC)
library(ggplot2)
library(dplyr)

# Data IO
modelingDF1 <- read.csv('nba_all_rounds_2022.csv')
head(modelingDF1)
str(modelingDF1)
unique(modelingDF1$SEASON)

# Remove teams that were out playoffs
modelingDF1 <- modelingDF1[!grepl(2, modelingDF1$ROUND1),]
unique(modelingDF1$ROUND1)
str(modelingDF1)
modelingDF1$ROUND1 <- as.logical(modelingDF1$ROUND1)
str(modelingDF1)

# Getting the max value for seed
max(modelingDF1$SEED)

# Transforming seed in ordinary
modelingDF1$SEED <- factor(modelingDF1$SEED, order = T, levels = 8:1)
head(modelingDF1$SEED,33)

# Identify the informative and target
names(modelingDF1)
targetVar       <- names(modelingDF1)[4]
informativeVars <- names(modelingDF1)[c(3, 11:36)] # model without seed: names(modelingDF)[c(7:20)]

#### SAMPLE
# Segment the prep data
set.seed(1234)
idx         <- sample(1:nrow(modelingDF1),.1*nrow(modelingDF1))
prepData    <- modelingDF1[idx,]
nonPrepData <- modelingDF1[-idx,]
nameKeeps <- modelingDF1$TEAMNAME[-idx] #tracking team name for later

# Design a "C"ategorical variable plan 
plan <- designTreatmentsC(prepData, 
                          informativeVars,
                          targetVar, 1)

# Apply to xVars
treatedX <- prepare(plan, nonPrepData)

#### MODIFY Further
# Partition to avoid over fitting
set.seed(2022)
idx        <- sample(1:nrow(treatedX),.8*nrow(treatedX))
train      <- treatedX[idx,]
validation <- treatedX[-idx,]

#### MODEL
# Fit a logistic regression model
fit <- glm(ROUND1 ~., data = train, family ='binomial')
summary(fit)

# Backward Variable selection to reduce chances of multi-colinearity
bestFit <- step(fit, direction='backward')
#saveRDS(bestFit, 'bestFit.rds')
summary(bestFit)


# Feature Importance
coef_df <- data.frame(feature = names(bestFit$coefficients)[-1], importance = abs(bestFit$coefficients[-1]))
# Sort the data frame by importance in descending order
coef_df <- coef_df %>% arrange(desc(importance))

# Plot the feature importance using a bar plot
ggplot(data = coef_df, aes(x = reorder(feature, -importance),
                           y = importance, fill = importance)) +
  geom_bar(stat = "identity", width = 0.5) +
  coord_flip() +
  theme_minimal() +
  labs(title = "Feature Importance Plot", x = "Feature", y = "Importance")



# Compare model size
length(coefficients(fit))
length(coefficients(bestFit))

# Get predictions
teamPreds <- predict(bestFit,  validation, type='response')
tail(teamPreds)

# Classify 
cutoff      <- 0.5
teamClasses <- ifelse(teamPreds >= cutoff, 1,0)

#### ASSESS
# Organize w/Actual
results <- data.frame(actual  = nonPrepData[-idx,]$ROUND1,
                      team    = nonPrepData[-idx,]$TEAMNAME,
                      seed    = nonPrepData[-idx,]$SEED,
                      classes = teamClasses,
                      probs   = teamPreds)
head(results)

# Get a confusion matrix
(confMat <- ConfusionMatrix(results$classes, results$actual))

# What is the accuracy?
sum(diag(confMat)) / sum(confMat)
Accuracy(results$classes, results$actual)

# Visually how well did we separate our classes?
ggplot(results, aes(x=probs, color=as.factor(actual))) +
  geom_density() + 
  geom_vline(aes(xintercept = cutoff), color = 'darkgreen')






################## TESTING SET ################## 

nbaTest <- read.csv('nba_all_rounds_2022_test2.csv')
names(nbaTest)
head(nbaTest, 10)
str(nbaTest)

# Remove teams that were out playoffs
nbaTest <- nbaTest[!grepl(2, nbaTest$ROUND1),]
unique(nbaTest$ROUND1)
nbaTest$ROUND1 <- as.logical(nbaTest$ROUND1)
str(nbaTest)

# Getting the max value for seed
max(nbaTest$SEED)

# Transforming seed in ordinary
nbaTest$SEED <- factor(nbaTest$SEED, order = T, levels = 10:1)
head(nbaTest$SEED,33)

# Get predictions
testTable <- prepare(plan, nbaTest)
testPred <- predict(bestFit,  testTable, type='response')
tail(testPred)

# Classify 
cutoff      <- 0.5
teamClasses <- ifelse(testPred >= cutoff, 1,0)

# Organize w/Actual
results <- data.frame(conference  = nbaTest$CONFERENCE,
                      team    = nbaTest$TEAMNAME,
                      seed    = nbaTest$SEED,
                      classes = teamClasses,
                      probs   = testPred)
head(results)

results <- results[order(-results$probs),]
head(results, 100)

# Exporting table
setwd("C:/Users/Isabella/Downloads")
write.csv(results, file = "nbaRound1.csv", row.names = FALSE)
