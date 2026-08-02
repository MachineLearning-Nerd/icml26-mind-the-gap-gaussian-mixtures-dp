# Method

Reconstruct the largest Gaussian scale compatible with each two-decimal reported loss, using the paper's selected K. Search a fixed interval and shift in `[0,1]` in float64, then recompute its hockey-stick difference with `mpmath` at 80 decimal digits. This is non-circular: the event is selected without using the final high-precision value, and one event is sufficient to contradict DP.
