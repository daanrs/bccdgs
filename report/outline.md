# Thesis Outline
WIP outline.

# Abstract

# Introduction

# Research

## The Problem

  * Quick introduction to causal discovery by example. This includes:
    * setup of experiment
    * DAG representation of causal relations
    * Maybe:
      * latent cofounders
      * selection bias
      * d-seperation
  * Advantages and disadvantages of different methods? Not sure how much
    of this to include. It conveys why BCCD is relevant, but is not
    directly related to what I'm trying to do. Maybe this should just be
    in the introduction?
  * Issues arising from real world data
    * Imperfect independence test
    * How BCCD deals with it
    * Comparison between BCCD and ASP

  * Why there might be room for improving the BCCD result graphs
  * Short version of how we plan to do so

## Details

  * How we greedily generate adjacent graphs
  * How we score a graph
  * What optimizations we might make to the process
  * The results

## Results

Questions to answer:

  * check distribution of iterations
  * condition on iterations > 0, see what bccd_accuracy is
  * check difference in skeleton
  * why is bccd_magpag better than bccd
  * check how often the search actually leaves the PAG class, by checking
  bopt == bmagpag (not the score, but the graphs proper)
  * compare difference in graph density
  * compare difference in min_prob for statements
  * compare difference in number of nodes

  * benchmark is super efficient

# Related Work

# Conclusions

## further work:

  * using metaheuristics such as tabu search, genetic algorithms, etc.
  * get multiple mag inputs
  * use topological sort, and other ways to find adjacent mags
