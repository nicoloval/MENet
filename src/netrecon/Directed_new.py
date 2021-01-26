import numpy as np
from numba import jit
from . import Directed_graph_Class as sample

# Stops Numba Warning for experimental feature
from numba.core.errors import NumbaExperimentalFeatureWarning
import warnings

warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)


@jit(nopython=True)
def iterative_dcm_new(theta, args):
    """Returns the next DBCM iterative step for the fixed-point [1]_ [2]_.
        It is based on the exponential version of the DBCM.
        This version only runs on non-zero indices.

    :param theta: Previous iterative step.
    :type theta: numpy.ndarray
    :param args: Out and in strengths sequences, adjacency matrix,
        and non zero out and in indices.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Next iterative step.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Squartini, Tiziano, and Diego Garlaschelli.
        "Analytical maximum-likelihood method to detect patterns
        in real networks."
        New Journal of Physics 13.8 (2011): 083001.
        `https://arxiv.org/abs/1103.0701 <https://arxiv.org/abs/1103.0701>`_

    .. [2] Squartini, Tiziano, Rossana Mastrandrea, and Diego Garlaschelli.
        "Unbiased sampling of network ensembles."
        New Journal of Physics 17.2 (2015): 023052.
        `https://arxiv.org/abs/1406.1197 <https://arxiv.org/abs/1406.1197>`_
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    n = len(k_out)
    # nz_index_out = args[2]
    # nz_index_in = args[3]
    nz_index_out = range(n)
    nz_index_in = range(n)
    c = args[4]

    f = np.zeros(2 * n, dtype=np.float64)
    x = np.exp(-theta)

    for i in nz_index_out:
        for j in nz_index_in:
            if j != i:
                f[i] += c[j] * x[j + n] / (1 + x[i] * x[j + n])
            else:
                f[i] += (c[j] - 1) * x[j + n] / (1 + x[i] * x[j + n])

    for j in nz_index_in:
        for i in nz_index_out:
            if j != i:
                f[j + n] += c[i] * x[i] / (1 + x[i] * x[j + n])
            else:
                f[j + n] += (c[i] - 1) * x[i] / (1 + x[i] * x[j + n])

    tmp = np.concatenate((k_out, k_in))
    # ff = np.array([tmp[i]/f[i] if tmp[i] != 0 else 0 for i in range(2*n)])
    ff = -np.log(tmp / f)

    return ff


@jit(nopython=True)
def iterative_dcm_new_2(theta, args):
    """Returns the next DBCM iterative step for the fixed-point.
        It is based on the exponential version of the DBCM.
        This version only runs on non-zero indices.

    :param theta: Previous iterative step.
    :type theta: numpy.ndarray
    :param args: Out and in strengths sequences, adjacency matrix,
        and non zero out and in indices.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Next iterative step.
    :rtype: numpy.ndarray
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    n = len(k_out)
    nz_index_out = args[2]
    nz_index_in = args[3]
    # nz_index_out = range(n)
    # nz_index_in = range(n)
    c = args[4]

    f = np.zeros(2 * n, dtype=np.float64)
    x = np.exp(-theta)

    for i in nz_index_out:
        for j in nz_index_in:
            if j != i:
                f[i] += c[j] * x[j + n] / (1 + x[i] * x[j + n])
            else:
                f[i] += (c[j] - 1) * x[j + n] / (1 + x[i] * x[j + n])

    for j in nz_index_in:
        for i in nz_index_out:
            if j != i:
                f[j + n] += c[i] * x[i] / (1 + x[i] * x[j + n])
            else:
                f[j + n] += (c[i] - 1) * x[i] / (1 + x[i] * x[j + n])

    tmp = np.concatenate((k_out, k_in))
    ff = -np.log(
        np.array(
            [tmp[i] / f[i] if tmp[i] != 0 else -np.infty for i in range(2 * n)]
        )
    )
    # ff = -np.log(tmp/f)

    return ff


