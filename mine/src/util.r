#!/usr/bin/env Rscript

# Source a single function from a source file.
# Example use
# max.a.posteriori <- source1("res/map.r","map")
source1 <- function( path, fun )
{
  source( path, local=TRUE )
  get( fun )
}
