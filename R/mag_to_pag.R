library(pcalg)

args = commandArgs()
n = length(args)
mag_location = args[n-1]
pag_location = args[n]
print(pag_location)

#V <- c("X1","X2","X3","X4") # variable labels
amat <- read.table(mag_location, sep=',')
amat <- as.matrix(amat)
#rownames(amat)<-V
#colnames(amat)<-V

suffStat<-list(g=amat,verbose=FALSE)

# Derive PAG that represents the Markov equivalence class of the MAG with the FCI algorithm
# Make use of d-separation oracle as "independence test"
indepTest <- dsepAMTest
fci.pag <- fci(suffStat,indepTest,alpha = 0.5, p=nrow(amat), verbose=FALSE)

write.table(fci.pag@amat, pag_location, row.names = FALSE, col.names = FALSE, sep = ',')
