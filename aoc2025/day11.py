from aoc import linetoks
import functools

edgelists = {}
for u, *vs in linetoks:
    edgelists[u.strip(":")] = vs

if "you" in edgelists:
    @functools.cache
    def p1count(node: str) -> int:
        if node == "out":
            return 1
        return sum(p1count(v) for v in edgelists[node])

    print(p1count("you"))

if "svr" in edgelists:
    def count(strt: str, goal: str, avoid: str | None, avoid2: str | None):
        @functools.cache
        def fn(node: str) -> int:
            if node == goal:
                return 1
            if node == avoid or node == avoid2:
                return 0
            return sum(fn(v) for v in edgelists[node])

        return fn(strt)

    svrdac = count("svr", "dac", "fft", "out")
    dacfft = count("dac", "fft", "svr", "out")
    fftout = count("fft", "out", "svr", "dac")
    svrfft = count("svr", "fft", "dac", "out")
    fftdac = count("fft", "dac", "svr", "out")
    dacout = count("dac", "out", "svr", "fft")
    print(svrdac * dacfft * fftout + svrfft * fftdac * dacout)
