# Advent of Code Python helper library

This is a small framework that takes care of storing text you have copied from adventofcode.com in your web browser in a local text file,
parsing it to extract numbers and lines and such, and running your solutions on both the sample input and the secret input.

It lets you solve AoC problems without having to use `with open()`, `splitlines()`, `map(int, ...)`, etc.,
and without storing sample inputs under `if True:` blocks.

When you import `aoc.py` using `from aoc import ...` in your script, `aoc.py` takes over execution
and runs your script on each stored input file in `inputs/`.
If nothing is stored for this script, it reads your clipboard contents and stores in `inputs/`.
You can run with `-q` to hide all but the last `print()` line.

You can always run your script with a plain `-` argument to read from stdin
or with `< FILE` to read the given file instead of using the magic in `inputs/`.
The framework checks `os.isatty(0)` and short-circuits if it detects that a file is being passed on stdin.

This project is NOT affiliated with or endorsed by Advent of Code in any way.

## Command-line interface tutorial

Suppose you have implemented `aoc2022d4.py` as follows:

```
from aoc import lineints
s = 0
for a, b, c, d in lineints:
    if a <= c <= d <= b or c <= a <= b <= d:
        s += 1
print("part 1:", s)
s = 0
for a, b, c, d in lineints:
    if a <= c <= b or c <= a <= d:
        s += 1
print("part 2:", s)
```

The first time you run `python3 aoc2022d4.py` you will be greeted by this output,
which helpfully tells you what to do:

```
Guessing paste kind from your clipboard metadata...
It does not seem like you have copied Advent of Code input in your web browser.

Please copy the sample data from https://adventofcode.com/2022/day/4
or the test data from https://adventofcode.com/2022/day/4/input

usage:

  python3 aoc2022d4.py         to run on AoC input copied from your web browser
  python3 aoc2022d4.py -       to run on input from stdin
  python3 aoc2022d4.py < FILE  to run on input from FILE
  python3 aoc2022d4.py NAME    to store clipboard contents and run on that input

Input data will be cached as inputs/aoc2022d4-*.txt for subsequent reuse.
```

If you then copy the sample data and run it again, it will print:

```
Guessing paste kind from your clipboard metadata...
Getting data from clipboard...
Storing clipboard contents as inputs/aoc2022d4-samp.txt...
=============> inputs/aoc2022d4-samp.txt <=============
part 1: 2
part 2: 4
```

Notice that the copied data has been stored as `inputs/aoc2022d4-samp.txt`.

-------

If you then go and copy your secret input and run it again, it will print:

```
mathias@apus:~/kattis/aoc/aoc2022$ python3 aoc2022d4.py 
Guessing paste kind from your clipboard metadata...
Getting data from clipboard...
Storing clipboard contents as inputs/aoc2022d4-test.txt...
=============> inputs/aoc2022d4-samp.txt <=============
part 1: 2
part 2: 4
=============> inputs/aoc2022d4-test.txt <=============
part 1: 524
part 2: 798
```

Notice how it runs first the sample input and then the secret input,
which has been stored at inputs/aoc2022d4-test.txt.

Since the secret input, named `test`, now exists,
subsequent executions will not look at your clipboard contents
and will instead go directly to running on the cached inputs.

-------

Run with `-p NAME` to paste another sample input and store it as `inputs/aoc2022d4-NAME.txt`.

Run with `-q` to only show the last `print()` statement in your script.


## System requirements

* GNU/Linux Wayland system with `wl-paste` available to read clipboard contents
* Firefox or Chromium browser


## Library

* from aoc import inp
  * The input as a single `str`, stripped of leading/trailing newlines.

* from aoc import lines
  * The input as a list of `str`, one string per line, with no trailing newlines.

* from aoc import sectionlines
  * The input as a list of lines, each "section" separated by two newlines. Can be used e.g. in 2022-11 and 2023-19.

* from aoc import ints
  * A list of all the integers in the input. Can be used e.g. in 2021-6 and 2021-7.

* from aoc import lineints
  * A list of lists of ints, each possibly-empty list containing the integers found in the line. Can be used e.g. in 2021-5, 2022-4 and 2023-9.

* from aoc import sectionints
  * A list of lists of lists of ints, ints per line separated by double newlines. Can be used e.g. in 2021-4 and 2022-1.

* from aoc import linetoks
  * A list of lists of strings and ints, each possibly-empty list containing the "words" and integers found in the line.

* from aoc import path
  * The path to the current input file as a string. Can be used for checking `if "samp" in path` and `if "test" in path`.

* from aoc import mat
  * The input viewed as an *n*×*m* matrix of characters, indexed using `(row,col)` tuples. Used in my solutions of 2023-3, 2023-10, 2023-11, 2023-14.

* from aoc import cmat
  * The input viewed as an *n*×*m* matrix of characters, indexed using `x+yj == complex(x,y)` complex numbers. Used in my solutions of 2023-16, 2023-17, 2023-23.


### String matrix BFS helper

The `from aoc import mat` and `from aoc import cmat` matrices implement a BFS helper.

Whether it's widely useful remains to be seen, but it's used in my solution of 2023-10.
