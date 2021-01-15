import sys
import os

sys.path.append("../")
import netrecon.Directed_graph_Class as sample
import netrecon.Undirected_graph_Class as sample_und
import netrecon.Matrix_Generator as mg
import numpy as np
import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_ECM_Dianati_random_dense_20_undir(self):

        network = mg.random_weighted_matrix_generator_dense(
            n=20, sup_ext=10, sym=True, seed=10, intweights=True
        )

        g = sample_und.UndirectedGraph(adjacency=network)

        g.solve_tool(
            model="ecm",
            method="fixed-point",
            max_steps=20000,
            verbose=False,
            initial_guess="random",
        )

        g.solution_error()

        # test result
        # print(g.error)

        self.assertTrue(g.error < 1)


if __name__ == "__main__":

    unittest.main()
