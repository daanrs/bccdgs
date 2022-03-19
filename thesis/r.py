from rpy2.robjects.packages import importr

base = importr('base')
stats = importr('stats')
bccdgsr = importr('bccdgsr')

def set_r_seed(s):
    base.set_seed(s)
