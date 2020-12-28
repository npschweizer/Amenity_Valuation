library(corrplot)
library(shiny)

ui <- fluidPage(
    sidebarLayout(
        sidebarPanel(
            checkboxGroupInput("variable", "Variables to show:",
                       detailed_listings %>%
                           select_if(is.numeric) %>%
                           select_if(~ !any(is.na(.)))%>%
                           colnames(),
                       selected = detailed_listings %>%
                           select_if(is.numeric) %>%
                           select_if(~ !any(is.na(.)))%>%
                           colnames()
           ),
           sliderInput("numeric", "Threshold:",
                       min = 0, max = 1,
                       value = .5)
        )

    ,
        mainPanel(
            plotOutput("data")
        )
    )
)

server <- function(input, output, session) {
    output$data <- renderPlot(
            corrplot(detailed_listings%>%
                         select_if(is.numeric) %>%
                         select_if(~ !any(is.na(.)))%>%
                         select(c(input$variable)) %>%
                             cor()>input$numeric, 
                                col = c("white", "red"),
                                #bg = "lightblue",
                                #method = "square",
                                order = "hclust",
                     addrect = 4
                     
                     )
                        
            )
    
    
    
}

shinyApp(ui, server)

#https://bradleyboehmke.github.io/HOML/regularized-regression.html
library(plotmo)
library(vip)
#Fitting the lasso regression. Alpha = 1 for lasso regression.
lasso.models = glmnet(x,y, alpha = 1, lambda = grid)
plot_glmnet(lasso.models, label = 20)
vip(lasso.models, num_features = 40, geom = "point")
set.seed(0)
cv.lasso.out = cv.glmnet(x[train, ], y[train],lambda = grid, alpha = 1, nfolds = 10)
plot(cv.lasso.out, main = "Lasso Regression\n")
bestlambda.lasso = cv.lasso.out$lambda.min
lasso.bestlambdatrain = predict(lasso.models, s = bestlambda.lasso, newx = x[test, ])
mean((lasso.bestlambdatrain - y.test)^2)