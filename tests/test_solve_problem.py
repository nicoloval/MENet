import sys
sys.path.append('../')
import Directed_graph_Class as sample
import numpy as np
import unittest  # test tool


class MyTest(unittest.TestCase):


    def setUp(self):
        pass


    def test_dcm_0(self):
        """test with 3 classes of cardinality 1
        and no zero degrees
        """
        A = np.array([[0, 1, 1],
                      [1, 0, 0],
                      [0, 1, 0],
			])

        g = sample.DirectedGraph(A)


        g._solve_problem(model='dcm', method='quasinewton', max_steps=200, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        """
        print('test 1:')
        print(A)
        print(g.dseq)
        print(g.r_dseq)
        print(g.r_x, g.r_y)
        print(g.x, g.y)
        """
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 0: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)



    def test_qn_dcm_1(self):
        """classes with cardinality > 1, no zero degree
        """
        # test Matrix 1
        n, seed = (4, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        # print(A)

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='quasinewton', max_steps=100, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        """
        print('test 1:')
        print(A)
        print(g.dseq)
        print(g.r_dseq)
        print(g.r_x, g.r_y)
        print(g.x, g.y)
        """
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 1: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-2)


    def test_qn_dcm_2(self):
        """classes with cardinality 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (5, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        A[0,:] = 0
        # print(A)

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='quasinewton', max_steps=100, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        """
        print('test 1:')
        print(A)
        print(g.dseq)
        print(g.r_dseq)
        print(g.r_x, g.r_y)
        print(g.x, g.y)
        """
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 2: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-2)


    def test_qn_dcm_3(self):
        """classes with cardinality more than 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (4, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        A[0,:] = 0

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='quasinewton', max_steps=100, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 3: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-2)

    def test_qn_dcm_4(self):
        """classes with cardinality more than 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (10, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='quasinewton', max_steps=100, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 4: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-2)


    def test_fp_dcm_5(self):
        """test with 3 classes of cardinality 1
        and no zero degrees
        """
        A = np.array([[0, 1, 1],
                      [1, 0, 0],
                      [0, 1, 0],
			])

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='fixed-point', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 5: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_fp_dcm_6(self):
        """classes with cardinality > 1, no zero degree
        """
        n, seed = (4, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='fixed-point', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 6: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_fp_dcm_7(self):
        """classes with cardinality 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (5, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        A[0,:] = 0

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='fixed-point', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 7: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_qn_dcm_8(self):
        """classes with cardinality more than 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (4, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        A[0,:] = 0

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='fixed-point', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 8: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_qn_dcm_9(self):
        """classes with cardinality more than 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (100, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='fixed-point', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 9: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_n_dcm_10(self):
        """test with 3 classes of cardinality 1
        and no zero degrees
        """
        A = np.array([[0, 1, 1],
                      [1, 0, 0],
                      [0, 1, 0],
			])

        g = sample.DirectedGraph(A)


        g._solve_problem(model='dcm', method='newton', max_steps=200, verbose=False, initial_guess='uniform')

        g.solution_error()
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 10: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


    def test_n_dcm_11(self):
        """classes with cardinality more than 1 and zero degrees
        """
        # test Matrix 1
        n, seed = (4, 22)
        A = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        A[0,:] = 0

        g = sample.DirectedGraph(A)

        g._solve_problem(model='dcm', method='newton', max_steps=300, verbose=False, initial_guess='uniform')

        g.solution_error()
        # print('degseq = ', np.concatenate((g.dseq_out, g.dseq_in)))
        # print('expected degseq = ',g.expected_dseq)
        # debug
        # print(g.r_dseq_out)
        # print(g.r_dseq_in)
        # print(g.rnz_dseq_out)
        # print(g.rnz_dseq_in)
        # print('\ntest 11: error = {}'.format(g.error))

        # test result
        self.assertTrue(g.error < 1e-1)


if __name__ == '__main__':
    unittest.main()

