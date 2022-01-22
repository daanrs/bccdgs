library(RUcausal)
library(pcalg)

args = commandArgs()
x = length(args)

n = as.integer(args[x-4])
lv_location = args[x-3]
dag_location = args[x-2]
pag_output = args[x-1]
lst_output = args[x]
print(n)

L <- read.table(lv_location, sep = ',')$V1
amat <- read.table(dag_location, sep =',')
g <- as.matrix(amat)
g <- getGraph(g)

## generate samples of DAG using standard normal error distribution
d <- rmvDAG(n, g, errDist="normal")
R <- cor(d)
R <- R[-L,-L]

bccd.fit1a <- BCCD(R, n, provide_detailed_output = TRUE, no_selection_bias = TRUE)

write.table(bccd.fit1a$PAG, pag_output, row.names = FALSE, col.names = FALSE, sep = ',')
write.table(bccd.fit1a$prob_L_max, lst_output, row.names = FALSE, col.names = FALSE, sep = ',')