@jit(nopython=True)
def loglikelihood_dcm_new(theta, args):
    """Returns DBCM [1]_ [2]_ loglikelihood function evaluated in theta.
    It is based on the exponential version of the DBCM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and non zero out and in indices,
        and classes cardinalities sequence.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Loglikelihood value.
    :rtype: float

    .. rubric: References
    .. [1] Squartini, Tiziano, and Diego Garlaschelli.
        "Analytical maximum-likelihood method to detect patterns
        in real networks."
        New Journal of Physics 13.8 (2011): 083001.
        `https://arxiv.org/abs/1103.0701 <https://arxiv.org/abs/1103.0701>`_

    .. [2] Squartini, Tiziano, Rossana Mastrandrea, and Diego Garlaschelli.
        "Unbiased sampling of network ensembles."
        New Journal of Physics 17.2 (2015): 023052.
        `https://arxiv.org/abs/1406.1197 <https://arxiv.org/abs/1406.1197>`_
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    nz_index_out = args[2]
    nz_index_in = args[3]
    # n = len(k_out)
    # nz_index_out = range(n)
    # nz_index_in = range(n)

    c = args[4]
    n = len(k_out)

    f = 0

    for i in nz_index_out:
        f -= c[i] * k_out[i] * theta[i]
        for j in nz_index_in:
            if i != j:
                f -= c[i] * c[j] * np.log(1 + np.exp(-theta[i] - theta[n + j]))
            else:
                f -= (
                    c[i]
                    * (c[i] - 1)
                    * np.log(1 + np.exp(-theta[i] - theta[n + j]))
                )

    for j in nz_index_in:
        f -= c[j] * k_in[j] * theta[j + n]

    return f


@jit(nopython=True)
def loglikelihood_prime_dcm_new(theta, args):
    """Returns DBCM [1]_ [2]_ loglikelihood gradient function evaluated in theta.
    It is based on the exponential version of the DBCM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood gradient.
        Out and in degrees sequences, and non zero out and in indices,
        and the sequence of classes cardinalities.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Loglikelihood gradient.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Squartini, Tiziano, and Diego Garlaschelli.
        "Analytical maximum-likelihood method to detect patterns
        in real networks."
        New Journal of Physics 13.8 (2011): 083001.
        `https://arxiv.org/abs/1103.0701 <https://arxiv.org/abs/1103.0701>`_

    .. [2] Squartini, Tiziano, Rossana Mastrandrea, and Diego Garlaschelli.
        "Unbiased sampling of network ensembles."
        New Journal of Physics 17.2 (2015): 023052.
        `https://arxiv.org/abs/1406.1197 <https://arxiv.org/abs/1406.1197>`_
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    nz_index_out = args[2]
    nz_index_in = args[3]
    c = args[4]
    n = len(k_in)

    f = np.zeros(2 * n)
    x = np.exp(-theta)

    for i in nz_index_out:
        fx = 0
        for j in nz_index_in:
            if i != j:
                const = c[i] * c[j]
                # const = c[j]
            else:
                const = c[i] * (c[j] - 1)
                # const = (c[j] - 1)

            fx += const * x[j + n] / (1 + x[i] * x[j + n])
        # f[i] = x[i]*fx - k_out[i]
        f[i] = x[i] * fx - c[i] * k_out[i]

    for j in nz_index_in:
        fy = 0
        for i in nz_index_out:
            if i != j:
                const = c[i] * c[j]
                # const = c[i]
            else:
                const = c[i] * (c[j] - 1)
                # const = (c[j] - 1)

            fy += const * x[i] / (1 + x[j + n] * x[i])
        # f[j+n] = fy*x[j+n] - k_in[j]
        f[j + n] = fy * x[j + n] - c[j] * k_in[j]

    return f


