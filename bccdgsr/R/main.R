set_seed <- function(s) {
  set.seed(s)
}

graph_to_matrix <- function(g) {
  return(as(g, "matrix"))
}

gen_graph <- function(v, prob) {
  g <- pcalg::randomDAG(v, prob = prob)
  return(graph_to_matrix(g))
}

get_cor <- function(g, L, n) {
  # generate samples of DAG using standard normal error distribution
  g <- pcalg::getGraph(g)
  d <- pcalg::rmvDAG(n, g, errDist="normal")

  R <- cor(d)
  if (length(L) > 0) {
    R <- R[-L,-L]
  }
  return(R)
}

dag_to_pag <- function(g, L) {
  g <- as(g, "graphNEL")

  # Find PAG
  n <- 10^9

  # compute the true covariance matrix of g
  cov.mat <- pcalg::trueCov(g)
  # transform covariance matrix into a correlation matrix
  true.corr <- cov2cor(cov.mat)

  indepTest = pcalg::gaussCItest
  true.pag <- pcalg::dag2pag(suffStat = list(C = true.corr, n=n),
                      indepTest = indepTest,
                      graph=g, L=L, alpha = 0.9999, verbose=FALSE)
  return(graph_to_matrix(true.pag))
}

run_bccd <- function(R, n) {
  bccd.fit <- RUcausal::BCCD(R, n, no_selection_bias=TRUE, provide_detailed_output = TRUE)

  bpag <- bccd.fit$PAG

  # transform to pcalg style
  #bpag <- t(bpag)
  #circles <- bpag == 1
  #tails <- bpag == 3
  #bpag[circles] <- 3
  #bpag[tails] <- 1

  sts = bccd.fit$prob_L_max
  sts_use = bccd.fit$prob_L_use

  return(list(bpag, sts, sts_use))
}

pag_to_mag <- function(pag) {
  mag <- pcalg::pag2magAM(pag, 1)
  if (purrr::is_empty(mag)) {
    return(c(0))
  }
  else {
    return(mag)
  }
}

mag_to_pag <- function(mag) {
  suffStat<-list(g=mag,verbose=FALSE)

  indepTest <- pcalg::dsepAMTest
  # use d-separation as independence test with FCI
  fci.pag <- pcalg::fci(suffStat, indepTest=indepTest, alpha = 0.5, p=nrow(mag),
                 verbose=FALSE, selectionBias=FALSE)
  return(graph_to_matrix(fci.pag))
}
