
[![Build Status](https://travis-ci.org/ibigpapa/bin_packing_problem.svg?branch=master)](https://travis-ci.org/ibigpapa/bin_packing_problem)

# Bin Packing Problem

This library is a grouping of 1D approximate solutions for the BPP  There is also a generic function to create variants.

## Example

```python

import random

from binpackp import NumberBin, Fit

bin_size = random.randint(10,100)

fit_these = [random.randint(1, bin_size) for _ in range(1000)]
generic_results = Fit.fit(NumberBin, bin_size, fit_these)

first_fit_results = Fit.ff(NumberBin, bin_size, fit_these)

print("General Function: ", generic_results)
print("First Fit Function: ", first_fit_results)

