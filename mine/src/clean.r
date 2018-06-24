#!/usr/bin/env Rscript


library(tidyverse)


source( "read.r" )


d = read.dataset( print.rows=10 )


# Valid times are those between the first and last measuremet.
# Returns a boolean vector.
.date.first = head( d$time, n=1 )
.date.last = tail( d$time, n=1 )
.date.is.valid = function( date )
{
    return( date >= .date.first & date <= .date.last )
}
stopifnot( ! .date.is.valid( Sys.time() ) )
stopifnot( .date.is.valid( .date.last ) )


# Valid power is non-negative and not unbound.
# Returns a boolean vector.
# NAs produce FALSE, not an NA.
.power.is.valid = function( power )
{
    valid = ! is.na( power )
    too.much.power = 1e12  # 1GW e.g. a nuclear power plant block
    bound = ( power >=0 & power < too.much.power )
    return( bound & valid )
}
stopifnot( all( .power.is.valid( c( 0, 42, 9000 ) ) ) )
stopifnot( ! all( .power.is.valid( 1e42 ) ) )
stopifnot( ! all( .power.is.valid( c( 1, 2, NA, 4 ) ) ) )



# Discriminate negatives, NAs and Inf-s.
is.nonnegative = function( val )
{
    is = FALSE
    if(val >= 0) is = TRUE
    return(is)
}
# assert 0 fails
# assert NA fails
# assert inf fails
# assert 42 succeeds

