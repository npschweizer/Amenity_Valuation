server <- function(input, output, session) {
  observe({
    amenities <- unique(amnames) 
    updateSelectizeInput(
      session, "amenity",
      choices = amnames,
      selected = amnames[1])
  })
  
  output$neighborhood <- renderPlot({
    
  })  
  output$corr <- renderPlot({
    
  })
  
  output$room <- renderPlot({
    
  })

  output$room_dist <-renderPlot({
    #room_dist_am = input$amenity
    #df_comb[room_dist_am ==1,]
    df_comb%>%
      filter(level == 2, input$amenity == 1)%>%
      ggplot(aes(x = bedrooms)) +
      geom_histogram() +
      ggtitle("Number of Listings with Ammenity") +
      scale_x_discrete(name ="Bedrooms", 
                       limits=c("0", "1", "2", "3", "4",
                                "5", "6", "7", "8", "9"))

  })
  
  output$am_dist <-renderPlot({
    detailed_listings%>%
      group_by(neighborhood)%>%
      summarise(count = sum(input$amenity), prop = (sum(input$amenity)/n())) %>%
      filter(prop != 0)%>%
      ggplot(aes(x = reorder(neighborhood,-prop), y = prop)) +
      geom_bar(stat = "identity")+
      ggtitle("Proportion of Properties w/ Ammenity")+
      xlab("Neighborhood")+ 
      theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
    
  })
}