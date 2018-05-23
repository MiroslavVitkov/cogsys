#!/usr/bin/env Rscript

'I am sorry for the late submission of the homework.'
'The reasons are a mixture of lazyness and bad internet connection (I am stealing it from the cafee across the street).'
'Also sorry for not submiting the previous one at all - I am a little late to the party this semester.'

'2E1'
'P(data | parameters)'
'(3) Pr(Monday|rain)'

'2E2'
'(1) The probability of rain on Monday.'

'2E3'
'(2) Pr(rain|Monday)'

'2E4'
'Given our measurements we believe there is about 70% water on Earth.'

'2M1'
plot_grid_approx <- function(water, total, prior=rep(1, 20))
{
    p_grid <- seq( from=0 , to=1 , length.out=20 )
    likelihood <- dbinom( water , size=total , prob=p_grid )
    unstd.posterior <- likelihood * prior
    posterior <- unstd.posterior / sum(unstd.posterior)

    plot( p_grid , posterior , type="b" ,
    xlab="probability of water" , ylab="posterior probability" )
    mtext( "20 points" )
}

plot_grid_approx(3, 3)
plot_grid_approx(3, 4)
plot_grid_approx(5, 7)

'2M2'
local
({
    prior = c( rep(0, 10), rep(2, 10) )
    plot_grid_approx(3, 3, prior)
    plot_grid_approx(3, 4, prior)
    plot_grid_approx(5, 7, prior)
})

'2M3'
local
({
    # Uniform prior multiplies each likelyhood by a constant.
    # Thus can be entirely skipped.
    p <- c(0.3, 1.0)
    posterior <- p / sum(p)
    posterior
})

'2M4'
'Possible outcomes: B/B, B/B, B/W, W/B, W/W, W/W.'
'Observed data: B/?.'
'P(B/B) = (B/B + B/B) / (B/B + B/B + B/W) = 2/3'

'2M5'
'Possible outcomes: B/B, B/B, B/B, B/B, B/W, W/B, W/W, W/W.'
'P(B/B) = (4 B/B) / (4 B/B + B/W) = 4/5'

'2M6'
'Possible outcomes: B/B, B/B, B/W, B/W, W/B, W/B, W/W, W/W, W/W, W/W, W/W, W/W'
'P(B/B) = 2/4' 

'2M7'
'Possible outcomes: B/B, B/B, B/W, W/W'
'P(B/B) = (B/B + B/B + B/W) / (B/B + B/B + B/W + W/W) = 3/4'


# Data for chapter 3
p_grid <- seq( from=0 , to=1 , length.out=1000 )
prior <- rep( 1 , 1000 )
likelihood <- dbinom( 6 , size=9 , prob=p_grid )
posterior <- likelihood * prior
posterior <- posterior / sum(posterior)
set.seed(100)
samples <- sample( p_grid , prob=posterior , size=1e4 , replace=TRUE )

'3E1'
sum(samples[p_grid < 0.2]) / sum(samples)

'3E2'
sum(samples[p_grid > 0.8]) / sum(samples)

'3E3'
sum(samples[p_grid > 0.2 & p_grid < 0.8]) / sum(samples)

'3E4'
quantile(samples, 0.2)

'3E5'
1 - quantile(samples, 0.8)

'3E6'
# Get HPDI code from GitHub as described in the book.
'HPDI(samples , prob=0.66)'

'3E7'
'Probbly the median, mean and HPDI coicide, if I have understood the question correctly, namely a symetric distribution.'
