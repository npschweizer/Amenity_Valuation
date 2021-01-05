ui <- fluidPage(
  
  ###Application Title
  titlePanel(title = "Amenity-Shmemenity"),
  
  sidebarLayout(
    sidebarPanel("by Nathan Schweizer",
    
    
      selectizeInput(inputId = "amenity",
                     label = "Amenity",
                     choices = unique(amnames)),
      #menuItem("Market Overview", 
      #         tabName = "Market Overview", 
      #         icon = icon("Market Overview")),
      
     # menuItem("data", 
      #         tabName = "data", 
      #         icon = icon("data"))
    ),
    
    mainPanel(
      tabsetPanel (
        tabPanel("Market Overview",
                 fluidRow(
                   plotOutput("room_dist"),
                   plotOutput("am_dist"),
                   plotOutput("am_dist_type")
                 )
        ),
        tabPanel("Amenities",
                 fluidRow(
                   plotOutput("neighborhood")),
                 fluidRow(
                   plotOutput("room"))
                 ),
        tabPanel("data",
                fluidRow(
                  plotOutput("corr"),
                  checkboxGroupInput("variable", 
                                     "Variables to show:",
                                     choices = df_comb %>%
                                       filter(level == 2)%>%
                                       select_if(is.numeric) %>%
                                       select_if(~ !any(is.na(.)))%>%
                                       colnames(),
                                     selected = df_comb %>%
                                       filter(level == 2) %>%
                                       select_if(is.numeric) %>%
                                       select_if(~ !any(is.na(.)))%>%
                                       colnames()),
                  sliderInput("numeric", 
                              "Threshold:",
                              min = 0, 
                              max = 1,
                              value = .5)
                ))
      ))
    
  )
)

