#!/usr/bin/env Rscript

library( tidyverse )

file.name = "../build/power_truncated"

read.csv( file.name, header=TRUE, sep=';' ) %>%
    as_tibble() ->
    d

options(tibble.print_max = Inf, tibble.print_max = Inf)
print(d, nrow=100)
