#!/usr/bin/env Rscript


library(tidyverse)


# Using the Titanic disaster stats from https://vincentarelbundock.github.io/Rdatasets/datasets.html
dat = read.csv("res/Titanic.csv", header = TRUE)


# Q1: In one ggplot, make histograms of passengers’ ages, split into facets for gender and for those
# who survived and those who didn’t. Who was more or less likely to survive?
use table$survived = as.factor(table$survived)
ggplot(data = dat, aes = ) + geom_hystogram() + facet_grid() or facet_wrap()
