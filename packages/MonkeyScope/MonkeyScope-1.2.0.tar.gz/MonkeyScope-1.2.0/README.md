# MonkeyScope Beta
Distribution Timer for Non-deterministic Value Generators

### Sister Projects:
- Fortuna: Collection of abstractions to make custom random value generators. https://pypi.org/project/Fortuna/
- Pyewacket: Complete drop-in replacement for the Python3 random module. https://pypi.org/project/Pyewacket/
- RNG: Python3 API for the C++ Random Library. https://pypi.org/project/RNG/

Support these and other random projects: https://www.patreon.com/brokencode

### Quick Install
``` 
$ pip install MonkeyScope
$ python3
>>> import MonkeyScope
```

### Installation may require the following:
- Python 3.6 or later with dev tools (setuptools, pip, etc.)
- Cython: `pip install Cython`
- Modern C++17 compiler and standard library for your platform.

---

## MonkeyScope Specifications
- `MonkeyScope.distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - Logger for the statistical analysis of non-deterministic output.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `MonkeyScope.distribution(func: staticmethod, *args, **kwargs) -> None`
    - Stats and distribution.
- `MonkeyScope.timer(func: staticmethod, *args, **kwargs) -> None`
    - Just the function timer.

## MonkeyScope Terminal Example
```
$ python3
Python 3.7.3
>>> import MonkeyScope, random
>>> MonkeyScope.timer(random.random)
Typical Timing: 45 ± 7 ns

```
### MonkeyScope Script Example
```python
import MonkeyScope, random


x, y, z = 1, 10, 2
MonkeyScope.distribution_timer(random.randint, x, y)
MonkeyScope.distribution_timer(random.randrange, x, y)
MonkeyScope.distribution_timer(random.randrange, x, y, z)
```
### Typical Script Output
```
Output Analysis: Random.randint(1, 10)
Typical Timing: 1312 ± 89 ns
Statistics of 1000 samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.434
 Std Deviation: 2.9475977222701766
Distribution of 100000 samples:
 1: 9.914%
 2: 10.032%
 3: 10.014%
 4: 10.083%
 5: 9.891%
 6: 10.021%
 7: 9.956%
 8: 9.994%
 9: 10.128%
 10: 9.967%

Output Analysis: Random.randrange(1, 10)
Typical Timing: 1115 ± 11 ns
Statistics of 1000 samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.988
 Std Deviation: 2.5734176649892024
Distribution of 100000 samples:
 1: 11.182%
 2: 11.107%
 3: 10.943%
 4: 11.287%
 5: 11.061%
 6: 11.123%
 7: 11.118%
 8: 11.237%
 9: 10.942%

Output Analysis: Random.randrange(1, 10, 2)
Typical Timing: 1382 ± 66 ns
Statistics of 1000 samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.028
 Std Deviation: 2.7244519886829788
Distribution of 100000 samples:
 1: 19.999%
 3: 19.954%
 5: 20.077%
 7: 19.971%
 9: 19.999%

```


### Development Log:

##### MonkeyScope 1.2.0
- Replaced stats module with numpy

##### MonkeyScope 1.1.5
- Public Release

##### MonkeyScope Beta 0.1.5
- Installer Update

##### MonkeyScope Beta 0.1.4
- Minor Bug Fix

##### MonkeyScope Beta 0.1.3
- Continued Development

##### MonkeyScope Beta 0.1.2
- Renamed to MonkeyScope

##### MonkeyTimer Beta 0.0.2
- Changed to c++ compiler

##### MonkeyTimer Beta 0.0.1
- Initial Project Setup
