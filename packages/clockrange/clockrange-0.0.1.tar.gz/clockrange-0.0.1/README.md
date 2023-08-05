[![CircleCI](https://circleci.com/gh/ccortezia/clockrange.svg?style=svg)](https://circleci.com/gh/ccortezia/clockrange)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d78ce1d72bb1d0b594b8/test_coverage)](https://codeclimate.com/github/ccortezia/clockrange/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/d78ce1d72bb1d0b594b8/maintainability)](https://codeclimate.com/github/ccortezia/clockrange/maintainability)

# clockrange

A clock-like periodic sequence generator

## Installation

```shell
pip install clockrange
```

## Getting Started

`ClockRange` provides clock-like sequences according to the given specification:

```python
from clockrange import ClockRange

# A typical 24h microsecond-granular clock.
clock = ClockRange((24, 60, 60, 1000, 1000))

# How many microseconds until the clock completes a full cycle?
len(clock)

# How does the clock look like when 150000 microseconds have passed?
clock[150000]
```

See more examples below.

## Examples

`ClockRange` accepts different specification formats:

```python
# These are equivalent:
ClockRange((3, 60))
ClockRange(([0, 1, 2], 60))
ClockRange((range(3), 60))
ClockRange((range(0, 3, 1), 60))

# These result in .counters being different from .rendered:
ClockRange((["A", "B", "Z"], 60))
ClockRange((range(4, 10, 2), 60))
```

`ClockRange` instances support random item access with O(1) runtime performance:

```python
clock = ClockRange((24, 60, 60))
clock[0] # ClockState(counters=(0, 0, 0), cycles=0, rendered=(0, 0, 0))
clock[1] # ClockState(counters=(0, 0, 1), cycles=0, rendered=(0, 0, 1))
clock[86400] # ClockState(counters=(0, 0, 0), cycles=1, rendered=(0, 0, 0))
```

`ClockRange.__len__` provides the cycle length:

```python
assert len(ClockRange((12,))) == 12
assert len(ClockRange((10, 10))) == 100
assert len(ClockRange((24, 60, 60))) == 86400
```

`ClockRange` instances can be iterated on:

```python
clock = ClockRange((24, 60, 60))
it = iter(clock)
next(it) # ClockState(counters=(0, 0, 0), cycles=0, rendered=(0, 0, 0))
next(it) # ClockState(counters=(0, 0, 1), cycles=0, rendered=(0, 0, 1))
```

`ClockRange` iterators never get exhausted, so loop control needs to be performed manually:

```python
for state in ClockRange((24, 60, 60):
    if state.cycle == 1:
        break
```

## Contributing

To run the test suite locally, clone and setup the repository for local development:

```shell
pipenv install
pytest --cov-report=html
```
