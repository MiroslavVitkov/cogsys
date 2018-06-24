#!/usr/bin/env Rscript


library(tidyverse)


source( "read.r" )


d = read.dataset( print.rows=10 )


# Valid times are those between the first and last measuremet.
.date.first = head( d$time, n=1 )
.date.last = tail( d$time, n=1 )
.date.is.valid = function( date )
{
    date >= .date.first & date <= .date.last
}
stopifnot( ! .date.is.valid( Sys.time() ) )
stopifnot( .date.is.valid( .date.last ) )


v = date.is.valid( d$time )
print(v)


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

