import contextlib
import os
import select
import signal
import sys
import termios
import tty


def stdin_read1(fd=0) -> str:
    "Read exactly one UTF-8 character from stdin using the read(2) syscall"
    return parse_one_character(os.read(fd, 1), lambda: os.read(fd, 1))


def wait_stdin_read1(
    timeout: float | None, extra_timeout: float | None = 0.1, fd=0
) -> str:
    "Read exactly one UTF-8 character from stdin with read(2) and select(2)"

    def get_next_byte() -> bytes:
        if timeout is not None:
            a, b, c = select.select([fd], [], [], timeout)
            if not a:
                return b""
        return os.read(fd, 1)

    b = get_next_byte()
    if not b:
        return ""
    # Update the variable "timeout", which is captured in get_next_byte()
    timeout = extra_timeout
    return parse_one_character(b, get_next_byte)


def parse_one_character(first_byte: bytes, get_next_byte) -> str:
    "Parse one UTF-8 character from first byte and a callable to get more bytes"
    assert len(first_byte) == 1
    b = first_byte
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError as e:
        if e.reason != "unexpected end of data":
            raise
    for i in range(10):
        bb = get_next_byte()
        if not bb:
            # Just bubble up the UnicodeDecodeError
            return b.decode("utf-8")
        assert len(bb) == 1
        b += bb
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError as e:
            if e.reason != "unexpected end of data":
                raise
    # Just bubble up the UnicodeDecodeError
    return b.decode("utf-8")


def read_one_keystroke(
    timeout: float | None, extra_timeout: float | None = 0.1, fd=0
) -> str:
    "Read exactly one Linux console keystroke from stdin"
    return parse_one_keystroke(
        wait_stdin_read1(timeout, fd=fd), lambda: wait_stdin_read1(extra_timeout, fd=fd)
    )


