#!/usr/bin/env Rscript
# Excercises - Measures of central tendency


library(nycflights13)
library(tidyverse)

# Q1
# Using the built-in R functions, find the mean, trimmed mean (trimmed by 5% either side), and
# median departure delay for the whole flights dataset. Are they different? Why?
mean(flights$dep_delay, na.rm = TRUE)
mean(flights$dep_delay, na.rm = TRUE, trim = 0.05)
median(flights$dep_delay, na.rm = TRUE)
"As expected, the timmed mean lies between the mean and the media."
"The mean being positive, while the median is negative, "
"indicates that planes are more often early, but when they are late, "
"they are very much late."

# Q2
# Use the n() function to find the number of arriving flights per destination airport and by carrier.
# Hint: use ?n to find out how the n() function works.
flights %>% group_by(dest, carrier) %>% summarise(n()) 

# Q3
# Using one pipe, (i) group the flights dataset by destination airport, (ii) find the number of arriving
# flights per destination airport, the mean, trimmed mean, and median departure delays, and (iii) save
# the output tibble as a variable.
dest_stats <- flights %>% group_by(dest) %>% summarise(n = n(),
                                                       mean = mean(dep_delay, na.rm = TRUE),
                                                       clipped_mean = mean(dep_delay, trim = 0.05, na.rm = TRUE),
                                                       median = median(dep_delay, na.rm = TRUE)) 
dest_stats

# Q4
# Using your saved tibble from Q3, make separate plots for the mean, median, and trimmed mean
# departure delays as a function of the number of arriving flights per destination airport. Are airports
# with more flights more likely to experience delays? For extra brownie points: Try doing all three in one
# ggplot using one pipe! (Hint: you’ll need to change the tibble to long format and use facets for the
# plot).
ggplot(dest_stats, aes(x=n)) +
    geom_smooth(aes(y=mean), colour="red") +
    geom_smooth(aes(y=clipped_mean), colour="blue") +
    geom_smooth(aes(y=median), colour="green")
"Small airports seem to have larger and often occuring delays."

# Q5
# Find the mean distance travelled for the whole flights dataset
# without using the mean() function.
col <- flights$distance
sum(col) / length(col)

# Q6
# Find the median distance travelled for the whole flights dataset
# without using the median() funtion.
# Even length lists not handled!
sort(col)[length(col)/2]

# Q7
# Do the same thing for the trimmed mean without using the mean() function.
cut = round(0.05 * length(col))
trimmed = sort(col)[cut : length(col)-cut]
sum(trimmed) / length(trimmed)
