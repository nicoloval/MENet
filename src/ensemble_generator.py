import multiprocessing as mp
import numpy as np
import sys
# Stops Numba Warning for experimental feature
from numba.core.errors import NumbaExperimentalFeatureWarning
import warnings

warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)


def ensemble_sampler_cm_graph(outfile_name, x, cpu_n=2, seed=None):
    # produce and write a single undirected binary graph
    if seed is not None:
        np.random.seed(seed)

    inds = np.arange(len(x))

    # put together inputs for pool
    # iter_ = itertools.product(zip(inds,x), zip(inds,x))
    # print(list(zip(inds, x)))
    iter_ = iter(
        ((i, xi), (j, xj), np.random.randint(0, 1000000))
        for i, xi in zip(inds, x)
        for j, xj in zip(inds, x)
        if i < j)

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_cm, iter_)

    # removing None
    edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {}\n".format(str(i), str(j))
                for (i, j) in edges_list)
            )

    return outfile_name


def ensemble_sampler_ecm_graph(outfile_name, x, y, cpu_n=2, seed=None):
    # produce and write a single undirected weighted graph
    if seed is not None:
        np.random.seed(seed)

    inds = np.arange(len(x))

    # put together inputs for pool
    # iter_ = itertools.product(zip(inds,x), zip(inds,x))
    # print(list(zip(inds, x)))
    iter_ = iter(
        ((i, xi, yi), (j, xj, yj), np.random.randint(0, 1000000))
        for i, xi, yi in zip(inds, x, y)
        for j, xj, yj in zip(inds, x, y)
        if i < j)

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_ecm, iter_)

    # removing None
    edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_dcm_graph(outfile_name, x, y, cpu_n=2, seed=None):
    # produce and write a single directed binary graph
    if seed is not None:
        np.random.seed(seed)

    inds = np.arange(len(x))

    # put together inputs for pool
    iter_ = iter(((i, xi), (j, yj), np.random.randint(0, 1000000))
                 for i, xi in zip(inds, x)
                 for j, yj in zip(inds, y)
                 if i != j)

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_dcm, iter_)

    # removing None
    edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {}\n".format(str(i), str(j))
                for (i, j) in edges_list)
            )

    return outfile_name


def ensemble_sampler_decm_graph(
        outfile_name,
        a_out, a_in,
        b_out, b_in,
        cpu_n=2,
        seed=None):
    # produce and write a single directed weighted graph

    if seed is not None:
        np.random.seed(seed)

    inds = np.arange(len(a_out))

    # put together inputs for pool
    iter_ = iter((
                    (i, a_out_i, b_out_i),
                    (j, a_in_j, b_in_j),
                    np.random.randint(0, 1000000))
                 for i, a_out_i, b_out_i in zip(inds, a_out, b_out)
                 for j, a_in_j, b_in_j in zip(inds, a_in, b_in)
                 if i != j)

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_decm, iter_)

    # removing None
    edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_ecm_det_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    (row_inds, col_inds, weigths_value) = adj
    del weigths_value

    # put together inputs for pool
    iter_ = iter(
        ((i, beta[i]), (j, beta[j]), np.random.randint(0, 1000000))
        for i, j in zip(row_inds, col_inds)
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_ecm_det, iter_)

    # removing None
    # commented cause there should be no None
    # edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_ecm_prob_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    (row_inds, col_inds, weigths_value) = adj

    # put together inputs for pool
    iter_ = iter(
        ((i, beta[i]), (j, beta[j]), w_prob, np.random.randint(0, 1000000))
        for i, j, w_prob in zip(row_inds, col_inds, weigths_value)
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_ecm_prob, iter_)

    # removing None
    # commented cause there should be no None
    # edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_sparse_ecm_prob_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    x = adj[0]
    n = len(x)

    # put together inputs for pool
    iter_ = iter(
        ((i, beta[i], x[i]), (j, beta[j], x[j]), np.random.randint(0, 1000000))
        for i in range(n)
        for j in range(n)
        if i != j
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_sparse_ecm_prob, iter_)

    # removing None
    # commented cause there should be no None
    # edges_list[:] = (value for value in edges_list if value is not None)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_decm_prob_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    b_out, b_in = beta

    (row_inds, col_inds, weigths_value) = adj

    # put together inputs for pool
    iter_ = iter(
        ((i, b_out[i]), (j, b_in[j]), w_prob, np.random.randint(0, 1000000))
        for i, j, w_prob in zip(row_inds, col_inds, weigths_value)
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_decm_prob, iter_)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_decm_det_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    b_out, b_in = beta

    (row_inds, col_inds, weigths_value) = adj
    del weigths_value

    # put together inputs for pool
    iter_ = iter(
        ((i, b_out[i]), (j, b_in[j]), np.random.randint(0, 1000000))
        for i, j in zip(row_inds, col_inds)
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_decm_det, iter_)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def ensemble_sampler_creama_sparse_decm_prob_graph(
        outfile_name,
        beta,
        adj,
        cpu_n=2,
        seed=None):
    """Produce and write a single undirected weighted graph."""
    if seed is not None:
        np.random.seed(seed)

    b_out, b_in = beta
    x, y = adj
    n = len(x)

    # put together inputs for pool
    iter_ = iter(
        (
            (i, b_out[i], x[i]),
            (j, b_in[j], y[j]),
            np.random.randint(0, 1000000))
        for i in range(n)
        for j in range(n)
        if i != j
    )

    # compute existing edges
    with mp.Pool(processes=cpu_n) as pool:
        edges_list = pool.starmap(is_a_link_creama_sparse_decm_prob, iter_)

    # debug
    # print(edges_list)

    # edgelist writing
    with open(outfile_name, "w") as outfile:
        outfile.write(
            "".join(
                "{} {} {}\n".format(str(i), str(j), str(w))
                for (i, j, w) in edges_list)
            )

    return outfile_name


