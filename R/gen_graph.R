library(pcalg)

args = commandArgs()
x = length(args)
hid = as.integer(args[x-5])
prob = as.double(args[x-4])
v = as.integer(args[x-3])
lv_location = args[x-2]
dag_location = args[x-1]
pag_location = args[x]

L_num <- sample.int(hid, 1)
L <- sample.int(v, L_num)

g <- randomDAG(v, prob = prob)

## compute the true covariance matrix of g
cov.mat <- trueCov(g)
## transform covariance matrix into a correlation matrix
true.corr <- cov2cor(cov.mat)

## Find PAG
n <- 10^9
true.pag <- dag2pag(suffStat = list(C = true.corr, n=n),
                    indepTest = gaussCItest,
                    graph=g, L=L, alpha = 0.9999, verbose=FALSE)

gm = as(g, "matrix")
write.table(L, lv_location, row.names = FALSE, col.names = FALSE, sep = ",")
write.table(gm, dag_location, row.names = FALSE, col.names = FALSE, sep = ',')
write.table(true.pag@amat, pag_location, row.names = FALSE, col.names = FALSE, sep = ',')
