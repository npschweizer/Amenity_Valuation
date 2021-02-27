###Run Me First
setwd("~/Projects/Ammenity_Valuation")
#detailed_listings_pre = read.csv("l0_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE, fileEncoding = 'UTF-8-BOM')
detailed_listings = read.csv("l1_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE, fileEncoding = 'UTF-8-BOM')
detailed_listings_post = read.csv("l2_detailed_listings.csv", stringsAsFactors = TRUE, header = TRUE, fileEncoding = 'UTF-8-BOM')
#df_amenities = read.csv("amenities.csv", stringsAsFactors = TRUE, header = TRUE,fileEncoding = 'UTF-8-BOM')
df_amenities_pre = read.csv("l0_amenities.csv", stringsAsFactors = TRUE, header = TRUE, fileEncoding = 'UTF-8-BOM')
df_amenities = read.csv("l1_amenities.csv", stringsAsFactors = TRUE, header = TRUE, fileEncoding = 'UTF-8-BOM')
df_train = read.csv("train.csv", stringsAsFactors = TRUE, header = FALSE, fileEncoding = 'UTF-8-BOM')
#train = df_train$V1
1
train = seq(1, nrow(detailed_listings_post) * .8,1)
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
#df_comb= detailed_listings_post
#amnames = colnames(amenities_df)
if( "updated_at" %in% colnames(df_comb)){
  df_comb$created_at = ymd_hms(df_comb$created_at)}
if( "created_at" %in% colnames(detailed_listings_post)){
  df_comb$updated_at = ymd_hms(df_comb$created_at)  
  df_comb = df_comb %>%
    filter(created_at < "2020-09-06 07:03:27 UTC")
}
if( "user_id" %in% colnames(df_comb)){
  df_comb$user_id = factor(df_comb$user_id)}
if( "zipcode" %in% colnames(df_comb)){
  df_comb$zipcode = factor(df_comb$zipcode)}
if( "neighborhood" %in% colnames(df_comb)){
  df_comb$neighborhood = factor(df_comb$neighborhood)}

#####################0
##Split and Dummify##
#####################
library(proxy)
library(caret)
df_imp = df_comb %>%
  select(rental_income, everything()) %>% filter(level ==2)#%>%
df_imp$level = NULL
df_imp$zipcode = NULL
df_imp$bed_type_category = NULL

X <- model.matrix(rental_income ~.,
                  data = df_imp)[,-1]

y = df_imp$rental_income
mat_dum = cbind(X,y)
maxs <- apply(mat_dum, 2, max)  
mins <- apply(mat_dum, 2, min)
mat_dum_sca = scale(mat_dum,  
                    center = mins, 
                    scale = maxs - mins)
set.seed(0)
train = sample(1:nrow(df_imp), 7*nrow(df_imp)/10)
test = (-train)
y.test = y[test]
X.train = X[train,]
X.test = X[test,]

df_imp_ri = df_imp
df_imp_ri$rental_income = NULL
X_ri <- model.matrix(occupancy ~.,
                     data = df_imp_ri)[,-1]
y_ri = df_imp_ri$occupancy
test = (-train)
y.test_ri = y_ri[test]
X.train_ri = X_ri[train,]
X.test_ri = X_ri[test,]



#######################
##Feature Engineering##
#######################


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

###creating 
###Linear Model
# library(car)
# model.crazy = lm(rental_income ~ .,
#                    data = df_imp[train,])
# plot(model.crazy)
# summary(model.crazy)
# 
# 
# model.crazy.log = lm(log(rental_income) ~ .,
#                  data = df_imp[train,])
# plot(model.crazy.log)
# summary(model.crazy.log)
# 
# bc = boxCox(model.crazy)
# lambda = bc$x[which(bc$y == max(bc$y))]
# 
# rental_income.bc = (df_imp$rental_income^lambda - 1)/lambda
# df_imp_bc = df_imp
# df_imp_bc$rental_income = rental_income.bc
# model.crazy.bc = lm(rental_income ~ .,
#                  data = df_imp_bc[train,])
# 
# 
# summary(model.crazy.bc)
# plot(model.crazy.bc)
# 

# ###Recursive Feature elimination
# library(caret)
#   ctrl =  rfeControl(functions = lmFuncs,
#                    method = "repeatedcv",
#                    repeats = 5,
#                    verbose = FALSE)
#   subsets <- c(1:5, 10, 15, 25)
# 
#   rfe(rental_income ~ .,
#       data = df_imp_bc[train,],
#       sizes = 5,
#       rfeControl = ctrl)
#   options(error=recover)
# 


###Creating accesibility score
df_access = df_amenities[c("Accessible.height.bed" ,"Accessible.height.toilet",
                           "Elevator", "Extra.space.around.bed", "Fixed.grab.bars.for.shower",
                           "Flat.path.to.guest.entrance", "Handheld.shower.head",
                           "No.stairs.or.steps.to.enter", "Roll.in.shower", 
                           "Wheelchair.accessible", "Well.lit.path.to.entrance", "Wide.entrance",
                           "Wide.doorway.to.guest.bathroom", "Wide.clearance.to.shower", 
                           "Wide.entrance.for.guests" ,"Wide.entryway", "Wide.hallways")]

df_access$AccessibilityScore = rowSums(df_access)

df_access%>%
  ggplot(aes(x = as.factor(AccessibilityScore))) +
  geom_histogram(stat = "count")
colSums(df_access)

###Bathroom Score

df_essential = df_amenities[c(13,17,19,51,154,170)]
colSums((df_essential))

###creating Child-Friendly Score
df_child = df_amenities[c("Baby.bath","Baby.monitor","Babysitter.recommendations",
                          "Changing.table","Children.s.books.and.toys","Children.s.dinnerware",
                          "Crib","Family.kid.friendly" ,"High.chair","Outlet.covers",
                          "Pack..n.Play.travel.crib","Playground",
                          "Table.corner.guards","Fireplace.guards","Playground","Bathtub")]
df_child$ChildScore = rowSums(df_child)
df_child%>%
  ggplot(aes(x = as.factor(ChildScore))) +
  geom_histogram(stat = "count")
colSums(df_child)

###creating Common Amenities df
df_common = df_amenities[c("Shampoo", "Shower.gel", "Conditioner", "Extra.pillows.and.blankets", "Hair.dryer" , 
                           "Hangers", "Iron", "Private.entrance", "Private.living.room", "Lock.on.bedroom.door", 
                           "Air.conditioning", "Heating", "Portable.fans", "Ceiling.fan","Laundromat.nearby","Hot.water",
                           "Ethernet.connection","Pocket.wifi","Laptop.friendly.workspace" ,
                           "TV","Cable.TV","Record.player","Sound.system","Indoor.fireplace" 
                           )]
colSums(df_common)

###creating Kitchen Amenities df
df_kitchen = df_amenities[c("Microwave","Cooking.basics", "Coffee.maker", "Nespresso.machine" , "Pour.Over.Coffee", "Keurig.coffee.machine", 
                            "Refrigerator", "Mini.fridge", "Freezer", "Dishwasher", "Trash.compacter", "Dishes.and.silverware",
                            "Stove", "Oven", "Bread.maker", "Refrigerator", "Baking.sheet" , "Barbecue.utensils", "Rice.Maker",
                            "Baking.sheet", "Convection.oven", "Espresso.machine", "Full.kitchen", "Kitchen","Kitchenette", "Nespresso.machine",
                            "Pour.Over.Coffee")]

colSums(df_kitchen)

###creating Facilities Amenities df

df_facilities = df_amenities[c("Free.parking.on.premises", "Free.street.parking", "Paid.parking.off.premises", 
                               "Paid.parking.on.premises", "EV.charger" , "Gym", "Pool", "Hot.tub", "Single.level.home" )]

###creating Outdoor df
df_outdoor=df_amenities[c("BBQ.grill", "Patio.or.balcony", "Garden.or.backyard")]
###creating Special Amenities df
df_logistics = df_amenities[c(34,98,99)]
df_logistics%>%cor()

 
                
#some outliers 1471,1478, 1476, 178

# summary(model.limited)
# plot(model.limited)
# 
 ###Engineering Location Variable
 library(class)

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



    
   # 
   
# #  #DisSamp = maxDissim(a = X.test, b = X.train, n = nrow(X)/10)
# # 
# #  
# ##########
# ##Models##
# ##########

#Running ElasticNet 10-fold cross validation.
# rsq <- function(x, y) summary(lm(y~x))$r.squared
# grid = 10^seq(5, -2, length = 100)
# agrid = seq(from = 0,
#             to = 1,
#             by = .1)
#  set.seed(0)
lasso.models = glmnet(X[train, ],y[train], alpha = 1, lambda = grid)
cv.lasso.out = cv.glmnet(X[train, ], y[train],type.measure = "mae",
                        lambda = grid, alpha = 1, nfolds = 10)
plot(cv.lasso.out, main = "Lasso Regression\n")
bestlambda.lasso = cv.lasso.out$lambda.min

lasso.best.yhat = predict(lasso.models, s = bestlambda.lasso, newx = X[test, ])
lasso.best.train.yhat = predict(lasso.models, s = bestlambda.lasso, newx = X[train, ])
lasso.r2.train = sum((y[train] - lasso.best.train.yhat)^2)/sum((y[train]-mean(y[train]))^2)
lasso.r2.test = sum((y[test] - lasso.best.yhat)^2)/ sum((y.test-mean(y.test))^2)
plot(y.test,lasso.best.yhat)
abline(0,1)
  # 
  # lasso.mae.train = mean(abs(lasso.best.train.yhat-y[train]))
  # lasso.mae.test = mean(abs(lasso.best.yhat-y.test))
  # 
  # set.seed(0)
  # ridge.models = glmnet(X[train, ],y[train], alpha = 0, lambda = grid)
  # cv.ridge.out = cv.glmnet(X[train, ], y[train],type.measure = "mae",
  #                          lambda = grid, alpha = 0, nfolds = 10)
  # plot(cv.ridge.out, main = "Ridge Regression\n")
  # bestlambda.ridge = cv.ridge.out$lambda.min
  # ridge.best.yhat = predict(ridge.models, s = bestlambda.ridge, newx = X[test, ])
  # ridge.best.train.yhat = predict(ridge.models, s = bestlambda.ridge, newx = X[train, ])
  # ridge.r2.train = sum((y[train] - ridge.best.train.yhat)^2)/sum((y[train]-mean(y[train]))^2)
  # ridge.r2.test = sum((y[test] - ridge.best.yhat)^2)/ sum((y.test-mean(y.test))^2)
  # plot(y.test,ridge.best.yhat)
  # abline(0,1)
  # 
  # ridge.mae.train = mean(abs(ridge.best.train.yhat-y[train]))
  # ridge.mae.test = mean(abs(ridge.best.yhat-y.test))


# #  ###Random Forest
    library(randomForest)
    library(vip)
# #
    #Fitting an initial random forest to the training subset.
    set.seed(0)
    rf.listing500 = randomForest( X[train,] , y[train], importance = TRUE, ntree = 100                           )
    rf.yhat500 = predict(rf.listing500, newdata = X[test, ])
    rf.train.yhat500 = predict(rf.listing500, newdata = X[train, ])
    plot(y.test,rf.yhat500)
    abline(0,1)

    rf.r2.500.train = sum((y[train] - rf.train.yhat500)^2)/sum((y[train]-mean(y[train]))^2)
    rf.r2.500.test = sum((y[test] - rf.yhat500)^2)/ sum((y.test-mean(y.test))^2)

    rf.mae500.train = mean(abs(rf.train.yhat500-y[train]))
    rf.mae500.test = mean(abs(rf.yhat500-y.test))
    vip(rf.listings500, num_features = 30, geom = "point")
# 
# rf.listing1000 = randomForest( X[train,] , y[train], importance = TRUE, ntree = 1000                           )
# rf.yhat1000 = predict(rf.listing1000, newdata = X[test, ])
# rf.train.yhat1000 = predict(rf.listing1000, newdata = X[train, ])
# plot(y.test,rf.yhat1000)
# abline(0,1)
# 
# rf.r2.1000.train = sum((y[train] - rf.train.yhat1000)^2)/sum((y[train]-mean(y[train]))^2)
# rf.r2.1000.test = sum((y[test] - rf.yhat1000)^2)/ sum((y.test-mean(y.test))^2)
# 
# rf.mae1000.train = mean(abs(rf.train.yhat1000-y[train]))
# rf.mae1000.test = mean(abs(rf.yhat1000-y.test))
# 
# rf.listing2500 = randomForest( X[train,] , y[train], importance = TRUE, ntree = 2500                           )
# rf.yhat2500 = predict(rf.listing2500, newdata = X[test, ])
# rf.train.yhat2500 = predict(rf.listing2500, newdata = X[train, ])
# plot(y.test,rf.yhat2500)
# abline(0,1)
# 
# rf.r2.2500.train = sum((y[train] - rf.train.yhat2500)^2)/sum((y[train]-mean(y[train]))^2)
# rf.r2.2500.test = sum((y[test] - rf.yhat2500)^2)/ sum((y.test-mean(y.test))^2)
# 
# rf.mae2500.train = mean(abs(rf.train.yhat2500-y[train]))
# rf.mae2500.test = mean(abs(rf.yhat2500-y.test))
# 
#   rf.listing5000 = randomForest( X[train,] , y[train], importance = TRUE, ntree = 5000                           )
#   rf.yhat5000 = predict(rf.listing5000, newdata = X[test, ])
#   rf.train.yhat5000 = predict(rf.listing5000, newdata = X[train, ])
#   plot(y.test,rf.yhat5000)
#   abline(0,1)
# 
#   rf.r2.5000.train = sum((y[train] - rf.train.yhat5000)^2)/sum((y[train]-mean(y[train]))^2)
#   rf.r2.5000.test = sum((y[test] - rf.yhat5000)^2)/ sum((y.test-mean(y.test))^2)
# 
#   rf.mae5000.train = mean(abs(rf.train.yhat5000-y[train]))
#   rf.mae5000.test = mean(abs(rf.yhat5000-y.test))
# 
#   rf.listing10000 = randomForest( X[train,] , y[train], importance = TRUE, ntree = 10000                           )
#   rf.yhat10000 = predict(rf.listing10000, newdata = X[test, ])
#   rf.train.yhat10000 = predict(rf.listing10000, newdata = X[train, ])
#   plot(y.test,rf.yhat10000)
#   abline(0,1)
# 
#   rf.r2.10000.train = sum((y[train] - rf.train.yhat10000)^2)/sum((y[train]-mean(y[train]))^2)
#   rf.r2.10000.test = sum((y[test] - rf.yhat10000)^2)/ sum((y.test-mean(y.test))^2)
# 
#   rf.mae10000.train = mean(abs(rf.train.yhat10000-y[train]))
#   rf.mae10000.test = mean(abs(rf.yhat10000-y.test))
# 
# 
# 
#   set.seed(0)
#   oob.err.test = seq(80, 200, 10)
#   oob.err.train = oob.err.test
#   i = 1
# 
#   for (i in 1:length(oob.err)) {
#     fit = randomForest(X[train,], y[train], mtry = oob.err[i])
#     oob.err.test[i] = mean(abs(predict(fit, newdata = X[test, ])-y.test))
#     oob.err.train[i] = mean(abs(predict(fit, newdata = X[train, ])-y[train]))
#     cat("We're performing iteration", i, "\n")
#   }
# 
#   #Visualizing the OOB error.
#   par(mfrow =c(1,2))
#   plot(seq(80, 200, 10), oob.err.test, pch = 16, type = "b",
#        xlab = "Variables Considered at Each Split",
#        ylab = "OOB Mean Absolute Error",
#        main = "Test Random Forest OOB Error Rates\nby # of Variables")
#   plot(seq(80, 200, 10), oob.err.train, pch = 16, type = "b",
#        xlab = "Variables Considered at Each Split",
#        ylab = "OOB Mean Absolute Error",
#        main = "Train Random Forest OOB Error Rates\nby # of Variables")
#   
# # # ###Gradient Boosted Regression
#  library(gbm)
# 
#  set.seed(0)
#  boost.listing = gbm(rental_income~.,data = df_imp[train,],
#                     distribution = "gaussian",
#                     n.trees = 10000,
#                     interaction.depth = 4,
#                     shrinkage = .1)
#  n.trees = seq(from = 100, to = 10000, by = 100)
#  
#  tpredmat = predict(boost.listing, newdata = df_imp[train, ], n.trees = n.trees)
#  predmat = predict(boost.listing, newdata = df_imp[-train, ], n.trees = n.trees)
#    #Inspecting the relative influence.
#   
    # par(mfrow = c(1, 2))
    # berr = with(df_imp[-train, ], apply(abs((predmat - rental_income)), 2, mean))
    # plot(n.trees, berr, pch = 16,
    #      ylab = "Mean Absolute Error",
    #      xlab = "# Trees",
    #      main = "Boosting Test Error")
    # 
    # #par(mfrow = c(1, 1))
    # tberr = with(df_imp[train, ], apply(abs((tpredmat - rental_income)), 2, mean))
    # plot(n.trees, tberr, pch = 16,
    #      ylab = "Mean Absolute Error",
    #      xlab = "# Trees",
    #      main = "Boosting Train Error")
#    
#    
# #  ###Support Vector Machine
#    library(e1071)
# # 
# #   #Fitting a maximal margin classifier to the training data.
# #   svm.mmc.linear = svm(rental_income~., #Familiar model fitting notation.
# #                        data = df_imp, #Using the linearly separable data.
# #                        subset = train, #Using the training data.
# #                        kernel = "linear", #Using a linear kernel.
# #                        cost = 1e6,#A very large cost; default is 1.
# #                        type = "eps",
# #                        scale = FALSE)
# #   yhat.svm.mmc.linear = predict(svm.mmc.linear, newdata = df_imp[test, ])
# #   summary(svm.mmc.linear)
# #   mean(abs(yhat.svm.mmc.linear - df_imp$rental_income[test]))
# # 
#    svm.mmc.radial = svm(rental_income~., #Familiar model fitting notation.
#                         data = df_imp, #Using the linearly separable data.
#                         subset = train, #Using the training data.
#                         kernel = "radial", #Using a linear kernel.
#                         cost = 1e6,#A very large cost; default is 1.
#                         type = "eps",
#                         scale = FALSE)
#    yhat.svm.mmc.radial = predict(svm.mmc.radial, newdata = df_imp[test, ])
#    summary(svm.mmc.radial)
#    mean(abs(yhat.svm.mmc.radial - df_imp$rental_income[test]))
# 
#   cv.svm = tune(svm,
#                             rental_income ~ .,
#                             data = df_imp[train, ],
#                             kernel = "radial",
#                             ranges = list(cost = 10^(seq(-5, .5, length = 100))))
# 
#   best.model = cv.svm$best.model
#   yhat.svm.best = predict(best.model, newdata = df_imp[test, ])
#   mean(abs(yhat.svm.best - df_imp$rental_income[test]))
# 
#   
#   
#    library(neuralnet)
#    # Build Neural Network 
#    n <- colnames(mat_dum_sca) 
#    colnames(mat_dum_sca) = gsub(" ", ".", n)
#    n <- colnames(mat_dum_sca)
#    colnames(mat_dum_sca) = gsub("'", "", n)
#    n <- colnames(mat_dum_sca) 
#    f <- as.formula(paste("y ~",  
#                          paste(n[!n %in% "y"], 
#                                collapse = " + "))) 
#   h=2
#   for(h in 2:7){
#       nn <- neuralnet(f, 
#                    data = mat_dum_sca[train,], hidden = c(h^2, h), 
#                    linear.output = TRUE) 
#    
#    # Predict on test data 
#    yhat.nn <- predict(nn, mat_dum_sca[test, ]) * attr(mat_dum_sca, 'scaled:scale')[ncol(mat_dum_sca)] + attr(mat_dum_sca, 'scaled:center')[ncol(mat_dum_sca)]
#    mean(abs(yhat.nn - mat_dum[test,ncol(mat_dum)]))}
#    # Plot the neural network 
#    plot(nn)
#    
      ###Model Stack
#     library(h2o)
#     h2o.init(max_mem_size = "5g")
#     n.h2o <- colnames(mat_dum)
#     colnames(mat_dum) = gsub(" ", ".", n.h2o)
#     n <- colnames(mat_dum)
#     colnames(mat_dum) = gsub("'", "", n.h2o)
#     mat_dum_h2o = as.h2o(mat_dum)
#     y_names = "y"
#     X_names = setdiff(names(mat_dum_h2o), y)
#     list_split <- h2o.splitFrame(data = mat_dum_h2o, ratios = 0.8, seed = 0)
#     h2o.train <- list_split[[1]]
#     h2o.valid <- list_split[[2]]
# #
# #   # Train & cross-validate a lasso model
#    best_lasso <- h2o.glm(
#      x = X_names, y = y_names, training_frame = h2o.train, alpha = 1,
#      remove_collinear_columns = TRUE, nfolds = 10, lambda = 21.37017,
#      stopping_metric = "MAE", fold_assignment = "Modulo",
#      keep_cross_validation_predictions = TRUE, seed = 0, standardize = TRUE
#    )
#    results.lasso.train = h2o.performance(best_lasso, newdata = h2o.train)
#    results.lasso.valid = h2o.performance(best_lasso, newdata = h2o.valid)
# 
#    best_ridge <- h2o.glm(
#      x = X_names, y = y_names, training_frame = h2o.train, alpha = 0,
#      remove_collinear_columns = TRUE, nfolds = 10, lambda = 756,
#      stopping_metric = "MAE", fold_assignment = "Modulo",
#      keep_cross_validation_predictions = TRUE, seed = 0, standardize = TRUE
#    )
#    results.ridge.train = h2o.performance(best_ridge, newdata = h2o.train)
#    results.ridge.valid = h2o.performance(best_ridge, newdata = h2o.valid)
# 
#    # Train & cross-validate a RF model
#    best_rf <- h2o.randomForest(
#      x = X_names, y = y_names, training_frame = h2o.train,
#      validation_frame = h2o.valid, ntrees = 500,
#      max_depth = 0, min_rows = 1, nfolds = 10,
#      fold_assignment = "Modulo", keep_cross_validation_predictions = TRUE,
#      seed = 0, stopping_rounds = 50, stopping_metric = "MAE",
#      stopping_tolerance = 0
#    )
#    results.rf.train = h2o.performance(best_rf, newdata = h2o.train)
#    results.rf.valid = h2o.performance(best_rf, newdata = h2o.valid)
# 
#    # Train & cross-validate a GBM model
#    best_gbm <- h2o.gbm(
#      x = X_names, y = y_names, training_frame = h2o.train, ntrees = 200, learn_rate = 0.01,
#      max_depth = 0, min_rows = 1, nfolds = 10,
#      fold_assignment = "Modulo", keep_cross_validation_predictions = TRUE,
#      seed = 0, stopping_rounds = 50, stopping_metric = "MAE",
#      stopping_tolerance = 0
#    )
#    results.gbm.train = h2o.performance(best_gbm, newdata = h2o.train)
#    results.gbm.valid = h2o.performance(best_gbm, newdata = h2o.valid)
# #
#   #
#   #   # Train & cross-validate an XGBoost model
#   #   best_xgb <- h2o.xgboost(
#   #     x = X, y = Y, training_frame = train_h2o, ntrees = 5000, learn_rate = 0.05,
#   #     max_depth = 3, min_rows = 3, sample_rate = 0.8, categorical_encoding = "Enum",
#   #     nfolds = 10, fold_assignment = "Modulo",
#   #     keep_cross_validation_predictions = TRUE, seed = 0, stopping_rounds = 50,
#   #     stopping_metric = "RMSE", stopping_tolerance = 0
#   #   )
#   #
# ensemble_tree_drf <- h2o.stackedEnsemble(
#   x = X_names, y = y_names, training_frame = h2o.train, model_id = "my_tree_ensemble",
#   base_models = list(best_lasso, best_ridge, best_gbm, best_rf),
#   metalearner_algorithm = "drf"
# )
# results.train_drf = h2o.performance(ensemble_tree_drf, newdata = h2o.train)
# results.valid_drf = h2o.performance(ensemble_tree_drf, newdata = h2o.valid)
# 
# ensemble_tree_beyes <- h2o.stackedEnsemble(
#   x = X_names, y = y_names, training_frame = h2o.train, model_id = "my_tree_ensemble",
#   base_models = list(best_lasso, best_ridge, best_gbm, best_rf),
#   metalearner_algorithm = "naivebayes"
# )
# results.train_beyes = h2o.performance(ensemble_tree_beyes, newdata = h2o.train)
# results.valid_beyes = h2o.performance(ensemble_tree_beyes, newdata = h2o.valid)
# 
# ensemble_tree_auto <- h2o.stackedEnsemble(
#   x = X_names, y = y_names, training_frame = h2o.train, model_id = "my_tree_ensemble",
#   base_models = list(best_lasso, best_ridge, best_gbm, best_rf),
#   metalearner_algorithm = "auto"
# )
# results.train_auto = h2o.performance(ensemble_tree_auto, newdata = h2o.train)
# results.valid_auto = h2o.performance(ensemble_tree_auto, newdata = h2o.valid)
# 
# 
# ensemble_tree_gbm <- h2o.stackedEnsemble(
#   x = X_names, y = y_names, training_frame = h2o.train, model_id = "my_tree_ensemble",
#   base_models = list(best_lasso, best_ridge, best_gbm, best_rf),
#   metalearner_algorithm = "gbm"
# )
# results.train_auto = h2o.performance(ensemble_tree_gbm, newdata = h2o.train)
# results.valid_auto = h2o.performance(ensemble_tree_gbm, newdata = h2o.valid)
# #   h2o.partialPlot(object = ensemble_tree, data = mat_dum_h2o, cols = c("bedrooms",
#                                                                        "y") )
#   
#   #https://bradleyboehmke.github.io/HOML/regularized-regression.html
#   library(plotmo)
#   library(vip)
#   #Fitting the lasso regression. Alpha = 1 for lasso regression.
#   lasso.models = glmnet(X,y, alpha = 1, lambda = grid)
#   plot_glmnet(lasso.models, label = 10)
#   vip(lasso.models, num_features = 30, geom = "point")
#   #Visualizing the lasso regression shrinkage.
#   plot(lasso.models , xvar = "lambda", label = TRUE, main = "Lasso Regression")
#   
#   plot(cv.lasso.out, label = 20)
#   vip(cv.lasso.out, num_features = 15, geom = "point")
#   
#   
#   #Can visualize a variable importance plot.
#      importance(rf.listing500)
#      varImpPlot(rf.listing500)
#   df_tree_imp = data.frame(importance(rf.listing))
#   df_tree_imp = df_tree_imp %>%arrange(desc(X.IncMSE))
#   
#   par(mfrow = c(1, 1))
#   summary(boost.listing)
#   