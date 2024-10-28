from aoc import lineints, path
if "test" in path:
    xmin = 200000000000000
    xmax = 400000000000000
else:
    xmin = 7
    xmax = 27
hail2d = []
for px,py,pz,vx,vy,vz in lineints:
    # assert xmin <= px <= xmax, px
    assert vx != 0
    assert vy != 0
    assert vz != 0
    hail2d.append((px,py,vx,vy))
count = 0
for i, (px1,py1,vx1,vy1) in enumerate(hail2d):
    # tmin1 = 0 if xmin <= px1 <= xmax else (xmin - px1) / vx1 if vx1 > 0 else (px1 - xmax) / vx1
    # tmax1 = (xmax - px1) / vx1 if vx1 > 0 else (px1 - xmin) / vx1
    for j, (px2,py2,vx2,vy2) in enumerate(hail2d[i+1:], i+1):
        # tmin2 = 0 if xmin <= px2 <= xmax else (xmin - px2) / vx2 if vx2 > 0 else (px2 - xmax) / vx2
        # tmax2 = (xmax - px2) / vx2 if vx2 > 0 else (px2 - xmin) / vx2
        print(f"Hailstone A: {px1}, {py1} @ {vx1}, {vy1}")
        print(f"Hailstone B: {px2}, {py2} @ {vx2}, {vy2}")
        # tmin = max(tmin1, tmin2)
        # tmax = min(tmax1, tmax2)
        # px = px2-px1
        # py = py2-py1
        # vx = vx2-vx1
        # vy = vy2-vy1
        # if px == vx == 0:
        #     if py == vy == 0:
        #         print(i, j, "always on top")
        #         assert 0
        #         count += 1
        #     elif py * vy < 0:
        #         ty = -py/vy
        #         assert ty >= 0
        #         if tmin <= ty <= tmax:
        #             print(i, j, "y", ty, px1 + vx1 * ty, px2 + vx2 * ty, py1 + vy1 * ty, py2 + vy2 * ty)
        #             count += 1
        #         else:
        #             print(i, j, "parallel-y, collide in the far future")
        #     else:
        #         print(i, j, "parallel-y, collide in the past")
        # elif py == py == 0:
        #     if px * vx < 0:
        #         tx = -px/vx
        #         assert tx >= 0
        #         if tmin <= tx <= tmax:
        #             print(i, j, "x", tx, px1 + vx1 * tx, px2 + vx2 * tx, py1 + vy1 * tx, py2 + vy2 * tx)
        #             count += 1
        #         else:
        #             print(i, j, "parallel-x, collide in the far future")
        #     else:
        #         print(i, j, "parallel-x, collide in the past")
        # elif px * vx < 0 and py * vy < 0:
        #     if px * vy == py * vx:
        #         tx = -px/vx
        #         assert tx >= 0
        #         ty = -py/vy
        #         assert ty >= 0
        #         print(i, j, "-", tx, ty, px1 + vx1 * tx, px2 + vx2 * tx, py1 + vy1 * tx, py2 + vy2 * tx)
        #     else:
        #         tx = -px/vx
        #         assert tx >= 0
        #         print(i, j, "*", tx, px1 + vx1 * tx, px2 + vx2 * tx, py1 + vy1 * tx, py2 + vy2 * tx)

        # y = py1 + (vy1 / vx1) * (x - px1)
        # y = py2 + (vy2 / vx2) * (x - px2)
        assert vx1 != 0
        assert vx2 != 0
        assert vy1 != 0
        assert vy2 != 0
        if vy1 * vx2 == vy2 * vx1:
            if (py1 - py2) * (vx1 * vx2) == (vy2 * px2 * vx1 - vy1 * px1 * vx2):
                print(1, i, j, "parallel coincide")
                count += 1
            else:
                print(2, "Hailstones' paths are parallel; they never intersect.")
        else:
            import fractions

            s1 = fractions.Fraction(vy1, vx1)
            s2 = fractions.Fraction(vy2, vx2)
            # py1 + s1 * (x - px1) = py2 + s2 * (x - px2)
            # (s1 - s2) * x = py2 - py1 + s1 * px1 - s2 * px2
            x = fractions.Fraction(py2 - py1 + s1 * px1 - s2 * px2, s1 - s2)
            y = fractions.Fraction(px2 - px1 + py1 / s1 - py2 / s2, 1 / s1 - 1 / s2)
            assert y != xmin
            assert y != xmax
            assert y != py1
            assert y != py2
            assert x != xmin
            assert x != xmax
            assert x != px1
            assert x != px2
            if xmin <= x <= xmax and xmin <= y <= xmax:
                if (x - px1) * vx1 >= 0:
                    if (x - px2) * vx2 >= 0:
                        print(3, f"Hailstones' paths will cross inside the test area (at x={x}).")
                        count += 1
                    else:
                        print(4, "Hailstones' paths crossed in the past for hailstone B.")
                else:
                    if (x - px2) * vx2 >= 0:
                        print(5, "Hailstones' paths crossed in the past for hailstone A.")
                    else:
                        print(6, "Hailstones' paths crossed in the past for both hailstones.")
            else:
                print(7, f"Hailstones' paths will cross outside the test area (at x={x}).", 1.0*min(abs(x-xmin),abs(x-xmax)))

assert xmin == 7 or count > 4382, count
assert xmin == 7 or count < 19112, count
print(count)
