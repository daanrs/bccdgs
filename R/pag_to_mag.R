library(pcalg)

args = commandArgs()
n = length(args)
pag_location = args[n-1]
mag_location = args[n]

#V <- c("X1","X2","X3","X4") # variable labels
amat <- read.table(pag_location, sep=',')
amat <- as.matrix(amat)

amat <- pag2magAM(amat, 1)
write.table(amat, mag_location, row.names = FALSE, col.names = FALSE, sep = ',')