@jit(nopython=True)
def loglikelihood_hessian_dcm_new(theta, args):
    """Returns DBCM [1]_ [2]_ loglikelihood hessian function evaluated in theta.
    It is based on the exponential version of the DBCM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and non zero out and in indices,
        and the sequence of classes cardinalities.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Loglikelihood hessian matrix.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Squartini, Tiziano, and Diego Garlaschelli.
        "Analytical maximum-likelihood method to detect patterns
         in real networks."
        New Journal of Physics 13.8 (2011): 083001.
        `https://arxiv.org/abs/1103.0701 <https://arxiv.org/abs/1103.0701>`_

    .. [2] Squartini, Tiziano, Rossana Mastrandrea, and Diego Garlaschelli.
        "Unbiased sampling of network ensembles."
        New Journal of Physics 17.2 (2015): 023052.
        `https://arxiv.org/abs/1406.1197 <https://arxiv.org/abs/1406.1197>`_
    """

    k_out = args[0]
    k_in = args[1]
    nz_out_index = args[2]
    nz_in_index = args[3]
    c = args[4]
    n = len(k_out)

    out = np.zeros((2 * n, 2 * n))  # hessian matrix
    x = np.exp(-theta)

    for h in nz_out_index:
        tmp_sum = 0
        for i in nz_in_index:
            if i == h:
                const = c[h] * (c[h] - 1)
                # const = (c[h] - 1)
            else:
                const = c[h] * c[i]
                # const = c[i]

            tmp = x[i + n] * x[h]
            tmp_sum += const * (tmp) / (1 + tmp) ** 2
            out[h, i + n] = -const * tmp / (1 + tmp) ** 2
        out[h, h] = -tmp_sum

    for i in nz_in_index:
        tmp_sum = 0
        for h in nz_out_index:
            if i == h:
                const = c[h] * (c[h] - 1)
                # const = (c[i] - 1)
            else:
                const = c[h] * c[i]
                # const = c[h]

            tmp = x[h] * x[i + n]
            tmp_sum += const * (tmp) / (1 + tmp) ** 2
            out[i + n, h] = -const * tmp / (1 + tmp) ** 2
        out[i + n, i + n] = -tmp_sum
    return out


@jit(nopython=True)
def loglikelihood_hessian_diag_dcm_new(theta, args):
    """Returns the diagonal of the DBCM [1]_ [2]_ loglikelihood hessian
    function evaluated in theta. It is based on DBCM exponential version.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and non zero out and in indices,
        and the sequence of classes cardinalities.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Loglikelihood hessian diagonal.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Squartini, Tiziano, and Diego Garlaschelli.
        "Analytical maximum-likelihood method to detect patterns
         in real networks."
        New Journal of Physics 13.8 (2011): 083001.
        `https://arxiv.org/abs/1103.0701 <https://arxiv.org/abs/1103.0701>`_

    .. [2] Squartini, Tiziano, Rossana Mastrandrea, and Diego Garlaschelli.
        "Unbiased sampling of network ensembles."
        New Journal of Physics 17.2 (2015): 023052.
        `https://arxiv.org/abs/1406.1197 <https://arxiv.org/abs/1406.1197>`_
    """
    # problem fixed paprameters
    k_out = args[0]
    k_in = args[1]
    nz_index_out = args[2]
    nz_index_in = args[3]
    c = args[4]
    n = len(k_in)

    f = -np.zeros(2 * n)
    x = np.exp(-theta)

    for i in nz_index_out:
        fx = 0
        for j in nz_index_in:
            if i != j:
                const = c[i] * c[j]
                # const = c[j]
            else:
                const = c[i] * (c[j] - 1)
                # const = (c[i] - 1)

            tmp = x[j + n] * x[i]
            fx += const * (tmp) / (1 + tmp) ** 2
        # original prime
        f[i] = -fx

    for j in nz_index_in:
        fy = 0
        for i in nz_index_out:
            if i != j:
                const = c[i] * c[j]
                # const = c[i]
            else:
                const = c[i] * (c[j] - 1)
                # const = (c[j] - 1)

            tmp = x[i] * x[j + n]
            fy += const * (tmp) / (1 + tmp) ** 2
        # original prime
        f[j + n] = -fy

    # f[f == 0] = 1

    return f


