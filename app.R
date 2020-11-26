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