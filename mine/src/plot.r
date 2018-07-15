#!/usr/bin/env Rscript


library( 'corrplot' )


source( 'clean.r' )
source( 'analyse.r' )


d = read.dataset( print.rows=20 )
d = subset( d, is.valid.row( d ) )
numbers = d %>% select( -c(time) )


cor.mat = calc.cor.matrix( numbers, method='pearson')
kl.mat = calc.kl.matrix( numbers )

corrplot( cor.mat, method='circle', order='hclust', addrect=3 )

