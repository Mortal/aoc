import argparse
import types
import datetime
import subprocess
import traceback
import importlib.abc
import importlib.util
import os
import re
import sys
from typing import Any, Generic, Iterator, TypeVar
from math import ceil, gcd  # type: ignore[import]
from collections import Counter  # type: ignore[import]


_parser = argparse.ArgumentParser()
_parser.add_argument("-p", "--paste", action="store_true", help="Get input from clipboard")
_parser.add_argument("-q", "--quiet", action="store_true", help="Only print the last line")
_parser.add_argument("-c", "--copy", action="store_true", help="Copy last line to clipboard")
_parser.add_argument("which", nargs="?", help="Which input to run/paste (e.g. 'samp' for sample input or 'test' for the full input")


path: str
inp: str
lines: list[str]
toks: list[Any]
ints: list[int]
linetoks: list[list[Any]]
lineints: list[list[int]]
sectionlines: list[list[str]]
sectiontoks: list[list[list[Any]]]
sectionints: list[list[list[int]]]
mat: "TupleStringMatrix"
cmat: "ComplexStringMatrix"


def _aoc_run(cliargs: Any, loader: importlib.abc.Loader, module: types.ModuleType, path_: str, quit_on_empty: bool = False) -> str:
    global path, inp, lines, toks, ints, linetoks, lineints, sectionlines, sectiontoks, sectionints, mat, cmat
    path = path_
    if path == "-":
        try:
            inp = sys.stdin.read()
        except (KeyboardInterrupt, EOFError):
            if quit_on_empty:
                print("\nBye!")
                raise SystemExit
            raise
    else:
        print(f"=============> {path} <=============")
        with open(path_) as fp:
            inp = fp.read()
    if quit_on_empty and not inp:
        raise SystemExit
    inp = inp.strip("\n")
    lines = inp.splitlines()
    sectionlines = [
        section.splitlines()
        for section in inp.strip("\n").split("\n\n")
    ]
    try:
        sectiontoks = [
            [
                [
                    int(w) if w[-1] in "0123456789" else w
                    for w in re.findall("([^0-9 ,;.=-][^0-9 ,;.=]*|-?[0-9]+)-?", line)
                ]
                for line in lines
            ]
            for lines in sectionlines
        ]
    except ValueError:
        sectiontoks = [
            [
                [
                    w
                    for w in re.findall("([^0-9 ,;.=-][^0-9 ,;.=]*|-?[0-9]+)-?", line)
                ]
                for line in lines
            ]
            for lines in sectionlines
        ]
    sectionints = [[[i for i in line if isinstance(i, int)] for line in section] for section in sectiontoks]
    linetoks = [line for section in sectiontoks for line in section]
    lineints = [[i for i in line if isinstance(i, int)] for line in linetoks]
    toks = [x for line in linetoks for x in line]
    ints = [i for line in lineints for i in line]
    mat = TupleStringMatrix(lines)
    cmat = ComplexStringMatrix(lines)
    emit_last_print_if_quiet = lambda: None
    last_line = ""
    if cliargs.quiet or cliargs.copy:
        def qprint(*args, **kwargs):
            nonlocal emit_last_print_if_quiet, last_line

            if cliargs.quiet:
                emit_last_print_if_quiet = lambda: print(*args, **kwargs)
            else:
                print(*args, **kwargs)
            if cliargs.copy and kwargs.get("file") is None:
                last_line = kwargs.get("sep", " ").join(map(str, args)) + kwargs.get("end", "\n")
        module.__dict__["print"] = qprint
    else:
        qprint = print
    try:
        loader.exec_module(module)
    except Exception:
        emit_last_print_if_quiet()
        traceback.print_exc()
    except SystemExit as e:
        if e.args:
            if isinstance(e.args[0], int):
                # exit(n) -> exit with code n
                if e.args[0]:
                    print(f"({module.__file__} exited with code {e.args[0]})")
            elif e.args[0] is None:
                # exit() -> exit successfully without printing anything extra
                pass
            elif e.args[0] is not None:
                # exit('msg') -> print('msg', file=sys.stderr) and exit with code 1
                qprint(e.args[0], file=sys.stderr)
    else:
        emit_last_print_if_quiet()
    return last_line.rstrip("\n")


