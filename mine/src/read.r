#!/usr/bin/env Rscript


# Reads the dataset file into a tibble.
# Casts everything to consistent physical units.


library( tidyverse )


# Produce a POSIXct value out of date and time strings
# or vectors of strings.
.as.time = function( date, time )
{
    str = paste( date, time )
    t = as.POSIXct( str, format="%d/%m/%Y %H:%M:%S" )
    return(t)
}
stopifnot( .as.time( '16/12/2006', '17:50:00' ) == as.POSIXct( "16/12/200617:50:00", format="%d/%m/%Y%H:%M:%S" ) )


# An attempt to convert 'watt-hour of active energy'
# to 'minute-averaged active power'.
.Wh.to.W = function( Wh )
{
    return( Wh / 3600 )
}
stopifnot( .Wh.to.W( 3.14 ) == 3.14 / 3600 )


# Overall power factor of the house.
.calc.power.factor = function( current.A, voltage.V, active.W )
{
    total.power.VA = current.A * voltage.V
    cos.fi = active.W / total.power.VA
    return( cos.fi )
}
stopifnot( .calc.power.factor( 2, 42, 42 ) == 0.5  )


read.dataset = function( file.name="../build/power_truncated", print.rows=0 )
{
    d = read.csv( file.name, header=TRUE, sep=';', stringsAsFactors=FALSE )

    # Convert '?' -> NA, factor -> double.
    d[ d == '?'] = NA
    factors = c('Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3')
    d[factors] <- lapply( d[factors], function(x) as.numeric( as.character( x ) ) )

    # Output tibble consists of slightly different attributes.
    # Furthermore, all attributes are scaled to SI base units.
    time = .as.time( d$Date, d$Time )
    active.W = d$Global_active_power * 1000
    reactive.VA = d$Global_reactive_power
    voltage.V = d$Voltage
    current.A = d$Global_intensity
    pf = .calc.power.factor( current.A, voltage.V, active.W )
    active1.W = .Wh.to.W( d$Sub_metering_1 )
    active2.W = .Wh.to.W( d$Sub_metering_2 )
    active3.W = .Wh.to.W( d$Sub_metering_3 )
    active4.W = active.W - active1.W - active2.W - active3.W

    ret = tibble( time, active.W, reactive.VA, voltage.V, current.A, pf
                , active1.W, active2.W, active3.W, active4.W )

    if( print.rows > 0 )
    {
        options( tibble.print_max=Inf )
        print( head( ret, n=print.rows ) )
    }

    return( ret )
}
read.dataset()
