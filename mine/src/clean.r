#!/usr/bin/env Rscript


# Deal with NAs, '?'s and impossible values.


source( "read.r" )
d = read.dataset( print.rows=10 )


# Valid times are those between the first and last measuremet.
# Returns a boolean vector.
# NAs produce FALSE, not a NA.
.date.first = head( d$time, n=1 )
.date.last = tail( d$time, n=1 )
.date.is.valid = function( date )
{
    valid = ! is.na( date )
    bound = ( date >= .date.first & date <= .date.last )
    return( valid & bound )
}
stopifnot( ! .date.is.valid( Sys.time() ) )
stopifnot( .date.is.valid( .date.last ) )


# Valid power is non-negative and not unbound.
# Returns a boolean vector.
.power.is.valid = function( power.W )
{
    valid = ! is.na( power.W )
    too.much.power = 1e12  # 1GW e.g. a nuclear power plant block
    bound = ( power.W >=0 & power.W < too.much.power )
    return( bound & valid )
}
stopifnot( all( .power.is.valid( c( 0, 42, 9000 ) ) ) )
stopifnot( ! all( .power.is.valid( 1e42 ) ) )
stopifnot( ! all( .power.is.valid( c( 1, 2, NA, 4 ) ) ) )


# Power factor is valid in the closed interval [-1, 1].
.pf.is.valid = function( pf )
{
    valid = ! is.na( pf )
    bound = (pf >= -1 & pf >= 1)
    return( valid & bound )
}


is.valid.row = function( dataset=d )
{
    v = .date.is.valid( d$time ) &
        .power.is.valid( d$active.W ) &
        .power.is.valid( d$reactive.VA ) &
        .power.is.valid( d$voltage.V ) &  # Let's be
        .power.is.valid( d$current.A ) &  # super lazy.
        .pf.is.valid( d$pf ) &
        .power.is.valid( d$active1.W ) &
        .power.is.valid( d$active2.W ) &
        .power.is.valid( d$active3.W ) &
        .power.is.valid( d$active4.W )

    return( v )
}
k=is.valid.row()
print(sum(k[k==TRUE])/length(rownames(d)))
