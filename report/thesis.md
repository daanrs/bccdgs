---
title: "Thesis"
bibliography: bib/thesis.bib
author: "Daan Spijkers"
---

# Thesis Draft
~~~ python
def bccdgs(pag):
  mag = pag_to_mag(pag)
  next_mag = next_mag(mag)

  while score(next_mag) > score(mag):
    mag = next_mag
    next_mag = best_scoring_mag(adjacent_mags(mag))
  return mag_to_pag(mag)
~~~

Here we see that there are 4 main problems that we need to solve:

  1. Transforming a PAG into a MAG.
  2. Generating adjacent mags.
  3. Scoring a MAG.
  4. Transforming a MAG into a PAG

#### Scoring a MAG
Scoring is not necessarily the most difficult part, but it is more
unique to our problem, and did not have a readily available
implementation. We have implemented 3 checks:

  1. Ancestor(x, y)
  2. Edge(x, y)
  3. Cofounder(x, y)
