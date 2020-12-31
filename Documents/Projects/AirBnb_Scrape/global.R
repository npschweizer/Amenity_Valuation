###Run Me First
setwd("C:/Users/nates/Documents/Projects/AirBnb_Scrape")
detailed_listings_pre = read.csv("l0_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE)
detailed_listings = read.csv("l1_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE)
detailed_listings_post = read.csv("l2_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE)
df_amenities = read.csv("amenities.csv", stringsAsFactors = TRUE, header = TRUE)
library(dplyr)
library(ggplot2)
library(corrplot)
library(caret)
library(lubridate)
library(ISLR)
library(glmnet)
library(shiny)
library(shinydashboard)
detailed_listings$level = 1
detailed_listings_post$level = 2
df_comb = rbind(detailed_listings, detailed_listings_post)
#amnames = colnames(amenities_df)
if( "updated_at" %in% colnames(df_comb)){
  df_comb$created_at = ymd_hms(df_comb$created_at)}
if( "created_at" %in% colnames(detailed_listings_post)){
  df_comb$updated_at = ymd_hms(df_comb$created_at)  
  df_comb = df_comb %>%
    filter(created_at < "2020-09-06 07:03:27 UTC")
}
if( "user_id" %in% colnames(df_comb)){
  df_comb$user_id = factor(df_comb$user_id)
  df_comb$user_id = NULL}
if( "zipcode" %in% colnames(df_comb)){
  df_comb$zipcode = factor(df_comb$zipcode)}
if( "neighborhood" %in% colnames(df_comb)){
  df_comb$neighborhood = factor(df_comb$neighborhood)}

# #######################
# ##Feature Engineering##
# #######################
# 
df_comb$fh_weekend_price = df_comb$listing_weekend_price_native + df_comb$price_for_extra_person_native * (df_comb$person_capacity - df_comb$guests_included)

###Creating feature ammenity_count to represent the number of ammenities in each listing
 amnames = c()
 for(ams in 1:length(df_amenities)){
   if(colnames(df_amenities[ams]) %in% colnames(df_comb) ){
   amnames =append(amnames, colnames(df_amenities[ams]))}
 }
 df_comb$amenity_count = rowSums(df_comb[amnames])
###Creating feature rooms to represent the number of bedrooms and bathrooms in each listing
 
df_comb$rooms = df_comb$bedrooms + df_comb$bathrooms

###Creating feature avg price to represent the expected price
###of a randomly selected night
 
df_comb$avg_price = (df_comb$price * 5 + df_comb$listing_weekend_price_native * 2)/7

###Creating accesibility score
df_access = df_amenities[c(2,3, 42, 54, 61, 62, 75, 107, 134, 161, 162, 163, 164, 165, 166, 167)]

df_access$AccessibilityScore = rowSums(df_access)

df_access%>%
  ggplot(aes(x = as.factor(AccessibilityScore))) +
  geom_histogram(stat = "count")
colSums(df_access)

###Bathroom Score

df_essential = df_amenities[c(13,17,19,51,154,170)]
colSums((df_essential))
###creating Child-Friendly Score
df_child = df_amenities[c(7,8,9,32,33,39,55,80,112,114,152,31,58,122,15)]
df_child$ChildScore = rowSums(df_child)
df_child%>%
  ggplot(aes(x = as.factor(ChildScore))) +
  geom_histogram(stat = "count")
colSums(df_child)

###creating Common Amenities df
df_common = df_amenities[c(138, 139, 36, 53, 73, 76, 87, 128, 129, 96, 4, 79, 125, 29,
                           95,83,52,123,93,94,151,25,131,147,85
                           )]
colSums(df_common)

###creating Kitchen Amenities df
df_kitchen = df_amenities[c(101,38, 35, 105, 126, 89, 132, 102, 66, 44, 156, 43, 149, 113, 20,
                            133, 10, 12)]

colSums(df_kitchen)

###creating Facilities Amenities df

df_facilities = df_amenities[c(64, 65, 115, 116, 47, 71, 124, 82, 140)]

###creating Outdoor df
df_outdoor=df_amenities[c(6,117,69)]

###creating Special Amenities df
df_logistics = df_amenities[c(34,98,99)]
summary(df_logistics)

###creating 
 ###Limited Linear Model
# df_lm = filter(df_comb, level ==2)
# df_lm$AccessibilityScore = df_access$AccessibilityScore
# df_lm$ChildScre = df_child$ChildScore
#  model.limited = lm(rental_income ~ rooms +
#                      fh_weekend_price+
#                      occupancy +
#                      guests_included+
#                      AccessibilityScore+
#                      cleaning_fee_native,
#                    data = df_lm[train,]
#                      )
                
#some outliers 1471,1478, 1476, 178

# summary(model.limited)
# plot(model.limited)
# 
 ###Engineering Location Variable
# library(class)
# library(caret)
# df_loc = data.frame(filter(df_comb, level == 2)$neighborhood)
# df_loc$city = filter(df_comb, level == 2)$city
# df_loc$zipcode = as.factor( filter(df_comb, level == 2)$zipcode)
# df_loc$lat = filter(df_comb, level == 2)$lat
# df_loc$lng = filter(df_comb, level == 2)$lng
# df_loc$rooms = filter(df_comb, level == 2)$rooms
# colnames(df_loc) = c("neighborhood", "city", "zipcode", "rooms")
#  
# 
# dummies <- dummyVars(rooms~., data = df_loc)
# df_loc = predict(dummies, newdata = df_loc)
# 
# set.seed(0)
# cl = factor(as.integer(runif(nrow(df_loc), 1,10)))
# knn.loc = knn3Train(train = df_loc[train,], df_loc[test,], cl = cl[train], k = 500, prob = TRUE)
# df_loc$probs = attributes(knn.loc)[[3]]
# max = max(df_loc$probs)
# nrow(subset(df_loc,probs != max))

#####################
##Feature Selection##
#####################
 df_imp = df_comb %>%
    select(rental_income, everything()) %>% filter(level ==2)%>%
    filter(neighborhood == "Center City" )
 df_imp = df_imp[complete.cases(df_imp),]
 x <- model.matrix(rental_income ~.,
                   data = df_imp)[,-1]
 
 y = df_imp$rental_income
 set.seed(0)
 train = sample(1:nrow(x), 7*nrow(x)/10)
 test = (-train)
 y.test = y[test]
 grid = 10^seq(5, -2, length = 100)
 
#https://bradleyboehmke.github.io/HOML/regularized-regression.html
library(plotmo)
library(vip)
#Fitting the lasso regression. Alpha = 1 for lasso regression.
lasso.models = glmnet(x,y, alpha = 1, lambda = grid)
plot_glmnet(lasso.models, label = 10)
vip(lasso.models, num_features = 30, geom = "point")
set.seed(0)
cv.lasso.out = cv.glmnet(x[train, ], y[train],lambda = grid, alpha = 1, nfolds = 10)
plot(cv.lasso.out, main = "Lasso Regression\n")
bestlambda.lasso = cv.lasso.out$lambda.min
lasso.bestlambdatrain = predict(lasso.models, s = bestlambda.lasso, newx = x[test, ])
mean((lasso.bestlambdatrain - y.test)^2)
summary(lasso.models)
#  #Visualizing the lasso regression shrinkage.
#  plot(lasso.models , xvar = "lambda", label = TRUE, main = "Lasso Regression")
# 
#  plot(cv.lasso.out, label = 20)
#  vip(cv.lasso.out, num_features = 15, geom = "point")
#  #Running 10-fold cross validation.
 


# ###Recursive Feature elimination
# 
# ctrl =  rfeControl(functions = lmFuncs,
#                  method = "repeatedcv",
#                  repeats = 5,
#                  verbose = FALSE)
# subsets <- c(1:5, 10, 15, 25)
# 
# rfe(x = x, y = y,
#     sizes = 5,
#     rfeControl = ctrl)
# options(error=recover)
# 
# ###Random Forest
# library(randomForest)
# 
# #Fitting an initial random forest to the training subset.
# set.seed(0)
# rf.listing = randomForest( x, y, importance = TRUE)
# rf.listing
# 
# #Can visualize a variable importance plot.
# importance(rf.listing)
# varImpPlot(rf.listing)
# df_tree_imp = data.frame(importance(rf.listing))
# df_tree_imp = df_tree_imp %>%arrange(desc(X.IncMSE))


   