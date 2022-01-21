library(pcalg)

location = commandArgs()[6]
print(location)

#V <- c("X1","X2","X3","X4") # variable labels
amat <- read.table(paste('data/', location, '_mag.csv', sep=""), sep=',')
amat <- as.matrix(amat)
#rownames(amat)<-V
#colnames(amat)<-V

suffStat<-list(g=amat,verbose=FALSE)

# Derive PAG that represents the Markov equivalence class of the MAG with the FCI algorithm
# Make use of d-separation oracle as "independence test"
indepTest <- dsepAMTest
fci.pag <- fci(suffStat,indepTest,alpha = 0.5, p=nrow(amat), verbose=FALSE)

write.table(fci.pag@amat, paste('data/', location, '_pag.csv', sep=""), row.names = FALSE, col.names = FALSE, sep = ',')

#cat('True MAG:\n')
#print(amat)
#cat('PAG output by FCI:\n')
#print(fci.pag@amat)
