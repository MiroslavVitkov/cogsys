#!/usr/bin/env Rscript


# Draw a lot of pictures. I have 1 hour until my deadline ot submit some stupid shit.


source( "clean.r" )



d = read.dataset( print.rows=10 )
d = subset( d, is.valid.row( d ) )


estimate = function( a, b, method )
{
    score = cor( d$a, d$b, method=method )
    return( score )
}


main = function()
{
    first_col = colnames(d)
    second_col = colnames(d)
    method = c("pearson", "kendall", "spearman")
}

p = cor( d[2], d[3], method="pearson" )
print(p)

for( i in 1:length(colnames(d)) )
{
    for( j in 1:length(colnames(d)) )
    {
        
    }
}


#p = cor( method="pearson" )

#method = c("pearson", "kendall", "spearman"

