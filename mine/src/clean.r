#!/usr/bin/env Rscript

library( tidyverse )

source( "read.r" )

read.dataset() %>% print.dataset()