def parse_one_keystroke(first_char: str, get_next_char) -> str:
    "Parse one Linux console keystroke using rules from console_codes(4)"
    s = first_char
    assert len(s) == 1
    codes = {
        "\x01": "CTRL-A",
        "\x02": "CTRL-B",
        "\x03": "CTRL-C",
        "\x04": "CTRL-D",
        "\x05": "CTRL-E",
        "\x06": "CTRL-F",
        "\x07": "CTRL-G",
        "\x08": "CTRL-H",
        "\t": "tab",
        "\n": "newline",
        "\x0B": "CTRL-K",
        "\x0C": "CTRL-L",
        "\r": "return",
        "\x0E": "CTRL-N",
        "\x0F": "CTRL-O",
        "\x10": "CTRL-P",
        "\x11": "CTRL-Q",
        "\x12": "CTRL-R",
        "\x13": "CTRL-S",
        "\x14": "CTRL-T",
        "\x15": "CTRL-U",
        "\x16": "CTRL-V",
        "\x17": "CTRL-W",
        "\x18": "CTRL-X",
        "\x19": "CTRL-Y",
        "\x1A": "CTRL-Z",
        "\x7f": "backspace",
    }
    esccodes = {
        "\x7f": "ALT-backspace",
    }
    altocodes = {
        "P": "F1",
        "Q": "F2",
        "R": "F3",
        "S": "F4",
    }
    csicodes = {
        "A": "uparrow",
        "B": "downarrow",
        "C": "rightarrow",
        "D": "leftarrow",
        "F": "end",
        "H": "home",
        "2~": "insert",
        "3~": "delete",
        "5~": "pageup",
        "6~": "pagedown",
        "15~": "F5",
        "17~": "F6",
        "18~": "F7",
        "19~": "F8",
        "20~": "F9",
        "22~": "F10",
        "23~": "F11",
        "24~": "F12",
        "15;2~": "SHIFT-F5",
        "17;2~": "SHIFT-F6",
        "18;2~": "SHIFT-F7",
        "19;2~": "SHIFT-F8",
        "20;2~": "SHIFT-F9",
        "22;2~": "SHIFT-F10",
        "23;2~": "SHIFT-F11",
        "24;2~": "SHIFT-F12",
        "15;5~": "CTRL-F5",
        "17;5~": "CTRL-F6",
        "18;5~": "CTRL-F7",
        "19;5~": "CTRL-F8",
        "20;5~": "CTRL-F9",
        "21;5~": "CTRL-F10",
        "23;5~": "CTRL-F11",
        "24;5~": "CTRL-F12",
        "15;3~": "ALT-F5",
        "17;3~": "ALT-F6",
        "18;3~": "ALT-F7",
        "19;3~": "ALT-F8",
        "20;3~": "ALT-F9",
        "21;3~": "ALT-F10",
        "23;3~": "ALT-F11",
        "24;3~": "ALT-F12",
        "15;4~": "ALT-SHIFT-F5",
        "17;4~": "ALT-SHIFT-F6",
        "18;4~": "ALT-SHIFT-F7",
        "19;4~": "ALT-SHIFT-F8",
        "20;4~": "ALT-SHIFT-F9",
        "21;4~": "ALT-SHIFT-F10",
        "23;4~": "ALT-SHIFT-F11",
        "24;4~": "ALT-SHIFT-F12",
        "15;8~": "CTRL-ALT-SHIFT-F5",
        "17;8~": "CTRL-ALT-SHIFT-F6",
        "18;8~": "CTRL-ALT-SHIFT-F7",
        "19;8~": "CTRL-ALT-SHIFT-F8",
        "20;8~": "CTRL-ALT-SHIFT-F9",
        "21;8~": "CTRL-ALT-SHIFT-F10",
        "23;8~": "CTRL-ALT-SHIFT-F11",
        "24;8~": "CTRL-ALT-SHIFT-F12",
        "5;3~": "ALT-pageup",
        "6;3~": "ALT-pagedown",
        "5;7~": "CTRL-ALT-pageup",
        "6;7~": "CTRL-ALT-pagedown",
        "1;2P": "SHIFT-F1",
        "1;2Q": "SHIFT-F2",
        "1;2R": "SHIFT-F3",
        "1;2S": "SHIFT-F4",
        "1;5P": "CTRL-F1",
        "1;5Q": "CTRL-F2",
        "1;5R": "CTRL-F3",
        "1;5S": "CTRL-F4",
        "1;3P": "ALT-F1",
        "1;3Q": "ALT-F2",
        "1;3R": "ALT-F3",
        "1;3S": "ALT-F4",
        "1;4P": "ALT-SHIFT-F1",
        "1;4Q": "ALT-SHIFT-F2",
        "1;4R": "ALT-SHIFT-F3",
        "1;4S": "ALT-SHIFT-F4",
        "1;8P": "CTRL-ALT-SHIFT-F1",
        "1;8Q": "CTRL-ALT-SHIFT-F2",
        "1;8R": "CTRL-ALT-SHIFT-F3",
        "1;8S": "CTRL-ALT-SHIFT-F4",
        "1;6P": "CTRL-ALT-F1",
        "1;6Q": "CTRL-ALT-F2",
        "1;6R": "CTRL-ALT-F3",
        "1;6S": "CTRL-ALT-F4",
        "1;3A": "ALT-uparrow",
        "1;3B": "ALT-downarrow",
        "1;3C": "ALT-rightarrow",
        "1;3D": "ALT-leftarrow",
        "1;3F": "ALT-end",
        "1;3H": "ALT-home",
        "1;5A": "CTRL-uparrow",
        "1;5B": "CTRL-downarrow",
        "1;5C": "CTRL-rightarrow",
        "1;5D": "CTRL-leftarrow",
        "1;5F": "CTRL-end",
        "1;5H": "CTRL-home",
        "1;7F": "CTRL-ALT-end",
        "1;7H": "CTRL-ALT-home",
        "2;3~": "ALT-insert",
        "2;5~": "CTRL-insert",
        "3;2~": "SHIFT-delete",
        "3;3~": "ALT-delete",
        "3;5~": "CTRL-delete",
        "200~": "pastestart",
        "201~": "pasteend",
    }
    o = ord(s)
    if 32 <= o != 127:
        return s
    if s == "\x1b":
        s = get_next_char()
        if s == "":
            return "escape"
        if s == "[":
            s = get_next_char()
            while 0x20 <= ord(s[-1]) < 0x3C:
                ss = get_next_char()
                if not ss:
                    break
                s += ss
            try:
                return csicodes[s]
            except KeyError:
                raise NotImplementedError("Need csicodes entry: %r: ''" % (s,))
        if s == "O":
            s = get_next_char()
            if not s:
                return "ALT-O"
            try:
                return altocodes[s]
            except KeyError:
                raise NotImplementedError("Need altocodes entry: %r: ''" % (s,))
        o = ord(s)
        if 32 <= o < 127 or 255 < o:
            return "ALT-" + s
        try:
            return esccodes[s]
        except KeyError:
            raise NotImplementedError("Need esccodes entry: %r: ''" % (s,))
    try:
        return codes[s]
    except KeyError:
        raise NotImplementedError("Need codes entry: %r: ''" % (s,))


