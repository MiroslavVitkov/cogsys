#!/usr/bin/env Rscript


# Estimate various scores for similarity between random variables.


library( tidyverse )


calc.cor.matrix = function( dataset, method=c('pearson', 'kendall', 'spearman') )
{
    score = cor( dataset[1:ncol(dataset)], method=method )
    return( score )
}


calc.kl.matrix = function( dataset, smooth=.smooth )
{
    features = ncol( dataset )
    kl = matrix( 0, nrow=features, ncol=features )
    for( i in 1:features )
    {
        for( j in 1:features )
        {
            d1 = pull( d, i ) %>% .pdf.discrete
            d2 = pull( d, j ) %>% .pdf.discrete %>% smooth

            score = .KL.discrete( d1, d2 )

            kl[i, j] = score
        }
    }

    colnames(kl) = colnames(d)
    rownames(kl) = colnames(d)

    return( kl )
}



'%=%' = function( a, b )
{
    e = 1e-10
    eq = a - b < e
    return( eq )
}


# The discrete equivelent of the probability density function.
.pdf.discrete = function( vec, buckets=length( base::unique( vec ) ) )
{
    h = hist( x=vec, breaks=buckets, plot=FALSE )
    dist = h$counts / sum( h$counts )

    if( sum( dist ) != 1 )
    {
        dist = dist / sum(dist)
    }
    stopifnot( sum( dist ) == 1 )

   return( dist )
}
stopifnot( .pdf.discrete( c(2, 2, 2, 2, 5) ) == c(0.8, 0.2) )
stopifnot( .pdf.discrete( -7 ) == c( 1 ) )


# k - totatal probability mass to evenly distribute, values: (0 - inf)
.smooth = function( vec, k=0.1 )
{
    stopifnot( k >= 0 )

    s = vec + k / length(vec)
    s = s / sum(s)
    return( s )
}
stopifnot( .smooth( c(1, 2), k=1 ) == c(0.375, 0.625) )
stopifnot( .smooth( c(2.95, 6.95) ) == c(0.3, 0.7) )


.pad = function( seq, target_len )
{
    if( length(seq) < target_len )
    {
        seq = c( seq, rep( 0, target_len - length(seq) ) )
    }

    return ( c( seq ) )
}
stopifnot( .pad( c(0, 1, 2, 3), 7 ) == c(0, 1, 2, 3, 0, 0, 0) )


# Kullback–Leibler divergence
.KL.discrete = function( p, q ) 
{
    # The K-L divergence is only defined if P and Q both sum to 1
    stopifnot( sum( p ) %=% 1 )
    stopifnot( sum( q ) %=% 1 )

    # and if Q(i) > 0 for any i such that P(i) > 0.
    p = .pad( p, length(q) ) %>% .smooth
    q = .pad( q, length(p) ) %>% .smooth
    stopifnot( all( p >= 0 ) )
    stopifnot( all( q > 0 ) )

    kl = p * log( p / q )

    return( sum( kl ))
}
stopifnot( .KL.discrete( c(0.1, 0.3, 0.45, 0.15), c(0.1, 0.3, 0.45, 0.15) ) == 0 )
stopifnot( .KL.discrete( c(0.1, 0.3, 0.45, 0.15), c(0.7, 0.1, 0.1, 0.1) ) != 0 )

