library(pcalg)

args = commandArgs()
x = length(args)
lv_location = args[x-2]
dag_location = args[x-1]
pag_location = args[x]
print(pag_location)

# nodes
v = 10
# probability of edge
#prob = 0.25
prob = 0.25
# max hidden
hid = 2

##
L_num <- sample.int(hid, 1)
L <- sample.int(v, hid)

g <- randomDAG(v, prob = prob)
#graph::nodes(g) # "1" "2" ... "10"

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

gm = as(g, "matrix")
write.table(L, lv_location, row.names = FALSE, col.names = FALSE, sep = ",")
write.table(gm, dag_location, row.names = FALSE, col.names = FALSE, sep = ',')
write.table(true.pag@amat, pag_location, row.names = FALSE, col.names = FALSE, sep = ',')
