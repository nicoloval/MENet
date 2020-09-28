import sys
sys.path.append('../')
import Directed_graph_Class as sample
from Directed_new import *
import Matrix_Generator as mg
import numpy as np
import unittest  # test tool
from scipy.optimize import approx_fprime

class MyTest(unittest.TestCase):


    def setUp(self):
        pass


    def test_iterative_dcm_new(self):

        n, seed = (3, 42)
        a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)

        # rd
        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'fixed-point')
        # theta = np.random.rand(6) 
        theta = np.array([np.infty, 0.5, 0.5, 0.5, np.infty, 0.5]) 
        x0 = np.exp(-theta)

        f_sample = g.fun(x0)
        g.last_model = 'dcm'
        g._set_solved_problem(f_sample)
        f_full = np.concatenate((g.x, g.y))
        f_full = -np.log(f_full)
        f_new = iterative_dcm_new(theta, g.args)
        g._set_solved_problem_dcm(f_new)
        f_new_full = np.concatenate((g.x, g.y))


        # f_new_bis = iterative_dcm_new_bis(theta, g.args)
        # print('normale ',f_new)
        # print('bis',f_new_bis)

        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_full)
        # print(f_new)
        # print(f_new_full)

        # test result
        self.assertTrue(np.allclose(f_full, f_new_full))


    def test_loglikelihood_dcm_new(self):

        n, seed = (3, 42)
        # a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)
        a = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0]])

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'newton')
        theta = np.array([np.infty, 0.5, 0.5, 0.5, 0.5, 0.5]) 
        x0 = np.exp(-theta)

        k_out = g.args[0]
        k_in = g.args[1]
        nz_index_out = g.args[2]
        nz_index_in = g.args[3]

        f_sample = g.step_fun(x0) 
        g.last_model = 'dcm'
        f_new = -loglikelihood_dcm_new(theta, g.args)


        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_sample)
        # print(f_sample)
        # print(f_new)

        # test result
        self.assertTrue(f_sample == f_new)


    def test_loglikelihood_prime_dcm_new(self):

        n, seed = (3, 42)
        # a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)
        a = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0]])

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'newton')
        theta = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) 
        x0 = np.exp(-theta)

        k_out = g.args[0]
        k_in = g.args[1]
        nz_index_out = g.args[2]
        nz_index_in = g.args[3]

        f = lambda x: loglikelihood_dcm_new(x, g.args)
        f_sample = approx_fprime(theta, f, epsilon=1e-6)  
        g.last_model = 'dcm'
        f_new = loglikelihood_prime_dcm_new(theta, g.args)


        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_sample)
        # print(f_new)

        # test result
        self.assertTrue(np.allclose(f_sample,f_new))


    def test_loglikelihood_hessian_dcm_new(self):

        n, seed = (3, 42)
        # a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)
        a = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0]])

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'newton')
        theta = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) 
        x0 = np.exp(-theta)

        k_out = g.args[0]
        k_in = g.args[1]
        nz_index_out = g.args[2]
        nz_index_in = g.args[3]

        f = lambda x: loglikelihood_prime_dcm_new(x, g.args)[1]
        f_sample = approx_fprime(theta, f, epsilon=1e-6)  
        g.last_model = 'dcm'
        f_new = loglikelihood_hessian_dcm_new(theta, g.args)[1]


        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_sample)
        # print(f_new)

        # test result
        self.assertTrue(np.allclose(f_sample,f_new))


    def test_loglikelihood_hessian_diag_dcm_new(self):

        n, seed = (3, 42)
        # a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)
        a = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0]])

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'newton')
        theta = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) 
        x0 = np.exp(-theta)

        k_out = g.args[0]
        k_in = g.args[1]
        nz_index_out = g.args[2]
        nz_index_in = g.args[3]

        f_sample = np.zeros(6)
        for i in range(6):
            f = lambda x: loglikelihood_prime_dcm_new(x, g.args)[i]
            f_sample[i] = approx_fprime(theta, f, epsilon=1e-6)[i]  
        g.last_model = 'dcm'
        f_new = loglikelihood_hessian_diag_dcm_new(theta, g.args)


        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_sample)
        # print(f_new)

        # test result
        self.assertTrue(np.allclose(f_sample,f_new))


    def test_loglikelihood_hessian_diag_vs_normal_dcm_new(self):

        n, seed = (3, 42)
        # a = mg.random_binary_matrix_generator_dense(n, sym=False, seed=seed)
        a = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [1, 1, 0]])

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'newton')
        theta = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) 
        x0 = np.exp(-theta)

        k_out = g.args[0]
        k_in = g.args[1]
        nz_index_out = g.args[2]
        nz_index_in = g.args[3]

        g.last_model = 'dcm'
        f_diag = loglikelihood_hessian_diag_dcm_new(theta, g.args)
        f_full = loglikelihood_hessian_dcm_new(theta, g.args)
        f_full_d = np.diag(f_full)


        # debug
        # print(a)
        # print(theta, x0)
        # print(g.args)
        # print(f_sample)
        # print(f_new)

        # test result
        self.assertTrue(np.allclose(f_diag, f_full_d))



if __name__ == '__main__':
    unittest.main()
