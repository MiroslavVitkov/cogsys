#!/usr/bin/env Rscript


library( 'corrplot' )
library( 'tidyverse' )


source( 'clean.r' )
source( 'analyse.r' )


d = read.dataset( print.rows=20 )
d = subset( d, is.valid.row( d ) )
numbers = d %>% select( -c(time) )


calc.cor.matrix( numbers, method='pearson') %>%
    corrplot( method='circle', order='hclust', addrect=3 )

calc.cor.matrix( numbers, method='spearman') %>%
    corrplot( method='circle', order='hclust', addrect=3 )

#calc.cor.matrix( numbers, method='kendall') %>%
#    corrplot( method='circle', order='hclust', addrect=3 )

# Pretend that these are corelation scores.
calc.kl.matrix( numbers ) %>%
    print %>%
    ( function( mat )  1 / mat ) %>%
    log %>%
    ( function( mat )  mat - min(mat) ) %>%
    ( function( mat )  mat / max(abs(mat)) ) %>%
    print %>%
    corrplot( method='circle', order='hclust' )




