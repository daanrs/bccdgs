library(pcalg)
library(RUcausal)

#set.seed(5)

## gen graph

gen_graph <- function(v, hid, prob) {
  L_num <- sample.int(hid, 1)
  L <- sample.int(v, L_num)

  g <- randomDAG(v, prob = prob)

  # compute the true covariance matrix of g
  cov.mat <- trueCov(g)
  # transform covariance matrix into a correlation matrix
  true.corr <- cov2cor(cov.mat)

  # Find PAG
  n <- 10^9
  true.pag <- dag2pag(suffStat = list(C = true.corr, n=n),
                      indepTest = gaussCItest,
                      graph=g, L=L, alpha = 0.9999, verbose=FALSE)

  return list(g, true.pag)
}

run_bccd <- function(g, n) {
  # generate samples of DAG using standard normal error distribution
  d <- rmvDAG(n, g, errDist="normal")
  R <- cor(d)
  R <- R[-L,-L]

  bccd.fit <- BCCD(R, n, provide_detailed_output = TRUE,
                   no_selection_bias = TRUE)

  bpag <- bccd.fit$PAG

  # transform to pcalg style
  bpag <- t(bpag)

  circles <- bpag == 1
  tails <- bpag == 3

  bpag[circles] <- 3
  bpag[tails] <- 1

  return bpag
}

pag_to_mag <- function(pag) {
  mag <- pag2magAM(pag, 1)
  return mag
}

mag_to_pag <- function(mag) {
  ## mag to pag
  suffStat<-list(g=bmag,verbose=FALSE)

  # use d-separation as independence test with FCI
  fci.pag <- fci(suffStat, indepTest=dsepAMTest, alpha = 0.5, p=nrow(amat),
                 verbose=FALSE, selectionBias=FALSE)
  return fci.pag
}
