"""
The Gauss-Legendre quadrature rule is properly supported by in
:ref:`gaussian_quadrature`. However, as Gauss-Legendre is a special case where
the weight function is constant, it can in principle be used to integrate any
weighting function. In other words, this is the same Gauss-Legendre integration
rule, but only in the context of uniform distribution as weight function.
Normalization of the weights will be used to achieve the general integration
form.

It is also worth noting that this specific implementation of Gauss-Legendre is
faster to compute than the general version in :ref:`gaussian_quadrature`.

Example usage
-------------

The first few orders::

    >>> distribution = chaospy.Uniform(0, 1)
    >>> for order in [0, 1, 2, 3]:
    ...     abscissas, weights = chaospy.generate_quadrature(
    ...         order, distribution, rule="E", normalize=True)
    ...     print("{} {} {}".format(
    ...         order, numpy.around(abscissas, 3), numpy.around(weights, 3)))
    0 [[0.5]] [1.]
    1 [[0.211 0.789]] [0.5 0.5]
    2 [[0.113 0.5   0.887]] [0.278 0.444 0.278]
    3 [[0.069 0.33  0.67  0.931]] [0.174 0.326 0.326 0.174]

Using an alternative distribution::

    >>> distribution = chaospy.Beta(2, 4)
    >>> for order in [0, 1, 2, 3]:
    ...     abscissas, weights = chaospy.generate_quadrature(
    ...         order, distribution, rule="E", normalize=True)
    ...     print("{} {} {}".format(
    ...         order, numpy.around(abscissas, 3), numpy.around(weights, 3)))
    0 [[0.5]] [1.]
    1 [[0.211 0.789]] [0.933 0.067]
    2 [[0.113 0.5   0.887]] [0.437 0.556 0.007]
    3 [[0.069 0.33  0.67  0.931]] [0.195 0.647 0.157 0.001]

The abscissas stays the same, but the weights are re-adjusted for the new
weight function.
"""
import numpy

import chaospy.quad


def quad_gauss_legendre(order, lower=0, upper=1):
    """
    Generate the quadrature nodes and weights in Gauss-Legendre quadrature.

    Note that this rule exists to allow for integrating functions with weight
    functions without actually adding the quadrature. Like:

    .. math:
        \int_a^b p(x) f(x) dx \approx \sum_i p(X_i) f(X_i) W_i

    instead of the more traditional:

    .. math:
        \int_a^b p(x) f(x) dx \approx \sum_i f(X_i) W_i

    To get the behavior where the weight function is taken into consideration,
    use :func:`~chaospy.quad.collection.golub_welsch.quad_golub_welsch`.

    Args:
        order (int, numpy.ndarray):
            Quadrature order.
        lower (int, numpy.ndarray):
            Lower bounds of interval to integrate over.
        upper (int, numpy.ndarray):
            Upper bounds of interval to integrate over.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            abscissas:
                The quadrature points for where to evaluate the model function
                with ``abscissas.shape == (len(dist), N)`` where ``N`` is the
                number of samples.
            weights:
                The quadrature weights with ``weights.shape == (N,)``.

    Example:
        >>> abscissas, weights = quad_gauss_legendre(3)
        >>> print(numpy.around(abscissas, 4))
        [[0.0694 0.33   0.67   0.9306]]
        >>> print(numpy.around(weights, 4))
        [0.1739 0.3261 0.3261 0.1739]
    """
    order = numpy.asarray(order, dtype=int).flatten()
    lower = numpy.asarray(lower).flatten()
    upper = numpy.asarray(upper).flatten()

    dim = max(lower.size, upper.size, order.size)
    order = numpy.ones(dim, dtype=int)*order
    lower = numpy.ones(dim)*lower
    upper = numpy.ones(dim)*upper

    results = [_gauss_legendre(order[i]) for i in range(dim)]
    abscis = numpy.array([_[0] for _ in results])
    weights = numpy.array([_[1] for _ in results])

    abscis = chaospy.quad.combine(abscis)
    weights = chaospy.quad.combine(weights)

    abscis = (upper-lower)*abscis + lower
    weights = numpy.prod(weights*(upper-lower), -1)

    return abscis.T, weights


def _gauss_legendre(order):
    """Backend function."""
    inner = numpy.ones(order+1)*0.5
    outer = numpy.arange(order+1)**2
    outer = outer/(16*outer-4.)

    banded = numpy.diag(numpy.sqrt(outer[1:]), k=-1) + numpy.diag(inner) + \
            numpy.diag(numpy.sqrt(outer[1:]), k=1)
    vals, vecs = numpy.linalg.eig(banded)

    abscissas, weights = vals.real, vecs[0, :]**2
    indices = numpy.argsort(abscissas)
    abscissas, weights = abscissas[indices], weights[indices]
    return abscissas, weights
