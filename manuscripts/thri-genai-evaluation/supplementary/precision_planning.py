"""Precision-planning tables for the manuscript.

Table A: exact (Clopper-Pearson) 95% confidence intervals for a success
         proportion estimated from n physical robot trials.
Table B: Monte Carlo sampling variability of Cohen's kappa between a model
         and a human reference coder on a validation subset of n items, as a
         function of the true kappa and the prevalence of the positive class.

Run:  python3 precision_planning.py   (requires numpy and scipy)
"""
import numpy as np
from scipy.stats import beta

RNG = np.random.default_rng(20261124)


def clopper_pearson(k, n, level=0.95):
    a = 1 - level
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def kappa_sampling(kappa, prev, n, reps=20000):
    """Two raters with equal marginals `prev` and true agreement `kappa`."""
    pq = prev * (1 - prev)
    probs = [prev**2 + kappa * pq,           # both positive
             (1 - prev)**2 + kappa * pq,     # both negative
             (1 - kappa) * pq,               # rater A only
             (1 - kappa) * pq]               # rater B only
    counts = RNG.multinomial(n, probs, size=reps).astype(float)
    a, d, b, c = counts.T
    po = (a + d) / n
    p1, p2 = (a + b) / n, (a + c) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    with np.errstate(divide="ignore", invalid="ignore"):
        k = (po - pe) / (1 - pe)
    ok = np.isfinite(k)
    lo, hi = np.percentile(k[ok], [2.5, 97.5])
    expected_po = 1 - 2 * (1 - kappa) * pq
    return lo, hi, 1 - ok.mean(), expected_po


if __name__ == "__main__":
    print("Table A. Clopper-Pearson 95% CI for k successes in n trials")
    for n in (10, 20, 50, 100):
        row = []
        for rate in (0.5, 0.7, 0.9):
            k = round(rate * n)
            lo, hi = clopper_pearson(k, n)
            row.append(f"{k}/{n}: [{lo:.2f}, {hi:.2f}]")
        print("  n=%3d  " % n + "   ".join(row))

    print("\nTable B. Central 95% range of estimated Cohen's kappa")
    for prev in (0.5, 0.1):
        for kappa in (0.4, 0.6, 0.8):
            cells = []
            for n in (50, 100, 200, 400):
                lo, hi, undefined, po = kappa_sampling(kappa, prev, n)
                cells.append(f"n={n}: [{lo:.2f}, {hi:.2f}]")
            print(f"  prev={prev:.1f} kappa={kappa:.1f} (expected raw agreement "
                  f"{po:.2f})  " + "  ".join(cells))

    print("\nPrevalence illustration: expected raw agreement when kappa = 0.2")
    for prev in (0.5, 0.2, 0.1, 0.05):
        print(f"  prevalence {prev:.2f}: raw agreement "
              f"{1 - 2 * 0.8 * prev * (1 - prev):.2f}")
