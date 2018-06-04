#!/usr/bin/env Rscript

library( tidyverse )

file.name = "../extern/power_truncated"

read.csv( file.name, header=TRUE, sep=';' ) %>%
    as_tibble() ->
    d

d