class MiniScreen:
    def __init__(self, stdin=0, stdout=sys.stdout) -> None:
        self._stdin = stdin
        self._stdout = stdout

        self._screen_lines: list[str] = []
        self._linebuf = ""
        self._cursor = 0

    @contextlib.contextmanager
    def minimize(self):
        self.cleanup()
        try:
            yield
        finally:
            self.start()

    def minimize_sigstop(self) -> None:
        with self.minimize():
            os.kill(os.getpid(), signal.SIGSTOP)

    def cleanup(self) -> None:
        # Set stdin to cooked mode
        termios.tcsetattr(self._stdin, termios.TCSAFLUSH, self.old)
        del self.old
        # Enable autowrap
        self._stdout.write("\x1b[?7h")
        # Disable bracketed paste
        self._stdout.write("\x1b[?2004l")
        self._stdout.flush()

    def start(self) -> None:
        # Enable bracketed paste
        self._stdout.write("\x1b[?2004h")
        # Disable autowrap
        self._stdout.write("\x1b[?7l")
        # Set stdin to raw mode
        self.old = termios.tcgetattr(self._stdin)
        tty.setraw(self._stdin)
        # Hack: use set_window() to redraw screen_lines+linebuf and flush
        lines = self._screen_lines[:]
        del self._screen_lines[:]
        self.set_window(lines)
        self._stdout.flush()

    def __enter__(self) -> "MiniScreen":
        self.start()
        return self

    def __exit__(self, ext, exv, exb) -> None:
        self.cleanup()

    def __iter__(self) -> "MiniScreen":
        return self

    def __next__(self) -> str:
        s = read_one_keystroke(None, fd=self._stdin)
        if s == "CTRL-D":
            raise StopIteration
        if s == "CTRL-C":
            raise KeyboardInterrupt
        ev = self.handle_keystroke(s)
        if ev is not None:
            return ev
        return s

    def set_line(self, s: str, c: int | None = None) -> None:
        if c is None:
            c = len(s)
        c = max(0, min(c, len(s)))
        self._linebuf = s
        self._stdout.write("\r\x1b[K" + self._linebuf)
        self._cursor = c
        if self._cursor != len(self._linebuf):
            self._stdout.write("\x1b[%sD" % (len(self._linebuf) - self._cursor))
        self._stdout.flush()

    def _move_up(self, nlines: int) -> None:
        if nlines:
            self._stdout.write("\x1b[%sA" % nlines)

    def _move_down(self, nlines: int) -> None:
        if nlines:
            self._stdout.write("\x1b[%sB" % nlines)

    def _insert_line(self) -> None:
        self._stdout.write("\x1b[1L")

    def _print_line_1(self, line: str) -> None:
        self._stdout.write("\r")
        self._move_up(len(self._screen_lines))
        self._insert_line()
        self._stdout.write("%s\r" % (line,))
        self._move_down(len(self._screen_lines))
        self._stdout.write("\n")

    def print_line(self, line: str) -> None:
        self._print_line_1(line)
        if self._cursor != 0:
            self._stdout.write("\x1b[%sD" % self._cursor)
        self._stdout.flush()

    def set_window(self, lines: list[str]) -> None:
        self._move_up(len(self._screen_lines))
        i = 0
        for line in lines:
            if i == len(self._screen_lines):
                self._stdout.write("\x1b[1L")
                self._stdout.write("%s\r\n" % line)
                self._screen_lines.append(line)
                i += 1
            else:
                self._screen_lines[i] = line
                i += 1
                self._stdout.write("\x1b[K%s\r\n" % (line,))
        if i < len(self._screen_lines):
            self._stdout.write("\r\x1b[%sM" % (len(self._screen_lines) - i))
            del self._screen_lines[i:]
        if self._screen_lines and self._screen_lines[-1]:
            self._stdout.write("\r")
        self._stdout.write(self._linebuf)
        if self._cursor != len(self._linebuf):
            self._stdout.write("\x1b[%sD" % (len(self._linebuf) - self._cursor))
        self._stdout.flush()

    def handle_keystroke(self, s: str) -> str | None:
        if s in ("return", "newline"):
            self._print_line_1(self._linebuf)
            self._linebuf = ""
            self._cursor = 0
            self._stdout.write("\x1b[K")
            self._stdout.flush()
            return "newline"
        elif s == "backspace":
            if self._cursor:
                self._linebuf = (
                    self._linebuf[: self._cursor - 1] + self._linebuf[self._cursor :]
                )
                self._cursor -= 1
                self._stdout.write("\x08\x1b[1P")
                self._stdout.flush()
            return "erase"
        elif len(s) == 1:
            if self._cursor != len(self._linebuf):
                self._stdout.write("\x1b[1@")
            self._linebuf = (
                self._linebuf[: self._cursor] + s + self._linebuf[self._cursor :]
            )
            self._cursor += 1
            self._stdout.write(s)
            self._stdout.flush()
            return "input"
        elif s in ("CTRL-A", "home"):
            self._cursor = 0
            self._stdout.write("\r")
            self._stdout.flush()
            return "arrow"
        elif s in ("CTRL-E", "end"):
            self._cursor = len(self._linebuf)
            self._stdout.write("\r")
            if self._cursor:
                self._stdout.write("\x1b[%sC" % self._cursor)
            self._stdout.flush()
            return "arrow"
        elif s == "CTRL-U":
            self._cursor = 0
            self._linebuf = ""
            self._stdout.write("\r\x1b[K")
            self._stdout.flush()
            return "erase"
        elif s == "ALT-backspace":
            i = self._cursor
            while i > 0 and not self._linebuf[i - 1].isalnum():
                i -= 1
            while i > 0 and self._linebuf[i - 1].isalnum():
                i -= 1
            self._linebuf = self._linebuf[:i] + self._linebuf[self._cursor :]
            self._stdout.write("\x1b[%sD" % (self._cursor - i))
            self._stdout.write("\x1b[%sP" % (self._cursor - i))
            self._cursor = i
            self._stdout.flush()
            return "erase"
        elif s == "CTRL-W":
            i = self._cursor
            while i > 0 and self._linebuf[i - 1].isspace():
                i -= 1
            while i > 0 and not self._linebuf[i - 1].isspace():
                i -= 1
            self._linebuf = self._linebuf[:i] + self._linebuf[self._cursor :]
            self._stdout.write("\x1b[%sD" % (self._cursor - i))
            self._stdout.write("\x1b[%sP" % (self._cursor - i))
            self._cursor = i
            self._stdout.flush()
            return "erase"
        elif s == "leftarrow":
            if self._cursor > 0:
                self._cursor -= 1
                self._stdout.write("\x1b[D")
                self._stdout.flush()
            return "arrow"
        elif s == "rightarrow":
            if self._cursor < len(self._linebuf):
                self._cursor += 1
                self._stdout.write("\x1b[C")
                self._stdout.flush()
            return "arrow"
        return None


def main() -> None:
    with MiniScreen() as screen:
        while True:
            s = read_one_keystroke(None)
            screen.print_line(s)
            if s in ("CTRL-C", "CTRL-D"):
                break


if __name__ == "__main__":
    main()