V = TypeVar("V")


class Bfs(Generic[V]):
    def __init__(self, lines: list[str] | list[list[str]]) -> None:
        self._lines = lines

    def __call__(self, inits: list[V] | V | dict[V, int]) -> "Bfs":
        if isinstance(inits, list):
            self._bfs = [*inits]
            self.dist = {s: 0 for s in inits}
            self.parent = {s: s for s in inits}
        elif isinstance(inits, dict):
            self.dist = {**inits}
            self._bfs = list(inits)
            self.parent = {s: s for s in inits}
        else:
            assert isinstance(inits, tuple | complex)
            self.dist = {inits: 0}
            self._bfs = [inits]
            self.parent = {inits: inits}
        self._i = 0
        return self

    def multi(self) -> None:
        self([])

    def __iter__(self) -> "Bfs":
        assert self._i == 0
        return self

    def __next__(self) -> V:
        if self._i >= len(self._bfs):
            raise StopIteration
        v = self._bfs[self._i]
        self._i += 1
        return v

    def newsource(self, pos: V) -> bool:
        assert self._i == len(self._bfs)
        if pos in self.dist:
            return False
        self._bfs = [pos]
        self.dist[pos] = 0
        self.parent[pos] = pos
        self._i = 0
        return True

    def enqueue(self, pos: V) -> bool:
        assert 1 <= self._i <= len(self._bfs)
        cur = self._bfs[self._i - 1]
        if pos in self.dist:
            return False
        self.dist[pos] = self.dist[cur] + 1
        self.parent[pos] = cur
        self._bfs.append(pos)
        return True


