__version__ = "1.0.1"
# Every computation the SEN0401 chapter 2 deck shows; outputs come from executing them, never from typing.
EX = {
 "units": ["10**8", "10**8 // 1000"],
 "fee": ["inputs = [15_000_000]; outputs = [10_000_000, 4_990_000]; sum(inputs) - sum(outputs)"],
 "change": ["20 - 5"],
 "wp": ["import math; q, p = 0.1, 0.9; P = lambda z: 1 - sum(math.exp(-z*q/p) * (z*q/p)**k / math.factorial(k) * (1 - (q/p)**(z-k)) for k in range(z+1)); round(P(1), 7)", "round(P(6), 7)"],
 "table": ["[round(P(z), 7) for z in range(0, 11)]"],
}
