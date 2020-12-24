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



# 
# ###Exploring Rooms, Capacity, and Income
# detailed_listings %>%
#   group_by(neighborhood)%>%
#   summarise(Mean_Revenue = mean(rental_income))%>%
#   arrange(Mean_Revenue)
# 
# detailed_listings%>%
#   ggplot(aes(y = rental_income, x = person_capacity)) +
#   geom_point(position = "jitter") +
#   geom_smooth()
# 
# detailed_listings%>%
#   ggplot(aes(x = price))+
#   geom_histogram() +
#   xlim(0,250)
# 
# detailed_listings %>%
#   ggplot(aes(y = rental_income, x = bedrooms)) +
#   geom_point(position = "jitter") +
#   geom_smooth() +
#   xlim(0,5)
# 
# detailed_listings%>%
#   ggplot(aes(x = weekly_price_factor))+
#   geom_histogram()
# 
# df_comb %>%
#   filter(level ==2)%>%
#   ggplot(aes(x = reorder(zipcode), rental_income))+
#   geom_boxplot()
# 
# df_comb %>%
#   filter(level == 2)%>%
#   ggplot(aes(x = fh_weekend_price, 
#              y = rental_income,
#              color = monthly_price_factor))+
#   geom_point()+
#   ylim(0,10000)+
#   xlim(0,1000)
 
# #######################
# ##Feature Engineering##
# #######################
# 
df_comb$fh_weekend_price = df_comb$listing_weekend_price_native + df_comb$price_for_extra_person_native * (df_comb$person_capacity - df_comb$guests_included)
# 
# detailed_listings%>%
#   ggplot(aes(x = fh_weekend_price, y = rental_income)) +
#   geom_point() + geom_smooth()
# 
# detailed_listings%>%
#   ggplot(aes(x = fh_weekend_price))+
#   geom_histogram()
# model.fh = lm(rental_income ~ fh_weekend_price
#                    ,
#                    data = detailed_listings
# )
# summary(model.fh)
# boxCox(model.fh)
# 
# ###Creating feature ammenity_count to represent the number of ammenities in each listing
 amnames = c()
 for(ams in 1:length(df_amenities)){
   if(colnames(df_amenities[ams]) %in% colnames(df_comb) ){
   amnames =append(amnames, colnames(df_amenities[ams]))}
 }
 df_comb$amenity_count = rowSums(df_comb[amnames])
# ###Creating feature rooms to represent the number of bedrooms and bathrooms in each listing
# 
 df_comb$rooms = df_comb$bedrooms + df_comb$bathrooms
# 
# ###Creating feature avg price to represent the expected price
# ###of a randomly selected night
# 
 df_comb$avg_price = df_comb$price * 5 + df_comb$listing_weekend_price_native
# 
# 
# 
# 
# # + 
# # xlim(0,5000)
# 
# detailed_listings %>%
#   ggplot(aes(x= ammenity_count)) +
#   geom_histogram()
# 
# detailed_listings$rental_income
# model.count = lm(rental_income ~ ammenity_count,
#                  data = detailed_listings)
# plot(model.count)
# summary(model.count)
# 
# ###Limited Linear Model
# df_lm = filter(df_comb, level ==2)
# df_lm = df_lm[-c(1471,1478, 1476, 178)]
# model.limited = lm(rental_income ~ rooms +
#                      fh_weekend_price+
#                      occupancy +
#                      guests_included+ 
#                      #ammenity_count + 
#                      #weekly_price_factor+
#                      #Outlet.covers + 
#                      cleaning_fee_native +
#                      neighborhood
#                      ,
#                    data = df_lm[train,]
#                      )
# summary(model.limited)
# plot(model.limited)
# 
# ###Engineering Location Variable
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
# knn3Train(train = df_loc[train,], df_loc[test,], cl = cl[train], k = 500, prob = TRUE)
# df_loc$probs = attributes(knn.loc)[[3]]
# max = max(df_loc$probs)
# nrow(subset(df_loc,probs != max))
# 
# 

# #####################
# ##Feature Selection##
# #####################

# summary(lasso.models)
# #Visualizing the lasso regression shrinkage.
# plot(lasso.models , xvar = "lambda", label = TRUE, main = "Lasso Regression")

# plot(cv.lasso.out, label = 20)
# vip(cv.lasso.out, num_features = 15, geom = "point")
# #Running 10-fold cross validation.
# set.seed(0)
# cv.lasso.out = cv.glmnet(x[train, ], y[train],lambda = grid, alpha = 1, nfolds = 10)
# plot(cv.lasso.out, main = "Lasso Regression\n")
# bestlambda.lasso = cv.lasso.out$lambda.min
# lasso.bestlambdatrain = predict(lasso.models, s = bestlambda.lasso, newx = x[test, ])
# mean((lasso.bestlambdatrain - y.test)^2)
# 
# 
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