class TupleStringMatrix:
    def __init__(self, lines: list[str]) -> None:
        self._lines = [list(line) for line in lines]
        self.bfs = Bfs[tuple[int, int]](self._lines)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._lines), len(self._lines[0])

    def append(self, row: list[str]) -> None:
        self._lines.append(row)

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, i: int) -> list[str]:
        return self._lines[i]

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self._lines)

    def keys(self) -> list[tuple[int, int]]:
        return [
            (i, j) for i, row in enumerate(lines) for j in range(len(row))
        ]

    def findall(self, ch: str) -> list[tuple[int, int]]:
        assert len(ch) == 1
        return [
            (i, j) for i, row in enumerate(lines) for j, c in enumerate(row) if c == ch
        ]

    def read(self, ij: tuple[int, int]) -> str:
        i, j = ij
        if 0 <= i < len(self._lines) and 0 <= j < len(self._lines[i]):
            return self._lines[i][j]
        return ''

    def neigh4(self, ij: tuple[int, int]) -> Iterator[tuple[int, int]]:
        i, j = ij
        n, m = self.shape
        yield i - 1, j
        yield i + 1, j
        yield i, j - 1
        yield i, j + 1

    def neigh4inside(self, ij: tuple[int, int]) -> Iterator[tuple[int, int]]:
        i, j = ij
        n, m = self.shape
        if i > 0:
            yield i - 1, j
        if i + 1 < n:
            yield i + 1, j
        if j > 0:
            yield i, j - 1
        if j + 1 < m:
            yield i, j + 1

    def neigh8(self, ij: tuple[int, int]) -> list[tuple[int, int]]:
        i, j = ij
        return [(i + a, j + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if not a == b == 0]


class ComplexStringMatrix:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines
        self.bfs = Bfs[complex](self._lines)
        self.shape = len(lines), len(lines[0])
        "shape is (rows, columns)"

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, i: int) -> str:
        return self._lines[i]

    def __iter__(self) -> Iterator[str]:
        return iter(self._lines)

    def findall(self, ch: str) -> list[complex]:
        assert len(ch) == 1
        return [
            complex(j, i) for i, row in enumerate(lines) for j, c in enumerate(row) if c == ch
        ]

    def read(self, pos: complex) -> str:
        "read(complex(2, 30)) or read(2+30j) -> read column 2, row 30"
        row = int(pos.imag)
        col = int(pos.real)
        if 0 <= row < len(self._lines) and 0 <= col < len(self._lines[row]):
            return self._lines[row][col]
        return ''

    def neigh4diag(self, pos: complex) -> list[complex]:
        row = int(pos.imag)
        col = int(pos.real)
        return [complex(col + a, row + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a and b]

    def neigh4(self, ij: complex) -> Iterator[complex]:
        i = int(ij.imag)
        j = int(ij.real)
        yield complex(j, i - 1)
        yield complex(j, i + 1)
        yield complex(j - 1, i)
        yield complex(j + 1, i)

    def neigh8(self, pos: complex) -> list[complex]:
        row = int(pos.imag)
        col = int(pos.real)
        return [complex(col + a, row + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if not a == b == 0]


class InputScanner:
    inputdir = "inputs"
    prefix: str
    suffix = ".txt"

    def __init__(self, basename: str) -> None:
        self.prefix = f"{basename}-"

    @property
    def help_pattern(self) -> str:
        return f"{self.inputdir}/{self.prefix}*{self.suffix}"

    def scan(self) -> list[str]:
        inputfiles: list[tuple[int, str]] = []
        try:
            contents = os.listdir(self.inputdir)
        except FileNotFoundError:
            contents = []
        for f in contents:
            kind = f.removeprefix(self.prefix).removesuffix(self.suffix)
            if f == f"{self.prefix}{kind}{self.suffix}":
                path = self.path(kind)
                sz = os.stat(path).st_size
                inputfiles.append((sz, path))
        return [path for (sz, path) in sorted(inputfiles)]

    def path(self, kind: str) -> str:
        if kind == "-":
            return "/dev/stdin"
        return os.path.join(self.inputdir, f"{self.prefix}{kind}{self.suffix}")

    def has(self, kind: str) -> bool:
        return os.path.exists(self.path(kind))

    def makedirs(self) -> None:
        os.makedirs(self.inputdir, exist_ok=True)


def _aoc_main() -> None:
    mainfile = sys.modules["__main__"].__file__
    assert mainfile
    basename = os.path.basename(mainfile).removesuffix(".py")
    assert re.fullmatch(r'^[a-z_][a-z_0-9]*$', basename)
    daymo = re.findall(r'[0-9]+', basename)
    years = [y for y in daymo if len(y) == 4]
    days = [int(d) for d in daymo if len(d) < 3]
    day = days[0] if days else None
    spec = importlib.util.spec_from_file_location("_aocmain", mainfile)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert module is not None
    assert spec.loader is not None

    input_scanner = InputScanner(basename)
    cliargs = _parser.parse_args()
    paste: bool = cliargs.paste
    which: str | None = cliargs.which
    stdin_tty = os.isatty(0)
    from_stdin = which == "-" or (not paste and not which and not stdin_tty)
    if paste or not from_stdin and not input_scanner.has(which or "test"):
        if which is None:
            files = [input_scanner.path(cliargs.which)] if cliargs.which else input_scanner.scan()
            print("Guessing paste kind from your clipboard metadata...")
            types = subprocess.check_output(("wl-paste", "-l")).decode().split()
            if "text/x-moz-url-priv" in types:
                url = subprocess.check_output(("wl-paste", "-t", "text/x-moz-url-priv")).decode().strip("\n").replace("\0", "")
            elif "chromium/x-source-url" in types:
                url = subprocess.check_output(("wl-paste", "-t", "chromium/x-source-url")).decode().strip("\n")
            elif paste or not files:
                cwdyears = re.findall("20[0-2][0-9]", os.getcwd())
                if cwdyears:
                    # There's a year in the path of the cwd, so use that.
                    theyear: int | None = int(cwdyears[-1])
                elif years:
                    theyear = int(years[0])
                else:
                    # Fall back on today's year.
                    today = datetime.date.today()
                    theyear = today.year
                theday = day or today.day
                runbase = f"{os.path.basename(sys.executable)} {sys.argv[0]}"
                raise SystemExit(
                    "It does not seem like you have copied Advent of Code input in your web browser.\n\n"
                    f"Please copy the sample data from https://adventofcode.com/{theyear}/day/{theday}\n"
                    f"or the test data from https://adventofcode.com/{theyear}/day/{theday}/input\n\n"
                    "usage:\n\n"
                    f"  {runbase}         to run on AoC input copied from your web browser\n"
                    f"  {runbase} -       to run on input from stdin\n"
                    f"  {runbase} < FILE  to run on input from FILE\n"
                    f"  {runbase} NAME    to store clipboard contents and run on that input\n\n"
                    f"Input data will be cached as {input_scanner.help_pattern} for subsequent reuse."
                )
            else:
                url = ""
            url = url.split("#")[0]
            urlinputmo = re.fullmatch(r'^https://adventofcode\.com/(\d+)/day/(\d+)(/input)?$', url)
            if urlinputmo:
                urlyear = int(urlinputmo.group(1))
                urlday = int(urlinputmo.group(2))
                isinput = urlinputmo.group(3) or ""

                cwdyears = re.findall("20[0-2][0-9]", os.getcwd())
                if cwdyears:
                    # There's a year in the path of the cwd, so use that.
                    theyear = int(cwdyears[-1])
                elif years:
                    theyear = int(years[0])
                else:
                    theyear = None
                if theyear and theyear != urlyear:
                    raise SystemExit(f"You have copied the input for the wrong year: {url} - you are running the code for year {theyear}, so you should copy from https://adventofcode.com/{theyear}/day/{day or urlday}{isinput}")
                if day and urlday != day:
                    raise SystemExit(f"You have copied the input for the wrong day: {url} - you are running the code for day {day}, so you should copy from https://adventofcode.com/{urlyear}/day/{day}{isinput}")

                print(f"Getting data from clipboard...")
                thetext = subprocess.check_output(("wl-paste",)).decode().strip("\n")
                assert thetext

                if isinput:
                    which = "test"
                else:
                    which = "samp"
                    i = 1
                    while input_scanner.has(which):
                        with open(input_scanner.path(which)) as fp:
                            if fp.read().strip("\n") == thetext:
                                break
                        i += 1
                        which = f"samp{i}"
            elif paste or not files:
                raise SystemExit(f"You appear to have copied some data from an unknown URL: {url!r}\n\nPlease copy the sample data directly from the AOC website, or copy the test data and run with -p samp or -p test")

        else:
            if input_scanner.has(which):
                raise SystemExit(f"Please delete {input_scanner.path(which)} and try again")
            print(f"Getting input {which!r} from clipboard...")
            thetext = subprocess.check_output(("wl-paste",)).decode().strip("\n")
            assert thetext

        if which is None:
            print("Unknown text pasted - continuing with previous sample input data")
        else:
            path = input_scanner.path(which)
            if input_scanner.has(which):
                print(f"Input {which!r} already exists at {path}")
            else:
                contents = f"{thetext}\n".encode()
                print(f"Storing clipboard contents as {path}...")
                input_scanner.makedirs()
                with open(path, "xb") as ofp:
                    ofp.write(contents)

    last_line = ""
    if from_stdin:
        if stdin_tty:
            print("Paste input data, end with CTRL-D")
        last_line = _aoc_run(cliargs, spec.loader, module, "-")
        if stdin_tty:
            while True:
                print("Done! Hope it went well. Anyway, you can paste another round of input data and press CTRL-D if you want. Or press CTRL-D or CTRL-C to exit right away.")
                last_line = _aoc_run(cliargs, spec.loader, module, "-", quit_on_empty=True)
    else:
        if cliargs.which:
            if "/" in cliargs.which or "." in cliargs.which:
                files = [cliargs.which]
            else:
                files = [input_scanner.path(cliargs.which)]
        else:
            files = input_scanner.scan()
        for path in files:
            last_line = _aoc_run(cliargs, spec.loader, module, path)
    if cliargs.copy and last_line:
        subprocess.run(("wl-copy",), input=last_line.encode())


_aoc_main()
raise SystemExit
