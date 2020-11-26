###Run Me First
setwd("C:/Users/nates/Documents/Projects/AirBnb_Scrape")
detailed_listings = read.csv("l1_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE)
library(dplyr)
library(ggplot2)
library(corrplot)
library(caret)
library(lubridate)
library(ISLR)
library(glmnet)
detailed_listings$created_at = ymd_hms(detailed_listings$created_at)
detailed_listings$updated_at = ymd_hms(detailed_listings$updated_at)


###########################
##Multi-Colinearity Check##
###########################

nums <- unlist(lapply(detailed_listings, is.numeric)) 
cors = data.frame(cor(detailed_listings[,nums], use = "complete.obs"))

############################
##Missing Value Imputation##
############################

missings = data.frame()
cols = colnames(detailed_listings)
missings[cols] <- list(character())
missings[1,] = colSums(is.na(detailed_listings))

missings = data.frame(name = names(colSums(is.na(detailed_listings))),
                      missing = colSums(is.na(detailed_listings)))
missings = missings %>%
  filter(missing>0)%>%
  arrange(missing)

subset <- t(data.frame(missings$missing))
barplot(subset, legend = c("missing"), names.arg=missings$name, beside=TRUE)

####Check In Time
detailed_listings %>%
  ggplot(aes(x = check_in_time)) + 
  facet_grid(~ X24.hour.check.in) +
  geom_histogram() +
  ggtitle("Check In Time by 24-Hour
          Check In Availability") + 
  xlab("Check In Time")

detailed_listings %>%
  group_by(X24.hour.check.in) %>%
  summarise(missing = sum(is.na(check_in_time))/n() )

###Check Out Time
detailed_listings %>%
  ggplot(aes(x = check_out_time)) + 
  geom_histogram() +
  ggtitle("Distribution of Check Out Times") + 
  xlab("Check Out Time (24 Hr)") +
  xlim(0,24)

detailed_listings %>%
  group_by(check_out_time)%>%
  summarise(count = n())

###Locale
detailed_listings %>%
  ggplot(aes(x = locale)) + geom_bar(stat = "count")

detailed_listings %>%
  group_by(locale)%>%
  summarise(count = n())

##Has_Agreed_to_Legal_Terms
detailed_listings %>%
  ggplot(aes(x = has_agreed_to_legal_terms)) + 
  geom_bar(stat = "count")

detailed_listings %>%
  group_by(has_agreed_to_legal_terms)%>%
  summarise(count = n())

###Language
detailed_listings %>%
  ggplot(aes(x = language)) + 
  geom_bar(stat = "count")

detailed_listings %>%
  group_by(language)%>%
  summarise(count = n())

charter = function(df){
  for (i in colnames(df)){
    if(class(df[[i]]) == "integer"){
      print(ggplot(data = df, aes(x = df[[i]])) + 
              geom_histogram() + 
              ggtitle(paste('Distribution of', colnames(df)[i], sep=' '))
      )
    }
    else{
      print(class(df[[i]]))
    }
  }
}
charter(detailed_listings)

levels(detailed_listings$neighborhood)
knn.pre = preProcess(x = detailed_listings[-which(names(detailed_listings) == "updated_at")], method = "knnImpute")
df_knn = predict(knn.pre, detailed_listings)


#################
##Dummification##
#################

dummies <- dummyVars(rental_income ~., data = detailed_listings)
df_dummies = predict(dummies, newdata = detailed_listings)


##################################
##Modeling & Feature Engineering##
##################################

###Creating feature ammenity_count to represent the number of ammenities in each listing

detailed_listings$ammenity_count = rowSums(detailed_listings[50:220])
detailed_listings %>% 
  ggplot(aes(y = occupancy, 
             x = ammenity_count)) +
  geom_smooth() +
  geom_point(position = "jitter")# + 
# xlim(0,5000)

model.count = lm(occupancy ~ c(ammenity_count),
                 data = detailed_listings)

summary(model.count)

##########################
##80/20 Train-Test Split##
##########################

detailed_listings = na.omit(detailed_listings)
x = model.matrix(rental_income ~ ., detailed_listings)[, -1] 
y = detailed_listings$rental_income
set.seed(0)
train = sample(1:nrow(x), 7*nrow(x)/10)
test = (-train)
y.test = y[test]
grid = 10^seq(5, -2, length = 100)

#####################
##Feature Selection##
#####################

###LASSO Model

#Fitting the lasso regression. Alpha = 1 for lasso regression.
lasso.models = glmnet(x, y, alpha = 1, lambda = grid)

#Visualizing the lasso regression shrinkage.
plot(lasso.models, xvar = "lambda", label = TRUE, main = "Lasso Regression")

#Running 10-fold cross validation.
set.seed(0)
cv.lasso.out = cv.glmnet(x[train], y[train],
                         lambda = grid, alpha = 1, nfolds = 10)
plot(cv.lasso.out, main = "Lasso Regression\n")
bestlambda.lasso = cv.lasso.out$lambda.min
lasso.bestlambdatrain = predict(lasso.models, s = bestlambda.lasso, newx = x[test, ])
mean((lasso.bestlambdatrain - y.test)^2)


###Recursive Feature elimination

ctrl =  rfeControl(functions = lmFuncs,
                 method = "repeatedcv",
                 repeats = 5,
                 verbose = FALSE)
subsets <- c(1:5, 10, 15, 25)

rfe(x = x, y = y,
    sizes = subsets,
    rfeControl = ctrl)






