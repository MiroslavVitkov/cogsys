#!/usr/bin/env Rscript


require( tidyverse )


read.dataset = function( file.name="../build/power_truncated" )
{
    read.csv( file.name, header=TRUE, sep=';' ) %>% as_tibble() -> d
    d[[1]] <- as.Date( d[[1]] )
#    d[[1]] <- as.POSIXct( d[[1]] )
    return(d)
}


print.dataset = function( d )
{
    options(tibble.print_max = Inf, tibble.print_max = Inf)
    print(d, nrow=100)
    return(d)
}
