#!/usr/bin/env Rscript


# Reads the dataset file into a tibble.
# Casts everything to consistent physical units.


library( tidyverse )


# Produce a POSIXct value out of date and time strings.
as.time = function( date, time )
{
    str = paste( date, time )
    t = as.POSIXct( str, format="%d/%m/%Y %H:%M:%S" )
    return(t)
}
stopifnot( as.time( '16/12/2006', '17:50:00' ) == as.POSIXct( "16/12/200617:50:00", format="%d/%m/%Y%H:%M:%S" ) )


# An attempt to convert 'watt-hour of active energy'
# to 'minute-averaged active power'.
Wh.to.W = function( Wh )
{
    return( Wh / 3600 )
}
stopifnot( Wh.to.W( 3.14 ) == 3.14 / 3600 )


read.dataset = function( file.name="../build/power_truncated", print=FALSE )
{
    d = read.csv( file.name, header=TRUE, sep=';' )

    time = as.time( d$Date, d$Time )
    active.W = d$Global_active_power * 1000
    reactive.VA = d$Global_reactive_power
    voltage.V = d$Voltage
    current.A = d$Global_intensity
    active1.W = Wh.to.W( d$Sub_metering_1 )
    active2.W = Wh.to.W( d$Sub_metering_2 )
    active3.W = Wh.to.W( d$Sub_metering_3 )
    active4.W = active.W - active1.W - active2.W - active3.W

    ret = tibble( time, active.W, reactive.VA, voltage.V, current.A
                , active1.W, active2.W, active3.W, active4.W )

    if( print )
    {
        options( tibble.print_max = Inf )
        print( ret, nrow=100 )
    }

    return( ret )
}
read.dataset()
