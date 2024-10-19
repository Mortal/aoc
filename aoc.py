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
from typing import Any, Iterator


_parser = argparse.ArgumentParser()
_parser.add_argument("-p", "--paste", action="store_true", help="Get input from clipboard")
_parser.add_argument("-q", "--quiet", action="store_true", help="Only print the last line")
_parser.add_argument("which", nargs="?", help="Which input to run/paste (e.g. 'samp' for sample input or 'test' for the full input")


path: str
inp: str
lines: list[str]
mat: "TupleStringMatrix"
cmat: "ComplexStringMatrix"


def _aoc_run(args: Any, loader: importlib.abc.Loader, module: types.ModuleType, path_: str, quit_on_empty: bool = False) -> None:
    global path, inp, lines, mat, cmat
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
    lines = inp.strip().splitlines()
    mat = TupleStringMatrix(lines)
    cmat = ComplexStringMatrix(lines)
    emit_last_print_if_quiet = lambda: None
    if args.quiet:
        def qprint(*args, **kwargs):
            nonlocal emit_last_print_if_quiet
            emit_last_print_if_quiet = lambda: print(*args, **kwargs)
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


class Bfs:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def __call__(self, inits: list[tuple[int, int]] | tuple[int, int] | dict[tuple[int, int], int]) -> "Bfs":
        if isinstance(inits, list):
            self._bfs = inits
            self.dist = {s: 0 for s in inits}
            self.parent = {s: s for s in inits}
        elif isinstance(inits, dict):
            self.dist = inits
            self._bfs = list(inits)
            self.parent = {s: s for s in inits}
        else:
            assert isinstance(inits, tuple)
            self.dist = {inits: 0}
            self._bfs = [inits]
            self.parent = {inits: inits}
        self._i = 0
        return self

    def __iter__(self) -> "Bfs":
        assert self._i == 0
        return self

    def __next__(self) -> tuple[int, int]:
        if self._i >= len(self._bfs):
            raise StopIteration
        v = self._bfs[self._i]
        self._i += 1
        return v

    def enqueue(self, pos: tuple[int, int]) -> bool:
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
        self._lines = lines
        self.shape = len(lines), len(lines[0])
        self.bfs = Bfs(self._lines)

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, i: int) -> str:
        return self._lines[i]

    def __iter__(self) -> Iterator[str]:
        return iter(self._lines)

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
            complex(i, j) for i, row in enumerate(lines) for j, c in enumerate(row) if c == ch
        ]

    def read(self, pos: complex) -> str:
        "read(complex(2, 30)) or read(2+30j) -> read column 2, row 30"
        row = int(pos.imag)
        col = int(pos.real)
        if 0 <= row < len(self._lines) and 0 <= col < len(self._lines[row]):
            return self._lines[row][col]
        return ''


class InputScanner:
    inputdir = "inputs"
    prefix: str
    suffix = ".txt"

    def __init__(self, basename: str) -> None:
        self.prefix = f"{basename}-"

    def scan(self) -> list[str]:
        inputfiles: list[tuple[int, str]] = []
        for f in os.listdir(self.inputdir):
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
    daymo = re.search(r'[0-9]+', basename)
    day = int(daymo.group()) if daymo else None
    spec = importlib.util.spec_from_file_location("_aocmain", mainfile)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert module is not None
    assert spec.loader is not None

    input_scanner = InputScanner(basename)
    args = _parser.parse_args()
    paste: bool = args.paste
    which: str | None = args.which
    stdin_tty = os.isatty(0)
    from_stdin = which == "-" or (not paste and not which and not stdin_tty)
    if paste or not from_stdin and not input_scanner.has(which or "test"):
        if which is None:
            print("Guessing paste kind from your clipboard metadata...")
            types = subprocess.check_output(("wl-paste", "-l")).decode().split()
            if "text/x-moz-url-priv" in types:
                url = subprocess.check_output(("wl-paste", "-t", "text/x-moz-url-priv")).decode().strip().replace("\0", "")
            elif "chromium/x-source-url" in types:
                url = subprocess.check_output(("wl-paste", "-t", "chromium/x-source-url")).decode().strip()
            else:
                cwdyears = re.findall("20[0-2][0-9]", os.getcwd())
                if cwdyears:
                    # There's a year in the path of the cwd, so use that.
                    theyear = int(cwdyears[-1])
                else:
                    # Fall back on today's year.
                    today = datetime.date.today()
                    theyear = today.year
                theday = day or today.day
                raise SystemExit(f"Please copy the sample data from https://adventofcode.com/{theyear}/day/{theday} or the test data from https://adventofcode.com/{theyear}/day/{theday}/input")
            urlinputmo = re.fullmatch(r'^https://adventofcode\.com/(\d+)/day/(\d+)(/input)?$', url)
            if not urlinputmo:
                raise SystemExit(f"You appear to have copied some data from an unknown URL: {url!r}\n\nPlease copy the sample data directly from the AOC website, or copy the test data and run with -p samp or -p test")

            urlyear = int(urlinputmo.group(1))
            urlday = int(urlinputmo.group(2))
            isinput = urlinputmo.group(3) or ""

            if day and urlday != day:
                raise SystemExit(f"You have copied the input for the wrong day: {url} - you are running the code for day {day}, so you should copy from https://adventofcode.com/{urlyear}/day/{day}{isinput}")

            print(f"Getting data from clipboard...")
            thetext = subprocess.check_output(("wl-paste",)).decode().strip()
            assert thetext

            if isinput:
                which = "test"
            else:
                which = "samp"
                i = 1
                while input_scanner.has(which):
                    with open(input_scanner.path(which)) as fp:
                        if fp.read().strip() == thetext:
                            break
                    i += 1
                    which = f"samp{i}"
        else:
            if input_scanner.has(which):
                raise SystemExit(f"Please delete {input_scanner.path(which)} and try again")
            print(f"Getting input {which!r} from clipboard...")
            thetext = subprocess.check_output(("wl-paste",)).decode().strip()
            assert thetext

        path = input_scanner.path(which)
        if input_scanner.has(which):
            print(f"Input {which!r} already exists at {path}")
        else:
            contents = f"{thetext}\n".encode()
            print(f"Storing clipboard contents as {path}...")
            input_scanner.makedirs()
            with open(path, "xb") as ofp:
                ofp.write(contents)

    if from_stdin:
        if stdin_tty:
            print("Paste input data, end with CTRL-D")
        _aoc_run(args, spec.loader, module, "-")
        if stdin_tty:
            while True:
                print("Done! Hope it went well. Anyway, you can paste another round of input data and press CTRL-D if you want. Or press CTRL-D or CTRL-C to exit right away.")
                _aoc_run(args, spec.loader, module, "-", quit_on_empty=True)
    else:
        files = [input_scanner.path(args.which)] if args.which else input_scanner.scan()
        for path in files:
            _aoc_run(args, spec.loader, module, path)


_aoc_main()
raise SystemExit