@jit(nopython=True)
def expected_out_degree_dcm_new(sol):
    """Expected out-degrees after the DBCM. It is based on DBCM
    exponential version.

    :param sol: DBCM solution.
    :type sol: numpy.ndarray
    :return: Out-degrees DBCM expectation.
    :rtype: numpy.ndarray
    """
    n = int(len(sol) / 2)
    ex_k = np.zeros(n, dtype=np.float64)

    for i in np.arange(n):
        for j in np.arange(n):
            if i != j:
                aux = np.exp(-sol[i]) * np.exp(-sol[j])
                ex_k[i] += aux / (1 + aux)
    return ex_k


@jit(nopython=True)
def expected_in_degree_dcm_new(theta):
    """Expected in-degrees after the DBCM. It is based on DBCM
    exponential version.

    :param sol: DBCM solution.
    :type sol: numpy.ndarray
    :return: In-degrees DBCM expectation.
    :rtype: numpy.ndarray
    """
    sol = np.exp(-theta)
    n = int(len(sol) / 2)
    a_out = sol[:n]
    a_in = sol[n:]
    k = np.zeros(n)  # allocate k
    for i in range(n):
        for j in range(n):
            if i != j:
                k[i] += a_in[i] * a_out[j] / (1 + a_in[i] * a_out[j])

    return k


@jit(nopython=True)
def expected_decm_new(theta):
    """Expected parameters after the DBCM.
    It returns a concatenated array of out-degrees and in-degrees.
    It is based on DBCM exponential version.

    :param theta: DBCM solution.
    :type x: numpy.ndarray
    :return: DBCM expected parameters sequence.
    :rtype: numpy.ndarray
    """
    x = np.exp(-theta)
    n = int(len(x) / 4)
    f = np.zeros_like(x, np.float64)

    for i in range(n):
        fa_out = 0
        fa_in = 0
        fb_out = 0
        fb_in = 0
        for j in range(n):
            if i != j:
                fa_out += (
                    x[j + n]
                    * x[i + 2 * n]
                    * x[j + 3 * n]
                    / (
                        1
                        - x[i + 2 * n] * x[j + 3 * n]
                        + x[i] * x[j + n] * x[i + 2 * n] * x[j + 3 * n]
                    )
                )
                fa_in += (
                    x[j]
                    * x[j + 2 * n]
                    * x[i + 3 * n]
                    / (
                        1
                        - x[j + 2 * n] * x[i + 3 * n]
                        + x[j] * x[i + n] * x[j + 2 * n] * x[i + 3 * n]
                    )
                )
                fb_out += x[j + 3 * n] / (1 - x[j + 3 * n] * x[i + 2 * n]) + (
                    x[j + n] * x[i] - 1
                ) * x[j + 3 * n] / (
                    1
                    - x[i + 2 * n] * x[j + 3 * n]
                    + x[i] * x[j + n] * x[i + 2 * n] * x[j + 3 * n]
                )
                fb_in += x[j + 2 * n] / (1 - x[i + 3 * n] * x[j + 2 * n]) + (
                    x[i + n] * x[j] - 1
                ) * x[j + 2 * n] / (
                    1
                    - x[j + 2 * n] * x[i + 3 * n]
                    + x[j] * x[i + n] * x[j + 2 * n] * x[i + 3 * n]
                )
        f[i] = x[i] * fa_out
        f[i + n] = x[i + n] * fa_in
        f[i + 2 * n] = x[i + 2 * n] * fb_out
        f[i + 3 * n] = x[i + 3 * n] * fb_in

    return f


# decm functions


