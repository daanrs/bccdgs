library(pcalg)

args = commandArgs()
x = length(args)

n = as.integer(args[x-2])
cor_location = args[x-1]
fci_output = args[x]

R <- read.table(cor_location, sep = ',')
R <- as.matrix(R)

suffstat <- list(C = R, n = n)
fci.pag <- fci(suffstat, gaussCItest, alpha = 0.05, p = nrow(R),
verbose=FALSE, selectionBias=FALSE)

write.table(fci.pag@amat, fci_output, row.names = FALSE, col.names = FALSE, sep = ',')
