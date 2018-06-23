#!/usr/bin/env Rscript


library(tidyverse)


source( "read.r" )


d = read.dataset()


# Valid times are those between the first and last measuremet.
date.first = head( d[1], n=1 )
date.last = tail( d[1], n=1 )
date.is.valid = function( date )
{
    date >= date.first && date <= date.last
}
stopifnot( ! date.is.valid( Sys.time() )
stopifnot( date.is.valid(date.last) )


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