@jit(nopython=True)
def loglikelihood_decm_new(x, args):
    """Returns DECM [1]_ loglikelihood function evaluated in theta.
    It is based on the exponential version of the DECM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and out and in strengths sequences
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray)
    :return: Loglikelihood value.
    :rtype: float

    .. rubric: References
    .. [1] Parisi, Federica, Tiziano Squartini, and Diego Garlaschelli.
        "A faster horse on a safer trail: generalized inference for the
        efficient reconstruction of weighted networks."
        New Journal of Physics 22.5 (2020): 053053.
        `https://arxiv.org/abs/1811.09829 <https://arxiv.org/abs/1811.09829>`_
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]
    n = len(k_out)

    f = 0
    for i in range(n):
        if k_out[i]:
            f -= k_out[i] * x[i]
        if k_in[i]:
            f -= k_in[i] * x[i + n]
        if s_out[i]:
            f -= s_out[i] * (x[i + 2 * n])
        if s_in[i]:
            f -= s_in[i] * (x[i + 3 * n])
        for j in range(n):
            if i != j:
                tmp = np.exp(-x[i + 2 * n] - x[j + 3 * n])
                f -= np.log(1 + np.exp(-x[i] - x[j + n]) * tmp / (1 - tmp))

    return f


# @jit(nopython=True)
def loglikelihood_prime_decm_new(theta, args):
    """Returns DECM [1]_ loglikelihood gradient function evaluated in theta.
    It is based on the exponential version of the DECM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and out and in strengths sequences.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray)
    :return: Loglikelihood gradient.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Parisi, Federica, Tiziano Squartini, and Diego Garlaschelli.
        "A faster horse on a safer trail: generalized inference for the
        efficient reconstruction of weighted networks."
        New Journal of Physics 22.5 (2020): 053053.
        `https://arxiv.org/abs/1811.09829 <https://arxiv.org/abs/1811.09829>`_
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]
    n = len(k_out)

    x = np.exp(-theta)

    f = np.zeros(4 * n)
    for i in range(n):
        fa_out = 0
        fb_out = 0
        fa_in = 0
        fb_in = 0
        for j in range(n):
            if i != j:
                tmp0 = x[i + 2 * n] * x[j + 3 * n]
                tmp1 = x[i] * x[j + n]
                fa_out += tmp0 * tmp1 / (1 - tmp0 + tmp0 * tmp1)
                fb_out += tmp0 * tmp1 / ((1 - tmp0 + tmp0 * tmp1) * (1 - tmp0))

                tmp0 = x[j + 2 * n] * x[i + 3 * n]
                tmp1 = x[j] * x[i + n]
                fa_in += tmp0 * tmp1 / (1 - tmp0 + tmp0 * tmp1)
                fb_in += tmp0 * tmp1 / ((1 - tmp0 + tmp0 * tmp1) * (1 - tmp0))

        f[i] = -k_out[i] + fa_out
        f[i + 2 * n] = -s_out[i] + fb_out
        f[i + n] = -k_in[i] + fa_in
        f[i + 3 * n] = -s_in[i] + fb_in

    return f


@jit(nopython=True)
def loglikelihood_hessian_decm_new(theta, args):
    """Returns DECM [1]_ loglikelihood hessian function evaluated in theta.
    It is based on the exponential version of the DECM.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood function.
        Out and in degrees sequences, and out and in strengths sequences..
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray)
    :return: Loglikelihood hessian matrix.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Parisi, Federica, Tiziano Squartini, and Diego Garlaschelli.
        "A faster horse on a safer trail: generalized inference for the
        efficient reconstruction of weighted networks."
        New Journal of Physics 22.5 (2020): 053053.
        `https://arxiv.org/abs/1811.09829 <https://arxiv.org/abs/1811.09829>`_
    """
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]

    n = len(k_out)
    f = np.zeros((n * 4, n * 4))
    x = np.exp(-theta)

    a_out = x[:n]
    a_in = x[n: 2 * n]
    b_out = x[2 * n: 3 * n]
    b_in = x[3 * n:]

    for i in range(n):
        for j in range(n):
            if j != i:
                tmp0 = a_out[i] * a_in[j]
                tmp1 = b_out[i] * b_in[j]
                # diagonal elements
                f[i, i] -= (
                    (1 - tmp1) * tmp0 * tmp1 / ((1 + (-1 + tmp0) * tmp1) ** 2)
                )
                f[i + 2 * n, i + 2 * n] -= (
                    tmp0
                    * tmp1
                    * (1 + (tmp0 - 1) * (tmp1 ** 2))
                    / ((1 - tmp1) * (1 + (tmp0 - 1) * tmp1)) ** 2
                )
                # out of diagonal
                f[i, j + n] = (
                    -(1 - tmp1) * tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                )
                f[j + n, i] = f[i, j + n]
                f[i, i + 2 * n] -= tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                f[i + 2 * n, i] = f[i, i + 2 * n]
                f[i, j + 3 * n] = -tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                f[j + 3 * n, i] = f[i, j + 3 * n]
                f[i + 2 * n, j + 3 * n] = (
                    -tmp0
                    * tmp1
                    * (1 + (tmp0 - 1) * tmp1 ** 2)
                    / (((1 - tmp1) ** 2) * ((1 + (tmp0 - 1) * tmp1) ** 2))
                )
                f[j + 3 * n, i + 2 * n] = f[i + 2 * n, j + 3 * n]

                tmp0 = a_out[j] * a_in[i]
                tmp1 = b_out[j] * b_in[i]
                # diagonal elements
                f[i + n, i + n] -= (
                    (1 - tmp1) * tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                )
                f[i + 3 * n, i + 3 * n] -= (
                    tmp0
                    * tmp1
                    * (1 + (tmp0 - 1) * tmp1 ** 2)
                    / (((1 - tmp1) ** 2) * ((1 + (tmp0 - 1) * tmp1) ** 2))
                )
                # out of diagonal
                f[i + n, j + 2 * n] = (
                    -tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                )
                f[j + 2 * n, i + n] = f[i + n, j + 2 * n]
                f[i + n, i + 3 * n] -= (
                    tmp0 * tmp1 / (1 + (tmp0 - 1) * tmp1) ** 2
                )
                f[i + 3 * n, i + n] = f[i + n, i + 3 * n]

    f = f
    for i in range(4 * n):
        for j in range(4 * n):
            if np.isnan(f[i, j]):
                f[i, j] = 0

    # print(np.isnan(f))
    return f


