library(RUcausal)
library(pcalg)

# NOT RUN {
## create the graph
set.seed(78)
g <- randomDAG(10, prob = 0.25)
graph::nodes(g) # "1" "2" ... "10" % FIXME: should be kept in result!

## define nodes 2 and 6 to be latent variables
L <- c(2,6)

## generate 1000 samples of DAG using standard normal error distribution
#n <- 10000000
#d.normMat <- rmvDAG(n, g, errDist="normal")
#R <- cor(d.normMat)
#R <- R[-L,-L]

## compute the true covariance matrix of g
cov.mat <- trueCov(g)
## transform covariance matrix into a correlation matrix
true.corr <- cov2cor(cov.mat)

## Find PAG
## as dependence "oracle", we use the true correlation matrix in
## gaussCItest() with a large "virtual sample size" and a large alpha:
n <- 10^9
true.pag <- dag2pag(suffStat = list(C = true.corr, n=n),
                    indepTest = gaussCItest,
                    graph=g, L=L, alpha = 0.9999, verbose=FALSE)

### ---- Find PAG using fci-function --------------------------

## From trueCov(g), delete rows and columns belonging to latent variable L
true.cov1 <- cov.mat[-L,-L]
## transform covariance matrix into a correlation matrix
true.corr1 <- cov2cor(true.cov1)

R <- true.corr1

bccd.fit1a <- BCCD(R, n, provide_detailed_output = TRUE, no_selection_bias = TRUE)

pagm = as(true.pag, "matrix")

write.table(pagm, 'data/in/original_pag.csv', row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$PAG, 'data/in/bccd_result.csv', row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$prob_L_max, 'data/in/lst.csv', row.names = FALSE, col.names = FALSE, sep = ',')

#print(bccd.fit1a$PAG)

#plot_PAG(bccd.fit1a$PAG)
#plot(g)

### compute the true covariance matrix of g
#cov.mat <- trueCov(g)
### transform covariance matrix into a correlation matrix
#true.corr <- cov2cor(cov.mat)

### Find PAG
### as dependence "oracle", we use the true correlation matrix in
### gaussCItest() with a large "virtual sample size" and a large alpha:
#system.time(
#true.pag <- dag2pag(suffStat = list(C = true.corr, n = 10^9),
                    #indepTest = gaussCItest,
                    #graph=g, L=L, alpha = 0.9999) )

#### ---- Find PAG using fci-function --------------------------

### From trueCov(g), delete rows and columns belonging to latent variable L
#true.cov1 <- cov.mat[-L,-L]
### transform covariance matrix into a correlation matrix
#true.corr1 <- cov2cor(true.cov1)
