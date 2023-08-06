# WITHTIMER

## Description

WithTimer is a Python module for benchmarking your code. It has the following features:

- Simple use
  - Just create a timer object, and it times execution until it goes out of scope
- Arbitrarily nested timers
  - Create as many nested timers as you want
  - Each timer pushes itself to a stack, and pops itself off when destroyed

## Example usage

```Python
with Timer(name="Something slow"):
  do_something_slow()
```

Timing is turned off by default, and can be optionally turned on. You can instrument your code with timers, and leave them in when you're not using them:

```Python
if args.enable_timing:
  Timer.enable_timing(args.enable_timing)
with Timer(name="Timers are a sometimes treat"):
  do_something()
```

You can nest timers:

```Python
with Timer(name="Outer timer"):
  for i in range(0, 100000):
    with Timer(name="Hope this isn't O(n^2)"):
      do_something_critical()
```

Here's a complete example:

```Python
from time import sleep
from withtimer.withtimer import Timer


def func1(count):
    for i in range(0, 3):
        with Timer(name="Calling func2"):
            func2(2)
    print("func1 sleeping {}".format(count))
    sleep(count)


def func2(count):
    print("func2 sleeping {}".format(count))
    sleep(count)


if __name__ == "__main__":
    Timer.enable_timing(True)
    with Timer(name="main"):
        for i in range(0, 3):
            if i % 2 > 0:
                func1(i+1)

```

Output:

```console
$ python3  ./example.py
[main] start
    [Calling func2] start
func2 sleeping 2
    [Calling func2] end	Elapsed time: 2.003 seconds

    [Calling func2] start
func2 sleeping 2
    [Calling func2] end	Elapsed time: 2.003 seconds

    [Calling func2] start
func2 sleeping 2
    [Calling func2] end	Elapsed time: 2.003 seconds

func1 sleeping 2
[main] end	Elapsed time: 8.015 seconds
$
```
