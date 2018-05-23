#!/usr/bin/env Rscript
# seite 52



####################
# External code
# Taken from: https://github.com/rmcelreath/rethinking
# highest posterior density interval, sensu Box and Tiao
# requires coda library
library(coda)
PIprimes <- c(0.67,0.89,0.97) # my snarky prime valued percentiles
HPDI <- function( samples , prob=0.89 ) {
    # require(coda)
    class.samples <- class(samples)[1]
    coerce.list <- c( "numeric" , "matrix" , "data.frame" , "integer" , "array" )
    if ( class.samples %in% coerce.list ) {
        # single chain for single variable
        samples <- coda::as.mcmc( samples )
    }
    x <- sapply( prob , function(p) coda::HPDinterval( samples , prob=p ) )
    # now order inside-out in pairs
    n <- length(prob)
    result <- rep(0,n*2)
    for ( i in 1:n ) {
        low_idx <- n+1-i
        up_idx <- n+i
        # lower
        result[low_idx] <- x[1,i]
        # upper
        result[up_idx] <- x[2,i]
        # add names
        # Miroslav: what is 'concat()'??
        names(result)[low_idx] <- paste("|",prob[i])
        names(result)[up_idx] <- paste(prob[i],"|")
#        names(result)[low_idx] <- concat("|",prob[i])
#        names(result)[up_idx] <- concat(prob[i],"|")
    }
    return(result)
}

####################


'3M1'
p_grid <- seq( from=0, to=1, length.out=1e2 )
generate_posterior <- function( water, total, prior=rep(1,length(p_grid)) )
{
    likelihood <- dbinom( water, size=total, prob=p_grid )
    posterior <- likelihood * prior
    posterior <- posterior / sum( posterior )
    posterior
}
( posterior <- generate_posterior( 8, 15 ) )

'3M2'
draw_samples <- function( posterior, how_many )
{
    # Set seed both for consistency with the book and for reproducible results.
    set.seed( 100 )
    sample( p_grid, prob=posterior, size=how_many, replace=TRUE )
    # Why do we use 'replace=TRUE'?
}
samples <- draw_samples( posterior, 1e4 )
HPDI( samples, 0.9 )

'3M3'
( w <- rbinom( 1e2 , size=15 , prob=samples ) )
length( w[ w==8 ] ) / length( w )

'3M4'
generate_posterior( 6, 9, posterior )

'3M5'
( posterior <- generate_posterior( 8, 15, c(rep(0,length(p_grid)/2),rep(1,length(p_grid)/2)) ) )
samples <- draw_samples( posterior, 1e4 )
HPDI( samples, 0.9 )
( w <- rbinom( 1e2 , size=15 , prob=samples ) )
length( w[ w==8 ] ) / length( w )
generate_posterior( 6, 9, posterior )
