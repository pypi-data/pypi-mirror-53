# HFTU: Hyperplane Folding Test of Unimodality

HFTU is another generalization of the [Folding Test of Unimodality](https://asiffer.github.io/libfolding/) (FTU) published in 2018:

*Siffer, A., Fouque, P. A., Termier, A., & Largouët, C. (2018, July). Are your data gathered?. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2210-2218). ACM.*

Like FTU, HFTU tests whether a multivariate distribution is unimodal or multimodal. The statistics both tests exploit is based on a folding mechanism of the distribution. While FTU uses a single point to perform point-wise folding, HFTU computes an hyperplane to fold the input distribution.

This repository contains a `python3` package, called `hftu`, to compute HFTU.

## Installation

`hftu` is available on PyPI, so you can download it through the `pip` package manager

```sh
pip3 install hftu
```

## Example


To perform the test we merely need to create an `HFTU` object and fit the data. The *folding statistics* from which the test is based can then be retrieved.

```python
import numpy as np
from hftu import HFTU

mean = [0, 0]
cov = [[2, 1], [1, 3]]
n = 1000
X = np.random.multivariate_normal(mean, cov, n)
h = HFTU()
opt_results = h.fit(X)
# Print the folding statistics
print(h.folding_statistics_)
```
```python3
0.8386729778145701
```

Once data are fit, one can perform the test itself. Indeed, the decision level must be tuned by the desired type I error *alpha*.
The value of *alpha* is the probability to declare a distribution multimodal while it is unimodal. In practice, it must be very low (close to zero).

```python
import numpy as np
from hftu import HFTU

dim = 5
mean = np.zeros(dim)
cov = np.eye(dim)
n = 2000
X = np.random.multivariate_normal(mean, cov, n)
h = HFTU()
opt_results = h.fit(X)
print(h.is_unimodal(alpha=1e-30))
```
```python3
True
```