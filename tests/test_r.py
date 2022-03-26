from bccdgs.r import *

import pytest
import numpy as np

@pytest.fixture
def collider_graph():
    return np.array([
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 0]
    ])

@pytest.fixture
def collider_pag():
    return np.array([
        [0, 0, 3],
        [0, 0, 3],
        [2, 2, 0]
    ])

@pytest.fixture
def hidden_nodes_empty():
    return np.array([], dtype=int)

def test_run_bccd(collider_graph, collider_pag):
    outp = run_bccd(collider_graph, np.array([]), 10**6)[0]

    np.testing.assert_equal(outp, collider_pag)

def test_dag_to_pag(collider_graph, collider_pag, hidden_nodes_empty):
    outp = dag_to_pag(collider_graph, hidden_nodes_empty)

    np.testing.assert_equal(outp, collider_pag)