@jit(nopython=True)
def loglikelihood_hessian_diag_decm_new(theta, args):
    """Returns the diagonal of the DECM [1]_ loglikelihood hessian
    function evaluated in *theta*. It is based on the DECM exponential version.

    :param theta: Evaluating point *theta*.
    :type theta: numpy.ndarray
    :param args: Arguments to define the loglikelihood hessian.
        Out and in degrees sequences, and out and in strengths sequences.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray)
    :return: Loglikelihood hessian diagonal.
    :rtype: numpy.ndarray

    .. rubric: References
    .. [1] Parisi, Federica, Tiziano Squartini, and Diego Garlaschelli.
        "A faster horse on a safer trail: generalized inference for the
        efficient reconstruction of weighted networks."
        New Journal of Physics 22.5 (2020): 053053.
        `https://arxiv.org/abs/1811.09829 <https://arxiv.org/abs/1811.09829>`_
    """
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]

    n = len(k_out)
    f = np.zeros(n * 4)
    x = np.exp(-theta)

    a_out = x[:n]
    a_in = x[n: 2 * n]
    b_out = x[2 * n: 3 * n]
    b_in = x[3 * n:]

    for i in range(n):
        for j in range(n):
            if j != i:
                tmp0 = a_out[i] * a_in[j]
                tmp1 = b_out[i] * b_in[j]
                # diagonal elements
                f[i] -= (
                    (1 - tmp1) * tmp0 * tmp1 / ((1 - tmp1 + tmp0 * tmp1) ** 2)
                )
                f[i + 2 * n] -= (
                    tmp0
                    * tmp1
                    * (1 - tmp1 ** 2 + tmp0 * (tmp1 ** 2))
                    / ((1 - tmp1) * (1 - tmp1 + tmp0 * tmp1)) ** 2
                )

                tmp0 = a_out[j] * a_in[i]
                tmp1 = b_out[j] * b_in[i]
                # diagonal elements
                f[i + n] -= (
                    (1 - tmp1) * tmp0 * tmp1 / (1 - tmp1 + tmp0 * tmp1) ** 2
                )
                f[i + 3 * n] -= (
                    tmp0
                    * tmp1
                    * (1 - tmp1 ** 2 + tmp0 * tmp1 ** 2)
                    / (((1 - tmp1) ** 2) * ((1 - tmp1 + tmp0 * tmp1) ** 2))
                )

    f = f

    return f


