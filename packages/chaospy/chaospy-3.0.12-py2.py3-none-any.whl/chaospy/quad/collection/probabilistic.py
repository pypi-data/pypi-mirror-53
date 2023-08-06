"""
Implementation of probabilistic collocation method.

Here subsamples of the Golub-Welsch method is removed at random and weights
renormalized.
"""
import numpy
import chaospy.quad


def probabilistic_collocation(order, dist, subset=.1):
    """
    Probabilistic collocation method.

    Args:
        order (int, numpy.ndarray) : Quadrature order along each axis.
        dist (Dist) : Distribution to generate samples from.
        subset (float) : Rate of which to removed samples.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            abscissas:
                The quadrature points for where to evaluate the model function
                with ``abscissas.shape == (len(dist), N)`` where ``N`` is the
                number of samples.
            weights:
                The quadrature weights with ``weights.shape == (N,)``.
    """
    abscissas, weights = chaospy.quad.collection.golub_welsch(order, dist)

    likelihood = dist.pdf(abscissas)

    alpha = numpy.random.random(len(weights))
    alpha = likelihood > alpha*subset*numpy.max(likelihood)

    abscissas = abscissas.T[alpha].T
    weights = weights[alpha]
    return abscissas, weights
