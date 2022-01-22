library(RUcausal)
library(pcalg)

args = commandArgs()
x = length(args)
location = args[x]
print(location)

# nodes
v = 10
# probability of edge
#prob = 0.25
prob = 0.25
# max hidden
hid = 2
points = 1000

##
L_num <- sample.int(hid, 1)
L <- sample.int(v, hid)

g <- randomDAG(v, prob = prob)
graph::nodes(g) # "1" "2" ... "10"

## compute the true covariance matrix of g
cov.mat <- trueCov(g)
## transform covariance matrix into a correlation matrix
true.corr <- cov2cor(cov.mat)

## Find PAG
n <- 10^9
true.pag <- dag2pag(suffStat = list(C = true.corr, n=n),
                    indepTest = gaussCItest,
                    graph=g, L=L, alpha = 0.9999, verbose=FALSE)

### ---- Find PAG using fci-function --------------------------

## From trueCov(g), delete rows and columns belonging to latent variable L
true.cov1 <- cov.mat[-L,-L]
## transform covariance matrix into a correlation matrix
true.corr1 <- cov2cor(true.cov1)

## generate 10000 samples of DAG using standard normal error distribution
n <- points
d.normMat <- rmvDAG(n, g, errDist="normal")
R <- cor(d.normMat)
R <- R[-L,-L]
#R <- true.corr1

bccd.fit1a <- BCCD(R, n, provide_detailed_output = TRUE, no_selection_bias = TRUE)

#pagm = as(true.pag, "matrix")

write.table(g@amat, paste('data/', location, '_original_pag.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')
write.table(true.pag@amat, paste('data/', location, '_original_dag.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$PAG, paste('data/', location, '_bccd_result.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$prob_L_max, paste('data/', location, '_lst.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$prob_L_use, paste('data/', location, '_lst_use.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')

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
