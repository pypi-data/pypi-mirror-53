import cProfile, pstats, io
from time import process_time as timer1, perf_counter as timer2, time as timer3
import functools
import sys

__all__ = ['simple_timer', 'profile', 'profile_by_line', 'profile_with_yappi']

def simple_timer(_func, *, num=1):
    def decorator_simple_timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Timey function
            s1, s2, s3 = timer1(), timer2(), timer3()
            for _ in range(num):
                result = func(*args, **kwargs)
            e1, e2, e3 = timer1(), timer2(), timer3()

            # Print stats
            print(f"{func.__name__}:")
            for start, end, timer in zip((s1, s2, s3), (e1, e2, e3), (timer1, timer2, timer3)):
                print(f"  {timer.__name__:12}: {(end - start) / num:.6f}s")

            return result

        return wrapper

    if _func is None:
        return decorator_simple_timer
    else:
        return decorator_simple_timer(_func)


def profile(_func=None, *, num=1, out_lines=30, sort_by='cumulative'):
    """A decorator that uses cProfile to profile a function."""

    def decorator_profile(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Profile function
            pr = cProfile.Profile()
            t1, t2 = timer1(), timer2()
            pr.enable()
            if num > 1:
                for _ in range(num - 1):
                    func(*args, **kwargs)
            result = func(*args, **kwargs)
            pr.disable()
            t1, t2 = timer1() - t1, timer2() - t2

            # Get stats
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)

            # Print stats
            print(f"\n{func.__name__}:\n"
                  f"{'': <9}{timer1.__name__}: {t1:.9f}s\n"
                  f"{'': <9}{timer2.__name__}: {t2:.9f}s")
            if out_lines:
                ps.print_stats()
                tmp = s.getvalue()
                tmp = tmp if out_lines == "all" else "\n".join(tmp.splitlines()[0:out_lines])
                print(tmp, end='\n' * 2)
            return result

        return wrapper

    if _func is None:
        return decorator_profile
    else:
        return decorator_profile(_func)


def formatted_number(number):
    remainder = number % 10
    suffix = ('st', 'nd', 'rd')[remainder - 1] if remainder < 3 else 'th'
    return f'{number}{suffix}'

def profile_by_line(_func=None, *, exit=False):
    def decorator_profile(func):
        from line_profiler import LineProfiler
        profile = LineProfiler()
        func = simple_timer(profile(func))
        counter = 1

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            profile.print_stats()
            if exit:
                nonlocal counter
                if counter == exit:
                    print(f"Exit after {formatted_number(counter)} call of {func.__name__}")
                    sys.exit()
                counter += 1
            return result

        return wrapper

    if _func is None:
        return decorator_profile
    else:
        return decorator_profile(_func)


def profile_with_yappi(func):
    import yappi
    yappi.set_clock_type('cpu')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Profile function
        yappi.start(builtins=True)
        t1, t2 = timer1(), timer2()
        result = func(*args, **kwargs)
        t1, t2 = timer1() - t1, timer2() - t2
        func_stats = yappi.get_func_stats()
        thread_stats = yappi.get_thread_stats()

        # Print stats
        print(f"\n\n{func.__name__}:\n\n"
              f"{'': <9}{timer1.__name__}: {t1:.9f}s\n"
              f"{'': <9}{timer2.__name__}: {t2:.9f}s")
        func_stats.print_all()
        thread_stats.print_all()
        return result

    return wrapper
