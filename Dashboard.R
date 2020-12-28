





  
####Dataset Overview


  



df_comb%>%
  filter(level == 1)%>%
  ggplot(aes(x = price))+
  geom_histogram() +
  xlim(0,250) +
  ggtitle("Distribution of Nightly Prices") +
  xlab("Nightly Price") +
  ylab("Count")



detailed_listings %>%
  ggplot(aes(y = rental_income, x = factor(bedrooms))) +
  geom_boxplot() +
  xlab("# of Bedrooms") +
  ylab("Monthly Income")

#detailed_listings %>%
#  ggplot(aes(y = rental_income, x = beds/bedrooms))+
#  geom_point()+
#  geom_smooth() +
#  xlim(0,8)

#detailed_listings %>%
#  ggplot(aes(x = occupancy, y = person_capacity, fill= rental_income))+
#  geom_tile()

#Ammenity Slides


detailed_listings %>%
  ggplot(aes(x = bedrooms))+
  geom_histogram()




dtb = detailed_listings %>%
  group_by(bedrooms, X24.hour.check.in)%>%
  summarise(income=mean(rental_income))
dtb$bedrooms = as.factor(dtb$bedrooms)
dtb$X24.hour.check.in = as.factor(dtb$X24.hour.check.in)
dtb %>% ggplot(aes(y = income, x = bedrooms, fill = X24.hour.check.in)) + 
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_x_discrete(name ="Bedrooms Per Listings", 
                   limits=c("0", "1", "2", "3", "4","5", "6", "7"))+
  ggtitle("Monthly Income for Properties With or Without Ammenity")

dtn = detailed_listings %>%
  group_by(neighborhood, Outlet.covers )%>%
  summarise(income=mean(rental_income), count= n())%>%
  group_by(neighborhood) %>%
  mutate(tcount = sum(count))
dtn$neighborhood = as.factor(dtn$neighborhood)
dtn$Outlet.covers = as.factor(dtn$Outlet.covers)

fval = 20
dtn %>% filter(tcount>=20)%>%
  ggplot(aes(y = income, x = neighborhood, fill = Outlet.covers )) + 
  geom_bar(stat = "identity", position = position_dodge()) +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
    labs(title = "Average Rental Income By Neighborhood", 
         caption = paste(c("Excludes Neighborhoods with Less than 20 Listings")))

