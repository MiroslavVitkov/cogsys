#!/usr/bin/env Rscript

library( tidyverse )

source( "read.r" )

read.dataset() %>% print.dataset() -> d




date.first = head( d[1], n=1 )
date.last = tail( d[1], n=1 )
date.is.valid = function( date )
{
#    date >= date.first && date <= date.last
    date >= date.first && date <= date.last
}
#date.is.valid( Sys.time() )
Sys.time() < Sys.time()

str(date.first)
print("!!!!!")
str(Sys.time())
