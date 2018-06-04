#!/usr/bin/env Rscript

source1 <- function( path, fun )
{
  source( path, local=TRUE )
  get( fun )
}

# Example use
# max.a.posteriori <- source1("res/map.r","map")
