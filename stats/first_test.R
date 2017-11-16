#!/usr/bin/env Rscript

# Solutions to some excercises from  Grolemund & Wickham (2017) R for Data Science
# at http://r4ds.had.co.nz/


library(nycflights13)
library(tidyverse)


# 3.3.1 Q1
# Now they are blue.
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy), colour = "blue") +
  ggtitle("3.3.1 Q1")

# 3.6.1 Q5
"3.6.1 Q5"
"No, they look the same."
"In the first case, we set a mapping in the parent scope and"
"implicitly use it in both plots."
"In the second example, we set two identical 'local' mappings."

# 3.6.1 Q6
# top left
tl <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy)) + 
        geom_point() + 
        geom_smooth(se=FALSE) +
        ggtitle("3.6.1 Q6")

# top right
tr <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy, group = drv)) +
        geom_point() +
        geom_smooth(se = FALSE)

# mid left
ml <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy, group = drv, colour = drv)) +
        geom_point() +
        geom_smooth(se = FALSE)

# mid right
mr <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy, colour = drv)) +
        geom_point() +
        geom_smooth(se = FALSE, colour = "blue")

# bottom left
bl <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy, group = drv, colour = drv, linetype = drv)) +
        geom_point() +
        geom_smooth(se = FALSE)

# bottom right
br <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy, colour = drv)) +
        geom_point()


# 5.7.1 Q1
"5.7.1 Q1"
"flights_sml %>% group_by(year, month, day) %>% filter(rank(desc(arr_delay)) < 10)"
"Here the grouppling causes R to print the 10 worst example for each day,"
"instead of the 10 worst examples overall."
"The results are fewer than 3650, because not each day has at least 10 flights."
""
"flights %>%group_by(dest) %>%filter(n() > 365)"
"Here the groupping is essential."
"It instructs filter() over which column to apply it's condition."
""

# 5.7.1 Q5
flights %>%
  filter(dep_delay <= 500) %>%
  ggplot(mapping = aes(x = dep_delay, y = lag(dep_delay))) +
    geom_point() +
    geom_smooth() +
    ggtitle("5.7.1 Q5")
"A positive correlation is somewhat visiable after filtering extreme values and fitting."

# 5.7.1 Q6
# Look at each destination. Can you find flights that are suspiciously fast?
# (i.e. flights that represent a potential data entry error).
# Using mean() instead of min() is a standard practice when filtering outliers.
mean_times <- flights %>%
                group_by(origin, dest) %>%
                summarise(mean_time = mean(air_time, na.rm = TRUE))
with_means <- left_join(flights, mean_times)
outliers <- with_means %>% filter(air_time <= (mean_time / 2) | air_time >= (mean_time * 2))
"Potential data entry errors:"
outliers

# Compute the air time a flight relative to the shortest flight to that destination.
shortest <- flights %>%
              group_by(dest) %>%
              summarise(min_time = min(air_time))
with_mins <- left_join(flights, shortest)
mutate(with_mins, rel_time = air_time / min_time)

# Which flights were most delayed in the air?
"Most delayed flights:"
arrange(flights, desc(arr_delay - dep_delay))

# Misc
print("Please refer to the gererated 'Rplot.pdf' for the plots.")

wait_for_key <- function()
{
  print("Type 'next' to see next plot.")
  b <- scan("stdin", character(), n=1)
}

# Copied from The R Cookbook:
# http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)/
# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

multiplot(tl, tr, ml, mr, bl, br, cols = 2)