@jit(nopython=True)
def iterative_decm_new(theta, args):
    """Returns the next iterative step for the DECM.
    It is based on the exponential version of the DBCM.

    :param theta: Previous iterative step.
    :type theta: numpy.ndarray
    :param args: Out and in degrees sequences, and out and in strengths
        sequences.
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Next iterative step.
    :rtype: numpy.ndarray
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]
    n = len(k_out)

    x = np.exp(-theta)

    f = np.zeros(4 * n)
    for i in range(n):
        fa_out = 0
        fb_out = 0
        fa_in = 0
        fb_in = 0
        for j in range(n):
            if i != j:
                tmp0 = x[i] * x[j + n]
                tmp1 = x[i + 2 * n] * x[j + 3 * n]

                fa_out += x[j + n] * tmp1 / (1 - tmp1 + tmp0 * tmp1)

                fb_out += (
                    tmp0
                    * x[j + 3 * n]
                    / ((1 - tmp1) * (1 - tmp1 + tmp0 * tmp1))
                )

                tmp0 = x[j] * x[i + n]
                tmp1 = x[j + 2 * n] * x[i + 3 * n]

                fa_in += x[j + n] * tmp1 / (1 - tmp1 + tmp0 * tmp1)

                fb_in += (
                    tmp0
                    * x[j + 3 * n]
                    / ((1 - tmp1) * (1 - tmp1 + tmp0 * tmp1))
                )

        if k_out[i]:
            f[i] = -np.log(k_out[i] / fa_out)
        else:
            f[i] = 1e3

        if s_out[i]:
            f[i + 2 * n] = -np.log(s_out[i] / fb_out)
        else:
            f[i + 2 * n] = 1e3

        if k_in[i]:
            f[i + n] = -np.log(k_in[i] / fa_in)
        else:
            f[i + n] = 1e3

        if s_in[i]:
            f[i + 3 * n] = -np.log(s_in[i] / fb_in)
        else:
            f[i + 3 * n] = 1e3

    return f


@jit(nopython=True)
def iterative_decm_new_2(theta, args):
    """Returns the next iterative step for the DECM.
    It is based on the exponential version of the DBCM.

    :param theta: Previous iterative step.
    :type theta: numpy.ndarray
    :param args: Out and in degrees sequences, and out and in strengths
        sequences..
    :type args: (numpy.ndarray, numpy.ndarray, numpy.ndarray,
        numpy.ndarray, numpy.ndarray)
    :return: Next iterative step.
    :rtype: numpy.ndarray
    """
    # problem fixed parameters
    k_out = args[0]
    k_in = args[1]
    s_out = args[2]
    s_in = args[3]
    n = len(k_out)

    x = np.exp(-theta)

    f = np.zeros(4 * n)
    for i in range(n):
        fa_out = 0
        fb_out = 0
        fa_in = 0
        fb_in = 0
        for j in range(n):
            if i != j:
                tmp0 = x[i + 2 * n] * x[j + 3 * n]
                tmp1 = tmp0 / (1 - tmp0)
                tmp2 = x[i] * x[j + n]

                fa_out += x[j + n] * tmp1 / (1 + tmp2 * tmp1)

                fb_out += (
                    tmp2 * x[j + 3 * n] / ((1 + tmp0 * tmp2) * (1 - tmp0))
                )

                tmp0 = x[j + 2 * n] * x[i + 3 * n]
                tmp1 = tmp0 / (1 - tmp0)
                tmp2 = x[j] * x[i + n]

                fa_in += x[j] * tmp1 / (1 + tmp2 * tmp1)

                fb_in += tmp2 * x[j + 2 * n] / ((1 + tmp0 * tmp2) * (1 - tmp0))

        # print('this',fb_out)
        f[i] = -np.log(k_out[i] / fa_out)
        f[i + 2 * n] = -np.log(s_out[i] / fb_out)
        f[i + n] = -np.log(k_in[i] / fa_in)
        f[i + 3 * n] = -np.log(s_in[i] / fb_in)

    return f
