library(pdp)
server <- function(input, output, session) {
  observe({
    amenities <- unique(amnames) 
    updateSelectizeInput(
      session, "amenity",
      choices = amnames,
      selected = amnames[1])
  })
  
  
  output$s11r <-renderPlot({
    partial(rf.listing500, pred.var = as.character(input$amenity), plot = TRUE, train = X,  plot.engine = "ggplot2")
    #X[X[, "bedrooms"] == 2,]
    })
  output$neighborhood <- renderPlot({
    
  })  
  output$corr <- renderPlot({
    
  })
  
  output$room <- renderPlot({
    dtb = df_comb %>%
      filter(level ==2)%>%
      group_by(bedrooms, get(input$amenity))%>%
      summarise(income=mean(rental_income))
    dtb$bedrooms = as.factor(dtb$bedrooms)
    dtb[,as.character(get(input$amenity))] = as.factor(get(input$amenity))
    dtb %>% ggplot(aes(y = income, x = bedrooms, fill = input$amenity)) + 
      geom_bar(stat = "identity", position = position_dodge()) +
      scale_x_discrete(name ="Bedrooms Per Listings", 
                       limits=c("0", "1", "2", "3", "4","5", "6", "7"))+
      ggtitle("Monthly Income for Properties With or Without Ammenity")
  })

  output$room_dist <-renderPlot({
    #room_dist_am = input$amenity
    #df_comb[room_dist_am ==1,]
    df_comb%>%
      filter(level == 2, get(input$amenity) == 1)%>%
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
      summarise(count = sum(get(input$amenity)), prop = (sum( get(input$amenity))/n())) %>%
      filter(prop != 0)%>%
      ggplot(aes(x = reorder(neighborhood,-prop), y = prop)) +
      geom_bar(stat = "identity")+
      ggtitle("Proportion of Properties w/ Ammenity")+
      xlab("Neighborhood")+ 
      theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
    
  })
  
  output$am_dist_type <-renderPlot({
    detailed_listings%>%
      group_by(property_type)%>%
      summarise(count = sum(get(input$amenity)), prop = (sum( get(input$amenity))/n())) %>%
      filter(prop != 0)%>%
      ggplot(aes(x = reorder(property_type,-prop), y = prop)) +
      geom_bar(stat = "identity")+
      ggtitle("Proportion of Properties w/ Ammenity")+
      xlab("Property Type")+ 
      theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
    
  })
}

#
#importance(rf.listing500) %>%arrange(desc(X.IncMSE))

#p1 <- partial(, pred.var = c("lstat", "rm"), plot = TRUE, chull = TRUE)
#p2 <- partial(boston_rf, pred.var = c("lstat", "rm"), plot = TRUE, chull = TRUE,
#              palette = "magma")
#grid.arrange(p1, p2, nrow = 1)  # Figure 7