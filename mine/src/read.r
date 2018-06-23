#!/usr/bin/env Rscript


# Reads a file into a tibble.


library( tidyverse )


read.dataset = function( file.name="../build/power_truncated", print=FALSE )
{
    read.csv( file.name, header=TRUE, sep=';' ) %>% as_tibble() -> d
#    print(as.POSIXct(d[[1]]))
#    d[[1]] = as.Date( d[[1]] )
#    d[[1]] <- as.POSIXct( d[[1]] )
#    d[[2]] <- as.POSIXct( d[[2]], format="%hh:%mm:%ss" )
    

    # if print
    options(tibble.print_max = Inf, tibble.print_max = Inf)
    print(d, nrow=100)

    return(d)
}


# Produce a POSIXct value out of date and time strings.
as.time = function( date, time )
{
    str = paste( date, time )
    t = as.POSIXct( str, format="%d/%m/%Y %H:%M:%S" )
    return(t)
}
stopifnot( as.time( '16/12/2006', '17:50:00' ) == as.POSIXct( "16/12/200617:50:00", format="%d/%m/%Y%H:%M:%S" ) )


# Active energy consumed every minute (in watt hour) in the household
# by electrical equipment not measured in sub-meterings 1, 2 and 3.
compose.sub_metering_rest = function( dataset )
{
# global_active_power*1000/60 - sub_metering_1 - sub_metering_2 - sub_metering_3
    return(kur)
}
