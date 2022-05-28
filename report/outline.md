# Thesis Outline

## Abstract

## Introduction
* what is a dag
* issues arising from real world data
* advantages and disadvantages of different methods
* goal of bccd
* how bccd uses its problem statements

## Preliminaries
* DAG representation of causal relations
* d-seperation
* ancestral graphs

## The algorithm
* algorithm overview
* pag to mag
* mag to pag
* generating adjacent graphs
* generating transitive closure
* details of bccd statements
* scoring a graph

## Results
* what causal score is
* number of nodes
* graph density
* skeleton, k
* min_prob
* runtime

## Related Work
* constraint-based methods, score methods
* other hybrid methods
* metaheuristics

## Conclusions
* bccdmp is better, and bccdgs only a lil better than that
* it's not obvious how we can improve this

further work:
* using all statements
* using metaheuristics such as tabu search, genetic algorithms, etc.
* get multiple mag inputs
* use topological sort, and other ways to find adjacent mags
