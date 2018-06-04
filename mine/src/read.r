#!/usr/bin/env Rscript


library( tidyverse )


read.dataset = function()
{
    file.name = "../build/power_truncated"
    read.csv( file.name, header=TRUE, sep=';' ) %>% as_tibble()
}


print.dataset = function( d )
{
    options(tibble.print_max = Inf, tibble.print_max = Inf)
    print(d, nrow=100)
}
