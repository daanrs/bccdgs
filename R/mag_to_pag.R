V <- c("X1","X2","X3","X4") # variable labels
amat <- rbind(c(0,0,2,0),
              c(0,0,2,0),
              c(3,3,0,2),
              c(0,0,3,0))
rownames(amat)<-V
colnames(amat)<-V

suffStat<-list(g=amat,verbose=FALSE)

# Derive PAG that represents the Markov equivalence class of the MAG with the FCI algorithm
# Make use of d-separation oracle as "independence test"
indepTest <- dsepAMTest
fci.pag <- fci(suffStat,indepTest,alpha = 0.5,labels = V,verbose=FALSE)

cat('True MAG:\n')
print(amat)
cat('PAG output by FCI:\n')
print(fci.pag@amat)
