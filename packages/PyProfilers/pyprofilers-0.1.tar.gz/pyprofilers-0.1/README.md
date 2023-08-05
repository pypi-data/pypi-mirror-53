# PyProfilers
PyProfilers is collection of wrapper functions to various Python profilers which aims to make profiling more convenient.


## Simple examples:

### Import PyProfilers
```python
import pyprofilers as pp
```


### Profile with [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile)
Use the standard Python [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile) to list 
the cumulative time spent in the function `func` and all its subfunctions:

```python
@pp.profile(sort_by='cumulative', out_lines=30)
def func():
  ...
```

- `sort_by` can be used to sort the results according to the supplied criteria. All criterias can be found [here.](https://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats)
- `out_lines` controls the number of lines in results. Use `None` or ommit the arugment to show all.

### Profile with [line_profiler](https://github.com/rkern/line_profiler)
Use the [line_profiler](https://github.com/rkern/line_profiler) to list time spent within each line of `func`:

```python
@pp.profile(exit=1)
def func():
  ...
```

Set `exit` to `True` to stop the execution after the first call to `func` returns. This is useful if `func` is called multiple times to
avoid the repeated output of the profiler statistics.

### Simple Timer
To just time the execution of a function use the `simple_timer` decoration:

```python
@pp.simple_timer(num=1)
def func():
  ...
```

The `num` argument can be used to specify how often the function should be executed.
