library(RUcausal)
library(pcalg)

args = commandArgs()
x = length(args)

n = as.integer(args[x-5])
lv_location = args[x-4]
dag_location = args[x-3]
cor_output = args[x-2]
pag_output = args[x-1]
lst_output = args[x]

L <- read.table(lv_location, sep = ',')$V1
amat <- read.table(dag_location, sep =',')
g <- as.matrix(amat)
g <- getGraph(g)

## generate samples of DAG using standard normal error distribution
d <- rmvDAG(n, g, errDist="normal")
R <- cor(d)
R <- R[-L,-L]

bccd.fit <- BCCD(R, n, provide_detailed_output = TRUE, no_selection_bias = TRUE)

bpag <- bccd.fit$PAG

# transform to pcalg style
bpag <- t(bpag)

circles <- bpag == 1
tails <- bpag == 3

bpag[circles] <- 3
bpag[tails] <- 1

write.table(R, cor_output, row.names=FALSE, col.names=FALSE, sep=',')
write.table(bpag, pag_output, row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit$prob_L_max, lst_output, row.names = FALSE, col.names = FALSE, sep = ',')