def is_a_link_cm(args_1, args_2, seed=None):
    if seed is not None:
        np.random.seed(seed)
    (i, xi) = args_1
    (j, xj) = args_2
    p = np.random.random()
    xij = xi*xj
    p_ensemble = xij/(1 + xij)
    if p < p_ensemble:
        return (i, j)


def is_a_link_ecm(args_1, args_2, seed=None):
    # q-ensemble source: "Unbiased sampling of network ensembles", WUNs
    if seed is not None:
        np.random.seed(seed)
    (i, xi, yi) = args_1
    (j, xj, yj) = args_2
    p = np.random.random()
    xij = xi*xj
    yij = yi*yj
    p_ensemble = xij*yij/(1 - yij + xij*yij)
    if p < p_ensemble:
        q_ensemble = yij
        w = np.random.geometric(1-q_ensemble)
        return (i, j, w)


def is_a_link_dcm(args_1, args_2, seed=None):
    if seed is not None:
        np.random.seed(seed)
    (i, xi) = args_1
    (j, yj) = args_2
    p = np.random.random()
    tmp = xi*yj
    p_ensemble = tmp/(1 + tmp)
    if p < p_ensemble:
        return (i, j)


def is_a_link_decm(args_1, args_2, seed=None):
    # q-ensemble source:
    # "Fast and scalable resolution of the likelihood maximization problem
    # for Exponential Random Graph models"
    if seed is not None:
        np.random.seed(seed)
    (i, a_out_i, b_out_i) = args_1
    (j, a_in_j, b_in_j) = args_2
    p = np.random.random()
    aij = a_out_i * a_in_j
    bij = b_out_i * b_in_j
    p_ensemble = aij*bij/(1 - bij + aij*bij)
    if p < p_ensemble:
        q_ensemble = bij
        w = np.random.geometric(1-q_ensemble)
        return (i, j, w)


def is_a_link_creama_ecm_det(args_1, args_2, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, beta_i) = args_1
    (j, beta_j) = args_2

    q_ensemble = 1/(beta_i + beta_j)
    w_link = np.random.exponential(q_ensemble)
    return (i, j, w_link)


def is_a_link_creama_ecm_prob(args_1, args_2, p_ensemble, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, beta_i) = args_1
    (j, beta_j) = args_2

    p = np.random.random()
    if p < p_ensemble:
        q_ensemble = 1/(beta_i + beta_j)
        w_link = np.random.exponential(q_ensemble)
        return (i, j, w_link)


def is_a_link_creama_sparse_ecm_prob(args_1, args_2, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, beta_i, x_i) = args_1
    (j, beta_j, x_j) = args_2

    p = np.random.random()
    p_ensemble = x_i*x_j/(1 + x_j*x_i)
    if p < p_ensemble:
        q_ensemble = 1/(beta_i + beta_j)
        w_link = np.random.exponential(q_ensemble)
        return (i, j, w_link)


def is_a_link_creama_decm_det(args_1, args_2, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, b_out_i) = args_1
    (j, b_in_j) = args_2

    q_ensemble = 1/(b_out_i + b_in_j)
    w_link = np.random.exponential(q_ensemble)
    return (i, j, w_link)


def is_a_link_creama_decm_prob(args_1, args_2, p_ensemble, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, b_out_i) = args_1
    (j, b_in_j) = args_2

    p = np.random.random()
    if p < p_ensemble:
        q_ensemble = 1/(b_out_i + b_in_j)
        w_link = np.random.exponential(q_ensemble)
        return (i, j, w_link)


def is_a_link_creama_sparse_decm_prob(args_1, args_2, seed=None):
    """Q-ensemble source: "A faster Horse on a safer trail"."""
    if seed is not None:
        np.random.seed(seed)
    (i, b_out_i, x_i) = args_1
    (j, b_in_j, x_j) = args_2

    p = np.random.random()
    p_ensemble = x_i*x_j/(1 + x_j*x_i)
    if p < p_ensemble:
        q_ensemble = 1/(b_out_i + b_in_j)
        w_link = np.random.exponential(q_ensemble)
        return (i, j, w_link)